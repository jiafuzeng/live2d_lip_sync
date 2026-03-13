"""
Microsoft Azure 22 Viseme (0–21) 标准相关工具。

本文件独立实现了 Azure 相关的：
- IPA → Viseme ID (0–21) 映射
- ARPAbet → 上述 ID 的桥接
"""

from __future__ import annotations

from typing import List

from aeiou.viseme_polly import ARPABET_TO_IPA, arpabet_to_ipa

# IPA → Microsoft viseme ID (0–21)
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

# Viseme ID → (open, form) 近似映射（0.0–1.0），用于上层驱动嘴型
MS_VISEME_ID_TO_PARAMS: dict[int, tuple[float, float]] = {
    # 0: 静音
    0: (0.0, 0.0),
    # 元音 / 双元音
    1: (0.7, -0.1),   # æ, ə, ʌ
    2: (0.9, 0.0),    # ɑ
    3: (0.7, -0.5),   # ɔ
    4: (0.6, 0.0),    # ɛ, ʊ
    5: (0.6, 0.1),    # ɝ
    6: (0.8, 0.5),    # j, i, ɪ - 扁长
    7: (0.6, -0.6),   # w, u - 圆嘴
    8: (0.7, -0.5),   # o
    9: (0.8, -0.2),   # aʊ
    10: (0.7, -0.1),  # ɔɪ
    11: (0.8, 0.2),   # aɪ
    # 辅音
    12: (0.4, 0.0),   # h
    13: (0.4, 0.2),   # r
    14: (0.5, 0.2),   # l
    15: (0.3, 0.4),   # s, z
    16: (0.35, 0.3),  # ʃ, tʃ, dʒ, ʒ
    17: (0.35, 0.2),  # ð
    18: (0.25, 0.0),  # f, v
    19: (0.3, 0.1),   # d, t, n, θ
    20: (0.25, 0.0),  # k, g, ŋ
    21: (0.2, 0.0),   # p, b, m
}


def arpabet_to_ms_viseme_id(arpabet: str) -> int:
    """ARPAbet → Microsoft Viseme ID (0-21)。"""
    ipa = arpabet_to_ipa(arpabet)
    for seq in ("aʊ", "ɔɪ", "aɪ", "oʊ", "eɪ", "tʃ", "dʒ"):
        if ipa == seq or seq in ipa:
            return MS_IPA_TO_VISEME_ID.get(seq, MS_DEFAULT_VISEME_ID)
    return MS_IPA_TO_VISEME_ID.get(ipa, MS_DEFAULT_VISEME_ID)


def phonemes_to_ms_viseme_ids(phonemes: list[str]) -> list[int]:
    """音素列表（ARPAbet）→ Microsoft viseme ID 列表。"""
    out: list[int] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        out.append(arpabet_to_ms_viseme_id(p))
    return out


__all__ = [
    "MS_IPA_TO_VISEME_ID",
    "MS_DEFAULT_VISEME_ID",
    "MS_VISEME_ID_TO_PARAMS",
    "arpabet_to_ms_viseme_id",
    "phonemes_to_ms_viseme_ids",
]

