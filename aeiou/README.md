aeiou: 英文文本转口型（viseme）小工具
=====================================

这个小项目提供了一些把英文文本转换成口型（viseme）参数的工具函数，并带有一个简单的命令行 demo (`test.py`)。

### 运行环境

- Python 3.9 及以上
- 能访问 PyPI 安装依赖

### 安装依赖

项目本身只有一个第三方依赖：`cmudict`（CMU Pronouncing Dictionary）。

下面给几种常见的安装方式，根据你当前环境选择其一即可。

#### 方式一：使用系统 Python（推荐）

macOS 上通常有 `python3`，可以直接用：

```bash
python3 -m pip install cmudict
```

如果提示 `pip` / `pip3` 不存在，可以先：

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install cmudict
```

#### 方式二：使用 uv + 虚拟环境

如果你使用 `uv`，建议先在项目里创建一个虚拟环境，再安装依赖：

```bash
uv venv .venv          # 创建虚拟环境（只需执行一次）
source .venv/bin/activate  # 激活虚拟环境
uv pip install cmudict
```

如果你不想建虚拟环境，也可以直接装到系统环境（不太推荐，但有时方便）：

```bash
uv pip install --system cmudict
```

安装成功后，再运行任何导入 `phoneme_viseme` 的代码就不会再报「未检测到 cmudict 包」的错误。

### 运行命令行 demo

在项目根目录下运行：

```bash
python test.py "Hello, nice to meet you!"
```

或者直接运行后按提示输入一行英文文本：

```bash
python test.py
```

- 输入非空英文文本：程序会把它转换成音素和 viseme，并在终端打印结果和 JSON payload。
- 直接按回车：会自动使用默认示例文本 `Hello, nice to meet you!`。

如果你已经安装并习惯使用 `uv`，也可以：

```bash
uv run python test.py "Hello, nice to meet you!"
```

### 终端输出示例说明

当你运行：

```bash
python test.py "Hello, nice to meet you"
```

会看到类似这样的输出（已简化）：

```text
=== Input text ===
Hello, nice to meet you

=== CMU phonemes (ARPAbet) ===
HH AH0 L OW1   N AY1 S   T UW1   M IY1 T   Y UW1

=== Visemes (label, open, form) ===
 k  open= 0.400  form= 0.000
 @  open= 0.490  form= 0.090
 ...

=== JSON payload (for Live2D) ===
{
  "visemes": [
    { "label": "k", "open": 0.4, "form": 0.0 },
    { "label": "@", "open": 0.49, "form": 0.09 },
    ...
  ]
}
```

- **Input text**：你输入的原始英文句子。
- **CMU phonemes (ARPAbet)**：用 CMU 词典把句子拆成的 ARPAbet 音素序列，例如 `HH AH0 L OW1 ...`。
- **Visemes (label, open, form)**：将音素序列映射并平滑后得到的口型帧列表：
  - **label**：一个简单的口型 / 嘴形类别标签（例如 `k`、`@`、`E` 等），不是原始音素，而是已经聚类后的 viseme 名称；
  - **open**：嘴巴张开的程度，范围大致在 \[0.0, 1.0]，数值越大表示张嘴越大；
  - **form**：嘴型的「扁/圆」程度，数值越大通常表示更「扁平」或收紧的嘴形，可直接用来驱动 Live2D 的 `ParamMouthForm` 等参数。
- **JSON payload (for Live2D)**：将上述口型序列转成方便前端 / Live2D 使用的 JSON 结构：
  - `visemes` 是一个数组，每个元素对应一帧口型，包含 `label`、`open`、`form`；
  - 前端可以按顺序播放这些帧，并把 `open`、`form` 绑定到模型的对应参数，实现简单的口型联动。

### 在你自己的项目中使用

你可以直接复制 `phoneme_viseme.py` 和 `viseme_standards.py` 到自己的项目里，然后在代码中：

```python
from phoneme_viseme import text_to_visemes

phonemes, visemes = text_to_visemes("Hello, nice to meet you!")
```

记得在你的项目环境中同样安装：

```bash
pip install cmudict
```

