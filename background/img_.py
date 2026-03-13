from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
RING_NAME = "RING.png"


def get_background_image_path() -> Optional[str]:
    """
    返回当前目录下名为 RING.png 的背景图片绝对路径。
    如果文件不存在，则返回 None。
    """
    img_path = BASE_DIR / RING_NAME
    if img_path.is_file():
        return str(img_path.resolve())
    return None

