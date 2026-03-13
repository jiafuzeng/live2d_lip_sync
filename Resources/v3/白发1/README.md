# 白发1 Live2D 模型目录结构完整说明

本文档详细说明"白发1" Live2D 模型目录中每个文件和文件夹的作用，帮助开发者理解模型资源的组织结构和使用方法。

---

## 📁 目录结构概览

```
白发1/
├── 白发1.model3.json          # 主配置文件（入口文件）
├── 白发1.moc3                  # 模型核心数据文件
├── 白发1.cdi3.json             # 显示信息配置文件
├── 白发1.physics3.json          # 物理模拟配置文件
├── 白发1.vtube.json             # VTube Studio 配置文件
├── 白发1.4096/                  # 纹理贴图文件夹（4096x4096 分辨率）
│   ├── texture_00.png
│   ├── texture_01.png
│   ├── texture_02.png
│   ├── texture_03.png
│   └── texture_04.png
├── aixin.exp3.json              # 爱心表情文件
├── haixiu.exp3.json             # 害羞表情文件
├── heilian .exp3.json           # 黑脸表情文件（注意文件名中有空格）
├── items_pinned_to_model.json   # VTube Studio 固定物品配置
└── README.md                    # 本说明文档
```

---

## 📄 核心文件说明

### 1. `白发1.model3.json` - 主配置文件（入口文件）

**作用**：这是 Live2D 模型的**入口配置文件**，程序通过 `model.LoadModelJson()` 加载此文件。

**文件内容**：
```json
{
    "Version": 3,
    "FileReferences": {
        "Moc": "白发1.moc3",
        "Textures": [
            "白发1.4096/texture_00.png",
            "白发1.4096/texture_01.png",
            "白发1.4096/texture_02.png",
            "白发1.4096/texture_03.png",
            "白发1.4096/texture_04.png"
        ],
        "Physics": "白发1.physics3.json",
        "DisplayInfo": "白发1.cdi3.json"
    },
    "Groups": [
        {
            "Target": "Parameter",
            "Name": "LipSync",
            "Ids": ["ParamEyeLOpen", "ParamEyeROpen"]
        },
        {
            "Target": "Parameter",
            "Name": "EyeBlink",
            "Ids": ["ParamEyeLOpen", "ParamEyeROpen"]
        }
    ]
}
```

**功能**：
- 定义模型版本（Version 3）
- 引用所有资源文件（MOC、纹理、物理、显示信息）
- 定义参数组（Groups）：眨眼组、口型同步组
- ⚠️ **注意**：未定义 `Expressions`（表情）和 `Motions`（动作）数组

**在代码中的使用**：
```python
model.LoadModelJson("Resources/v3/白发1/白发1.model3.json")
# SDK 会自动解析此文件并加载所有引用的资源
```

**重要性**：⭐⭐⭐⭐⭐ 这是模型加载的入口，所有其他文件都通过此文件引用。

**⚠️ 重要提示**：
- 表情文件（`aixin.exp3.json`、`haixiu.exp3.json`、`heilian .exp3.json`）**未在 model3.json 中定义**
- 如需自动加载表情，需要在 `FileReferences` 中添加 `Expressions` 数组（见下方"改进建议"）

---

### 2. `白发1.moc3` - 模型核心数据文件

**作用**：包含模型的**核心数据**，包括：
- 网格（Mesh）数据
- 骨骼（Bone）结构
- 变形器（Deformer）配置
- 参数定义

**重要性**：⭐⭐⭐⭐⭐ **必需文件**，没有此文件模型无法加载。

**文件特点**：
- 二进制格式，由 Live2D Cubism Editor 导出
- 不能直接编辑，需要通过 Cubism Editor 修改模型后重新导出

---

### 3. `白发1.4096/` - 纹理贴图文件夹

**作用**：存储模型的**外观贴图**，所有可见部分的图片。

**文件列表**：
- `texture_00.png` - 纹理 0
- `texture_01.png` - 纹理 1
- `texture_02.png` - 纹理 2
- `texture_03.png` - 纹理 3
- `texture_04.png` - 纹理 4

**特点**：
- **分辨率**：4096x4096 像素（高分辨率，适合高质量显示）
- **格式**：PNG，支持透明通道
- **数量**：5 个纹理文件（比 Haru 模型的 2 个更多，可能包含更多细节）

**用途**：
- 模型的皮肤、衣服、头发等所有可见部分
- 多个纹理可以用于：
  - 不同部件的贴图
  - 实现换装功能
  - 优化内存使用（按需加载）

**重要性**：⭐⭐⭐⭐⭐ 没有纹理，模型无法显示外观。

---

### 4. `白发1.physics3.json` - 物理模拟配置文件

**作用**：定义模型的**物理模拟参数**，控制头发、衣服等部件的自然摆动效果。

**功能**：
- 重力、阻力、弹性等物理参数
- 头发、衣服等可动部件的物理行为
- 使模型动作更加自然流畅

**重要性**：⭐⭐⭐⭐ 重要但可选，没有物理文件模型仍可正常显示，但缺少自然摆动效果。

