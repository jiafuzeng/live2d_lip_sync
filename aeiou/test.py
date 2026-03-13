from __future__ import annotations

"""
简单命令行小工具：把英文文本转换成口型（viseme）参数并以 JSON 打印出来。

用法（在仓库根目录）：
  uv run python test/aeiou/test.py "Hello, nice to meet you!"
或直接运行后按提示输入一行英文。
"""

import json
import sys

from phoneme_viseme import text_to_visemes


def run(text: str) -> None:
    phonemes, visemes = text_to_visemes(text)
    print("=== Input text ===")
    print(text)
    print("\n=== CMU phonemes (ARPAbet) ===")
    print(" ".join(phonemes) if phonemes else "[empty]")

    print("\n=== Visemes (label, open, form) ===")
    for label, open_, form in visemes:
        print(f"{label:>2}  open={open_: .3f}  form={form: .3f}")

    # 与生产代码中的 payload 结构保持一致，便于前端 / Live2D 复用
    payload = {
        "visemes": [
            {"label": label, "open": open_, "form": form}
            for (label, open_, form) in visemes
        ]
    }
    print("\n=== JSON payload (for Live2D) ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("请输入一行英文文本（回车使用默认示例）: ").strip()
        if not text:
            text = "Hello, nice to meet you!"
            print(f"使用默认文本: {text}")
    run(text)
