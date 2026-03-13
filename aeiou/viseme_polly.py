"""
Amazon Polly 口型（viseme）标准相关工具。

本文件独立实现了 Polly 相关的：
- IPA → Polly viseme 名称 映射
- Polly viseme → (open, form) 口型参数映射
- ARPAbet → 上述两种映射的桥接
- 对口型序列的平滑处理
"""

from __future__ import annotations

import re
from typing import List, Tuple

# IPA → Polly viseme 名称
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

# ARPAbet → IPA 映射（简化版，只保留 Polly 映射用到的）
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
    """ARPAbet 符号（可带数字重音）转 IPA。"""
    raw = arpabet.strip().upper()
    if raw in ARPABET_TO_IPA:
        return ARPABET_TO_IPA[raw]
    key = re.sub(r"\d", "", raw).upper()
    return ARPABET_TO_IPA.get(key, key.lower() if key else "ə")


def arpabet_to_polly_viseme(arpabet: str) -> str:
    """ARPAbet → Amazon Polly Viseme 名称。"""
    ipa = arpabet_to_ipa(arpabet)
    for seq in ("aɪ", "aʊ", "eɪ", "oʊ", "ɔɪ", "tʃ", "dʒ"):
        if ipa == seq or seq in ipa:
            return POLLY_IPA_TO_VISEME.get(seq, POLLY_DEFAULT_VISEME)
    return POLLY_IPA_TO_VISEME.get(ipa, POLLY_DEFAULT_VISEME)


def phonemes_to_polly_visemes(phonemes: list[str]) -> list[str]:
    """音素列表（ARPAbet，可带空格）→ Polly viseme 名称列表。"""
    out: list[str] = []
    for p in phonemes:
        if p == " " or not p.strip():
            continue
        out.append(arpabet_to_polly_viseme(p))
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
    """
    if not visemes:
        return []
    out: list[tuple[str, float, float]] = []
    last_open, last_form = visemes[0][1], visemes[0][2]
    for label, target_open, target_form in visemes:
        alpha = attack_alpha if target_open > last_open else release_alpha
        last_open += alpha * (target_open - last_open)
        last_form += alpha * (target_form - last_form)
        out.append((label, round(last_open, 4), round(last_form, 4)))
    return out


__all__ = [
    "POLLY_IPA_TO_VISEME",
    "POLLY_VISEME_TO_MOUTH",
    "POLLY_DEFAULT_VISEME",
    "POLLY_DEFAULT_MOUTH",
    "ARPABET_TO_IPA",
    "arpabet_to_ipa",
    "arpabet_to_polly_viseme",
    "phonemes_to_polly_visemes",
    "phonemes_to_visemes",
    "smooth_visemes",
]