**在 VTube Studio 中的配置**：
- `Use`: true（启用物理）
- `Live2DPhysicsFPS`: 3
- `PhysicsStrength`: 50
- `WindStrength`: 0
- `DraggingPhysicsStrength`: 10

---

### 5. `白发1.cdi3.json` - 显示信息配置文件

**作用**：定义模型的**显示元数据**，包括：
- 画布尺寸（Canvas Size）
- 原点位置（Origin）
- 像素密度（Pixels Per Unit）
- 参数列表和范围

**重要性**：⭐⭐⭐⭐ 重要，影响模型的显示位置和缩放。

---

### 6. `白发1.vtube.json` - VTube Studio 配置文件

**作用**：VTube Studio 软件的**配置文件**，包含：
- 模型在 VTube Studio 中的设置
- 参数映射配置（面部追踪、表情等）
- 快捷键配置
- 物理设置
- 表情热键配置

**内容概览**：
- **模型信息**：名称、ID、保存时间等
- **参数设置**：面部角度、眼睛、眉毛、嘴巴等参数映射
- **快捷键**：
  - `Ctrl+1`: 触发 `aixin`（爱心）表情
  - `Ctrl+2`: 触发 `haixiu`（害羞）表情
  - `Ctrl+3`: 触发 `heilian `（黑脸）表情
- **物理设置**：物理强度、平滑度等

**重要性**：⭐⭐⭐ 仅用于 VTube Studio，不影响程序代码中的使用。

---

## 🎭 表情文件说明

### 表情文件列表

| 文件名 | 表情名称 | 参数 ID | 说明 |
|--------|---------|---------|------|
| `aixin.exp3.json` | 爱心 | `Param19` | 爱心表情 |
| `haixiu.exp3.json` | 害羞 | `Param18` | 害羞表情 |
| `heilian .exp3.json` | 黑脸 | `Param17` | 黑脸/生气表情（⚠️ 注意文件名中有空格） |

### 表情文件结构

每个表情文件的结构如下：

```json
{
    "Type": "Live2D Expression",
    "Parameters": [
        {
            "Id": "Param19",    // 参数 ID（不同表情使用不同参数）
            "Value": 1,          // 参数值（0-1）
            "Blend": "Add"       // 混合模式（Add=叠加）
        }
    ]
}
```

### 表情使用方式

**在代码中使用**：
```python
# 设置表情
model.SetExpression("aixin")      # 爱心
model.SetExpression("haixiu")     # 害羞
model.SetExpression("heilian ")   # 黑脸（注意空格）

# 重置表情
model.ResetExpression()

# 随机表情
model.SetRandomExpression()
```

**⚠️ 重要提示**：
1. 表情文件**未在 model3.json 中定义**，可能需要手动加载
2. `heilian .exp3.json` 文件名中有**空格**，使用时需要注意
3. 如果 `SetExpression()` 无法工作，可能需要：
   - 手动加载表情文件
   - 或在 `model3.json` 中添加 `Expressions` 数组（见下方"改进建议"）

---

### 7. `items_pinned_to_model.json` - 固定物品配置

**作用**：VTube Studio 中固定到模型上的物品配置。

**内容**：
- 当前为空数组 `"Items": []`
- 用于存储附加到模型上的装饰物品（如帽子、眼镜等）

**重要性**：⭐⭐ 仅用于 VTube Studio，不影响程序代码。

---

## 🔍 与 Haru 模型的对比

| 项目 | 白发1 模型 | Haru 模型 |
|------|-----------|-----------|
| **纹理数量** | 5 个 | 2 个 |
| **纹理分辨率** | 4096x4096 | 2048x2048 |
| **表情数量** | 3 个 | 8 个（F01-F08） |
| **表情定义** | ❌ 未在 model3.json 中定义 | ✅ 已定义 |
| **动作文件** | ❌ 未定义 | ✅ 定义了 Idle、TapBody 等 |
| **Pose 文件** | ❌ 未定义 | ✅ 定义了 Haru.pose3.json |
| **UserData 文件** | ❌ 未定义 | ✅ 定义了 Haru.userdata3.json |

---

## 🛠️ 使用指南

### 在代码中加载模型

```python
from live2d_deam_haru import Live2DModelManager

# 创建模型管理器（会自动加载白发1模型）
model_manager = Live2DModelManager()

# 或者指定路径
model_manager = Live2DModelManager(
    model_path="v3/白发1/白发1.model3.json"
)
```

### 控制表情

```python
# 方式1：使用表情名称
model_manager.set_expression("爱心")
model_manager.set_expression("害羞")
model_manager.set_expression("黑脸")

# 方式2：使用表情 ID（直接使用文件名，注意空格）
model_manager.model.SetExpression("aixin")
model_manager.model.SetExpression("haixiu")
model_manager.model.SetExpression("heilian ")

# 重置表情
model_manager.reset_all_expressions()

# 随机表情
model_manager.set_random_expression()
```

### 键盘快捷键（pygame_deam_haru.py）

