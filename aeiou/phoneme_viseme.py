"""
音素 / 口型（viseme）相关工具方法。

主要功能：
- 使用 cmudict（CMU Pronouncing Dictionary）将英文文本转为 ARPAbet 音素序列；
- 将音素转换为 Polly 标准 viseme，并映射为 Live2D 口型参数（含平滑）；
- 可选返回 Microsoft 的 22 维 viseme ID，方便与 Azure 等引擎对齐。
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Iterable, List, Sequence, Tuple

from aeiou.viseme_standards import (
    phonemes_to_visemes,
    smooth_visemes,
    phonemes_to_ms_viseme_ids,
)

try:
    import cmudict  # type: ignore[import-not-found]
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "未检测到 cmudict 包。请先安装：pip install cmudict\n"
        f"导入错误: {e}"
    ) from e

_CMU_DICT = cmudict.dict()


class LipMode(str, Enum):
    """
    口型映射模式：

    - POLLY: 返回带有 label/open/form 的口型单元（适合直接驱动 Live2D ParamMouthOpenY / ParamMouthForm）
    - MS_ID: 返回 Microsoft 风格的 viseme ID（0–21），用于在上层做自定义映射
    """

    POLLY = "polly"
    MS_ID = "ms_id"


def text_to_phonemes_cmudict(text: str) -> list[str]:
    """
    将英文文本用 cmudict 查表转成 ARPAbet 音素序列。

    - 仅依赖词典，速度非常快；
    - 不在词典中的词（OOV）会被跳过；
    - 返回格式与 g2p_en 类似：音素之间用 \" \" 作为分隔（方便后续处理）。
    """
    words = re.findall(r"[A-Za-z']+", text.lower())
    out: list[str] = []
    for w in words:
        prons = _CMU_DICT.get(w)
        if not prons:
            continue
        out.extend(prons[0])
        out.append(" ")
    if out and out[-1] == " ":
        out.pop()
    return out


def phonemes_to_smoothed_visemes(
    phonemes: Sequence[str],
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> list[tuple[str, float, float]]:
    """
    ARPAbet 音素 → Polly viseme 名称 → Live2D 口型参数，并做平滑。

    返回：(label, ParamMouthOpen, ParamMouthForm) 列表。
    """
    base = phonemes_to_visemes(list(phonemes))
    return smooth_visemes(base, attack_alpha=attack_alpha, release_alpha=release_alpha)


def phonemes_to_ms_ids(phonemes: Sequence[str]) -> list[int]:
    """ARPAbet 音素 → Microsoft 22 维 viseme ID (0–21)。"""
    return phonemes_to_ms_viseme_ids(list(phonemes))


def text_to_visemes(
    text: str,
    *,
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> tuple[list[str], list[tuple[str, float, float]]]:
    """
    方便方法：一句英文文本 → (ARPAbet 音素序列, 平滑后的口型序列)。

    - 仅使用 cmudict 词典，OOV 会被忽略；
    - 如需更强大的 G2P，可在上层自行换成 g2p_en / 其他库，再复用 phonemes_to_smoothed_visemes。
    """
    phonemes = text_to_phonemes_cmudict(text)
    vis = phonemes_to_smoothed_visemes(
        phonemes, attack_alpha=attack_alpha, release_alpha=release_alpha
    )
    return phonemes, vis


def text_to_lip_units(
    text: str,
    *,
    mode: LipMode = LipMode.POLLY,
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> list[dict]:
    """
    高层封装：一句英文文本 → 口型「单元」列表，支持两种模式：

    - LipMode.POLLY: 返回 [{"label": str, "open": float, "form": float}, ...]
    - LipMode.MS_ID: 返回 [{"id": int}, ...]，id 为 0–21 的占位 viseme ID

    这样上层（如 live2d_deam_gal.py）只需要根据 mode 分支消费即可。
    """
    text = (text or "").strip()
    if not text:
        return []

    phonemes, visemes = text_to_visemes(
        text, attack_alpha=attack_alpha, release_alpha=release_alpha
    )

    if not phonemes or not visemes:
        return []

    if mode == LipMode.POLLY:
        # label/open/form 直接用于驱动 Live2D 口型
        return [
            {"label": label, "open": float(open_), "form": float(form)}
            for (label, open_, form) in visemes
        ]

    if mode == LipMode.MS_ID:
        ids = phonemes_to_ms_ids(phonemes)
        return [{"id": int(v)} for v in ids]

    # 未知模式，兜底为空列表，避免上层崩溃
    return []


# 每个音节约 0.08s，用于无 TTS 时间戳时的 fallback
_DEFAULT_SEC_PER_VISEME = 0.08


def text_to_timed_visemes(
    text: str,
    start_sec: float,
    end_sec: float,
    *,
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> list[tuple[str, float, float, float, float]]:
    """
    将文本转为带时间戳的口型序列，用于与音频时间轴同步。

    - 使用 text_to_visemes 得到 (label, open, form) 列表；
    - 在 [start_sec, end_sec] 内均匀分配每个 viseme 的起止时间（与 TTS 段时间轴一致）。

    返回：(label, open, form, t_start, t_end) 列表，t_start/t_end 单位秒。
    """
    if end_sec <= start_sec:
        return []
    _, visemes = text_to_visemes(
        text, attack_alpha=attack_alpha, release_alpha=release_alpha
    )
    if not visemes:
        return []
    duration = end_sec - start_sec
    step = duration / len(visemes)
    out: list[tuple[str, float, float, float, float]] = []
    for i, (label, open_, form) in enumerate(visemes):
        t_start = start_sec + i * step
        t_end = start_sec + (i + 1) * step
        out.append((label, open_, form, t_start, t_end))
    return out


def text_to_timed_visemes_fallback(
    text: str,
    *,
    start_sec: float = 0.0,
    sec_per_viseme: float = _DEFAULT_SEC_PER_VISEME,
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> list[tuple[str, float, float, float, float]]:
    """
    当没有 TTS 的 start/end 时间时使用的备用方案。

    区别：
    - text_to_timed_visemes(text, start_sec, end_sec)：有真实时间区间，口型均匀铺在 [start_sec, end_sec] 里，和音频对齐。
    - 本函数：没有真实区间，就「假设每个口型占固定时长」（默认 0.08 秒），从 start_sec 起逐个往后排。
      例如 3 个口型 → t_start 分别为 0, 0.08, 0.16，t_end 分别为 0.08, 0.16, 0.24。
    这样得到的时间轴是估的，和实际播放可能对不齐，只适合没有 TimedString 时的兜底。

    返回：(label, open, form, t_start, t_end)。
    """
    _, visemes = text_to_visemes(
        text, attack_alpha=attack_alpha, release_alpha=release_alpha
    )
    if not visemes:
        return []
    out: list[tuple[str, float, float, float, float]] = []
    for i, (label, open_, form) in enumerate(visemes):
        t_start = start_sec + i * sec_per_viseme
        t_end = t_start + sec_per_viseme
        out.append((label, open_, form, t_start, t_end))
    return out


