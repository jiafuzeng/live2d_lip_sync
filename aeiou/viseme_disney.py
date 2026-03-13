"""
Disney 12 口型（viseme）标准相关工具。

本文件独立实现了迪士尼 12 口型分组：
- IPA → 12 类嘴型 ID 映射
- ARPAbet → 上述 ID 的桥接
"""

from __future__ import annotations

from typing import List

from aeiou.viseme_polly import ARPABET_TO_IPA, arpabet_to_ipa

# IPA → Disney 12 口型类别 ID
DISNEY_IPA_TO_VISEME_ID: dict[str, int] = {
    # 1: [p, b, m] - 双唇闭合
    "p": 1,
    "b": 1,
    "m": 1,
    # 2: [w] - 圆唇前伸
    "w": 2,
    # 3: [r] - 稍圆的开口 /r/
    "ɹ": 3,
    "r": 3,
    # 4: [f, v] - 下唇贴上齿
    "f": 4,
    "v": 4,
    # 5: [th] - 舌头夹在齿间（θ, ð）
    "θ": 5,
    "ð": 5,
    # 6: [l] - 舌尖抵上齿后方，两侧有缝
    "l": 6,
    # 7: [d, t, z, s, n] - 齿龈音，牙齿大多闭合
    "d": 7,
    "t": 7,
    "z": 7,
    "s": 7,
    "n": 7,
    # 8: [ʃ, tʃ, dʒ, ʒ] - 颚龈擦音/塞擦音
    "ʃ": 8,
    "tʃ": 8,
    "dʒ": 8,
    "ʒ": 8,
    # 9: [j, g, k] - 半元音 / 软腭塞音
    "j": 9,
    "g": 9,
    "ɡ": 9,
    "k": 9,
    # 10: [前高元音一类，如 beat/bit] - 宽而略开的口
    "i": 10,
    "ɪ": 10,
    "e": 10,
    "eɪ": 10,
    # 11: [ow] - 圆唇元音
    "o": 11,
    "oʊ": 11,
    # 12: [ah, aa, ao, aw, oy, ay] - 张口较大的一系列开元音/双元音
    "a": 12,
    "ɑ": 12,
    "ɔ": 12,
    "aʊ": 12,
    "ɔɪ": 12,
    "aɪ": 12,
}
DISNEY_DEFAULT_VISEME_ID = 12


DISNEY_VISEME_ID_TO_PARAMS: dict[int, tuple[float, float]] = {
    # 1: p/b/m - 完全闭嘴
    1: (0.0, 0.0),
    # 2: w - 圆唇前伸，开口较小
    2: (0.4, -0.6),
    # 3: r - 稍圆的开口
    3: (0.5, -0.2),
    # 4: f/v - 下唇贴上齿，微张
    4: (0.25, 0.0),
    # 5: th - 舌夹齿间，中等开口
    5: (0.4, 0.2),
    # 6: l - 侧裂口型，中等开口
    6: (0.45, 0.2),
    # 7: d/t/z/s/n - 齿龈音，牙齿大多闭合，轻微张嘴
    7: (0.3, 0.2),
    # 8: ʃ/tʃ/dʒ/ʒ - 颚龈擦音，稍紧的口型
    8: (0.35, 0.3),
    # 9: j/g/k - 半元音 / 软腭塞音
    9: (0.4, 0.0),
    # 10: 前高元音（beat/bit 类）——宽而略开的口，偏扁
    10: (0.7, 0.4),
    # 11: ow 圆唇元音
    11: (0.65, -0.6),
    # 12: 大开口元音 / 双元音（ah/aa/ao/aw/oy/ay）
    12: (1.0, 0.2),
}


def arpabet_to_disney_viseme_id(arpabet: str) -> int:
    """ARPAbet → Disney 12 口型类别 ID。"""
    ipa = arpabet_to_ipa(arpabet)
    for seq in ("aʊ", "ɔɪ", "aɪ", "oʊ", "eɪ", "tʃ", "dʒ"):
        if ipa == seq or seq in ipa:
            return DISNEY_IPA_TO_VISEME_ID.get(seq, DISNEY_DEFAULT_VISEME_ID)
    return DISNEY_IPA_TO_VISEME_ID.get(ipa, DISNEY_DEFAULT_VISEME_ID)


def phonemes_to_disney_viseme_ids(phonemes: list[str]) -> list[int]:
    """音素列表（ARPAbet）→ Disney 12 口型类别 ID 列表。"""
    out: list[int] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        out.append(arpabet_to_disney_viseme_id(p))
    return out


__all__ = [
    "DISNEY_IPA_TO_VISEME_ID",
    "DISNEY_DEFAULT_VISEME_ID",
    "DISNEY_VISEME_ID_TO_PARAMS",
    "arpabet_to_disney_viseme_id",
    "phonemes_to_disney_viseme_ids",
]

