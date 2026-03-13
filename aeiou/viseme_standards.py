"""
标准 Viseme 映射表（供口型 / Lip Sync 使用）。

1. Amazon Polly (en-US): IPA → Viseme 名称
   https://docs.aws.amazon.com/polly/latest/dg/ph-table-english-us.html
   Viseme 名称: p, t, f, k, s, S, T, l, r, i, u, @, a, E, e, O, o 等

2. Microsoft Azure (22 Visemes): IPA → Viseme ID (0-21)
   https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# 1. Amazon Polly en-US: IPA → Viseme 名称
# 来源: https://docs.aws.amazon.com/polly/latest/dg/ph-table-english-us.html
# 辅音: b→p, d→t, d͡ʒ→S, ð→T, f→f, ɡ→k, h→k, j→i, k→k, l→l, m→p, n→t, ŋ→k, p→p, ɹ→r, s→s, ʃ→S, t͡ʃ→S, θ→T, t→t, v→f, w→u, z→s, ʒ→S
# 元音: ə→@, ɚ→@, æ→a, aɪ→a, aʊ→a, ɑ→a, eɪ→e, ɝ→E, ɛ→E, i→i, ɪ→i, oʊ→o, ɔ→O, ɔɪ→O, u→u, ʊ→u, ʌ→E
# 注: 多字符 IPA 用 Unicode 规范形式；Polly 表里 ɡ 为 U+0261
POLLY_IPA_TO_VISEME: dict[str, str] = {
    # Consonants
    "b": "p",
    "d": "t",
    "dʒ": "S",  # d͡ʒ
    "ð": "T",
    "f": "f",
    "ɡ": "k",  # ɡ (U+0261)
    "g": "k",
    "h": "k",
    "j": "i",
    "k": "k",
    "l": "l",
    "m": "p",
    "n": "t",
    "ŋ": "k",
    "p": "p",
    "ɹ": "r",
    "r": "r",
    "s": "s",
    "ʃ": "S",
    "tʃ": "S",  # t͡ʃ
    "θ": "T",
    "t": "t",
    "v": "f",
    "w": "u",
    "z": "s",
    "ʒ": "S",
    # Vowels
    "ə": "@",
    "ɚ": "@",
    "æ": "a",
    "aɪ": "a",
    "aʊ": "a",
    "ɑ": "a",
    "eɪ": "e",
    "ɝ": "E",
    "ɛ": "E",
    "i": "i",
    "ɪ": "i",
    "oʊ": "o",
    "ɔ": "O",
    "ɔɪ": "O",
    "u": "u",
    "ʊ": "u",
    "ʌ": "E",
}
POLLY_DEFAULT_VISEME = "E"

# Polly Viseme 名称 → (ParamMouthOpen, ParamMouthForm)，用于驱动 Live2D 口型
POLLY_VISEME_TO_MOUTH: dict[str, tuple[float, float]] = {
    "p": (0.0, 0.0),  # 双唇 b/m/p
    "t": (0.3, 0.2),  # 齿龈 d/n/t
    "f": (0.2, -0.2),  # 唇齿 f/v
    "k": (0.4, 0.0),  # 软腭 g/k/ŋ/h
    "s": (0.2, 0.5),  # 齿龈擦音 s/z
    "S": (0.25, 0.4),  # 颚龈 ʃ/tʃ/dʒ/ʒ
    "T": (0.2, 0.4),  # 齿音 θ/ð
    "l": (0.35, 0.2),  # 边音 l
    "r": (0.4, -0.3),  # 近音 ɹ
    "i": (0.8, 0.4),  # 前高 i/ɪ/j
    "u": (0.5, -0.5),  # 后圆 u/ʊ/w
    "@": (0.6, 0.2),  # 中元音 ə/ɚ
    "a": (1.0, 0.2),  # 开元音 æ/ɑ/aɪ/aʊ
    "E": (0.7, 0.3),  # 中前 ɛ/ʌ/ɝ
    "e": (0.75, 0.35),  # eɪ
    "O": (0.7, -0.7),  # ɔ/ɔɪ
    "o": (0.6, -0.6),  # oʊ
}
POLLY_DEFAULT_MOUTH = (0.3, 0.1)

# ---------------------------------------------------------------------------
# 2. Microsoft Azure: IPA → Viseme ID (0-21)
MS_IPA_TO_VISEME_ID: dict[str, int] = {
    "": 0,
    " ": 0,
    "æ": 1,
    "ə": 1,
    "ʌ": 1,
    "ɑ": 2,
    "ɔ": 3,
    "ɛ": 4,
    "ʊ": 4,
    "ɝ": 5,
    "ɚ": 5,
    "j": 6,
    "i": 6,
    "ɪ": 6,
    "w": 7,
    "u": 7,
    "o": 8,
    "oʊ": 8,
    "aʊ": 9,
    "ɔɪ": 10,
    "aɪ": 11,
    "h": 12,
    "ɹ": 13,
    "r": 13,
    "l": 14,
    "s": 15,
    "z": 15,
    "ʃ": 16,
    "tʃ": 16,
    "dʒ": 16,
    "ʒ": 16,
    "ð": 17,
    "f": 18,
    "v": 18,
    "d": 19,
    "t": 19,
    "n": 19,
    "θ": 19,
    "k": 20,
    "ɡ": 20,
    "g": 20,
    "ŋ": 20,
    "p": 21,
    "b": 21,
    "m": 21,
    "eɪ": 6,
    "a": 2,
}
MS_DEFAULT_VISEME_ID = 1

# ---------------------------------------------------------------------------
# 3. ARPAbet (g2p_en 输出) → IPA，用于接入上述标准表
ARPABET_TO_IPA: dict[str, str] = {
    "AA": "ɑ",
    "AE": "æ",
    "AH": "ʌ",
    "AH0": "ə",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "aɪ",
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "EH": "ɛ",
    "ER": "ɝ",
    "ER0": "ɚ",
    "EY": "eɪ",
    "F": "f",
    "G": "ɡ",
    "HH": "h",
    "IH": "ɪ",
    "IH0": "ɪ",
    "IY": "i",
    "IY0": "i",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "P": "p",
    "R": "ɹ",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "UH": "ʊ",
    "UW": "u",
    "UW0": "u",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ",
}


def arpabet_to_ipa(arpabet: str) -> str:
    """ARPAbet 符号（可带数字重音）转 IPA。先试完整符号如 AH0，再试去掉数字的 AH。"""
    raw = arpabet.strip().upper()
    if raw in ARPABET_TO_IPA:
        return ARPABET_TO_IPA[raw]
    key = re.sub(r"\\d", "", raw).upper()
    return ARPABET_TO_IPA.get(key, key.lower() if key else "ə")


def arpabet_to_polly_viseme(arpabet: str) -> str:
    """ARPAbet → Amazon Polly Viseme 名称。"""
    ipa = arpabet_to_ipa(arpabet)
    for seq in ("aɪ", "aʊ", "eɪ", "oʊ", "ɔɪ", "tʃ", "dʒ"):
        if ipa == seq or seq in ipa:
            return POLLY_IPA_TO_VISEME.get(seq, POLLY_DEFAULT_VISEME)
    return POLLY_IPA_TO_VISEME.get(ipa, POLLY_DEFAULT_VISEME)


def arpabet_to_ms_viseme_id(arpabet: str) -> int:
    """ARPAbet → Microsoft Viseme ID (0-21)。"""
    ipa = arpabet_to_ipa(arpabet)
    for seq in ("aʊ", "ɔɪ", "aɪ", "oʊ", "eɪ", "tʃ", "dʒ"):
        if ipa == seq or seq in ipa:
            return MS_IPA_TO_VISEME_ID.get(seq, MS_DEFAULT_VISEME_ID)
    return MS_IPA_TO_VISEME_ID.get(ipa, MS_DEFAULT_VISEME_ID)


def phonemes_to_polly_visemes(phonemes: list[str]) -> list[str]:
    """音素列表（ARPAbet，可带空格）→ Polly viseme 名称列表。"""
    out: list[str] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        out.append(arpabet_to_polly_viseme(p))
    return out


def phonemes_to_ms_viseme_ids(phonemes: list[str]) -> list[int]:
    """音素列表（ARPAbet）→ Microsoft viseme ID 列表。"""
    out: list[int] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        out.append(arpabet_to_ms_viseme_id(p))
    return out


def phonemes_to_visemes(phonemes: list[str]) -> list[tuple[str, float, float]]:
    """
    音素列表（ARPAbet）→ (Polly viseme 名称, ParamMouthOpen, ParamMouthForm)。
    先按 Polly 标准得到 viseme 名称，再查表得到 Live2D 口型参数。
    """
    out: list[tuple[str, float, float]] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        label = arpabet_to_polly_viseme(p)
        open_, form = POLLY_VISEME_TO_MOUTH.get(label, POLLY_DEFAULT_MOUTH)
        out.append((label, open_, form))
    return out


def smooth_visemes(
    visemes: list[tuple[str, float, float]],
    attack_alpha: float = 0.45,
    release_alpha: float = 0.2,
) -> list[tuple[str, float, float]]:
    """
    对口型序列做 attack/release 平滑，避免嘴型突变。

    attack_alpha：张嘴时跟随目标的速度（越大越快）；
    release_alpha：闭嘴时跟随的速度（通常略小，更自然）。
    返回与输入同长的 (label, open, form) 列表，open/form 为平滑后的值。
    """
    if not visemes:
        return []
    out: list[tuple[str, float, float]] = []
    last_open, last_form = visemes[0][1], visemes[0][2]
    for label, target_open, target_form in visemes:
        alpha = attack_alpha if target_open > last_open else release_alpha
        last_open += alpha * (target_open - last_open)
        last_form += alpha * (target_form - last_form)
        # 为了让 ParamMouthForm 在 0 附近既有正值也有负值，这里做一个简单的重心平移和缩放：
        # 1. 将原始 form 以 0.25 为中心平移到 0 附近；
        # 2. 略微放大振幅，使负值更容易出现，便于区分「圆嘴」与「扁嘴」。
        adjusted_form = (last_form - 0.25) * 1.5
        out.append((label, round(last_open, 4), round(adjusted_form, 4)))
    return out
