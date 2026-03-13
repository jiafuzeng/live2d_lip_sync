from __future__ import annotations

"""
ARPAbet ↔ IPA 映射表。

- 独立维护 ARPABET_TO_IPA，便于 Polly / MS / Disney 等多个口型模块复用；
- 只做符号级别转换，不关心具体 viseme 映射。
"""

import re

# ARPAbet → IPA 映射（完整表）
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
    key = re.sub(r"\\d", "", raw).upper()
    return ARPABET_TO_IPA.get(key, key.lower() if key else "ə")


__all__ = ["ARPABET_TO_IPA", "arpabet_to_ipa"]