- **数字键 1**: 触发爱心表情（aixin）
- **数字键 2**: 触发害羞表情（haixiu）
- **数字键 3**: 触发黑脸表情（heilian）
- **数字键 0**: 重置所有表情
- **R 键**: 随机表情
- **C 键**: 清理所有表情
- **L 键**: 开启/关闭口型同步

---

## ⚠️ 已知问题和限制

### 1. 表情文件未在 model3.json 中定义

**问题**：表情文件（`aixin.exp3.json`、`haixiu.exp3.json`、`heilian .exp3.json`）未在 `model3.json` 的 `FileReferences.Expressions` 数组中定义。

**影响**：
- `model.GetExpressions()` 可能返回空列表
- `model.SetExpression()` 可能无法正常工作
- 需要手动加载表情文件或修改 `model3.json`

**解决方案**：见下方"改进建议"

### 2. 动作文件未定义

**问题**：`model3.json` 中未定义 `Motions` 数组。

**影响**：
- `play_idle_motion()` 和 `play_tap_body_motion()` 无法工作
- 模型无法播放动作动画

**解决方案**：如需动作功能，需要：
1. 准备动作文件（`.motion3.json`）
2. 在 `model3.json` 中添加 `Motions` 配置

### 3. 表情文件名中有空格

**问题**：`heilian .exp3.json` 文件名中有空格。

**影响**：
- 使用时需要注意空格：`"heilian "`（不是 `"heilian"`）
- 可能导致路径解析问题

**解决方案**：建议重命名文件为 `heilian.exp3.json`（去掉空格）

### 4. LipSync 组配置异常

**问题**：`LipSync` 组使用了眼睛参数（`ParamEyeLOpen`、`ParamEyeROpen`）而非嘴巴参数。

**影响**：
- 口型同步可能无法正常工作
- 通常应该使用 `ParamMouthOpenY` 等嘴巴参数

**解决方案**：检查模型参数，确认正确的口型同步参数

---

## 💡 改进建议

### 1. 在 model3.json 中添加表情定义

在 `白发1.model3.json` 的 `FileReferences` 中添加 `Expressions` 数组：

```json
{
    "Version": 3,
    "FileReferences": {
        "Moc": "白发1.moc3",
        "Textures": [...],
        "Physics": "白发1.physics3.json",
        "DisplayInfo": "白发1.cdi3.json",
        "Expressions": [
            {
                "Name": "aixin",
                "File": "aixin.exp3.json"
            },
            {
                "Name": "haixiu",
                "File": "haixiu.exp3.json"
            },
            {
                "Name": "heilian",
                "File": "heilian .exp3.json"
            }
        ]
    },
    "Groups": [...]
}
```

这样 Live2D SDK 就能自动识别和加载这些表情文件了。

### 2. 重命名表情文件（去掉空格）

建议将 `heilian .exp3.json` 重命名为 `heilian.exp3.json`，避免空格带来的问题。

### 3. 添加动作文件（可选）

如果需要动作功能：
1. 准备动作文件（`.motion3.json`）
2. 创建 `motions/` 文件夹
3. 在 `model3.json` 中添加 `Motions` 配置

---

## 📊 文件重要性总结

| 文件/文件夹 | 重要性 | 说明 |
|------------|--------|------|
| `白发1.model3.json` | ⭐⭐⭐⭐⭐ | 入口文件，必需 |
| `白发1.moc3` | ⭐⭐⭐⭐⭐ | 核心数据，必需 |
| `白发1.4096/*.png` | ⭐⭐⭐⭐⭐ | 纹理贴图，必需 |
| `白发1.cdi3.json` | ⭐⭐⭐⭐ | 显示信息，重要 |
| `白发1.physics3.json` | ⭐⭐⭐ | 物理模拟，可选 |
| `*.exp3.json` | ⭐⭐⭐⭐ | 表情文件，重要但未定义 |
| `白发1.vtube.json` | ⭐⭐ | VTube Studio 配置，仅用于 VTube Studio |
| `items_pinned_to_model.json` | ⭐ | 固定物品配置，仅用于 VTube Studio |

---

## 🔗 相关代码文件

- **模型管理器**：`live2d_deam_haru.py`
- **Pygame 界面**：`pygame_deam_haru.py`
- **模型路径**：`v3/白发1/白发1.model3.json`

---

## 📝 总结

"白发1" Live2D 模型是一个**高分辨率**（4096x4096）的 Live2D 模型，包含：

- ✅ **核心功能完整**：模型数据、纹理、物理、显示信息都已配置
- ⚠️ **表情功能**：有 3 个表情文件，但未在 `model3.json` 中定义，可能需要手动加载
- ❌ **动作功能**：未定义动作文件，无法播放动作动画
- 📦 **VTube Studio 兼容**：包含完整的 VTube Studio 配置文件

**使用建议**：
1. 如需使用表情功能，建议在 `model3.json` 中添加 `Expressions` 定义
2. 如需动作功能，需要准备动作文件并添加到配置中
3. 建议重命名 `heilian .exp3.json` 去掉空格

---

**最后更新**：2026年1月  
**适用版本**：Live2D Cubism 3.0+  
**模型版本**：白发1 v1.0
