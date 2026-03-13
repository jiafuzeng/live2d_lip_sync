# Haru.model3.json 配置文件详解

本文档详细说明 `Haru.model3.json` 文件的结构、每个字段的含义、如何修改以及注意事项。

---

## 📋 文件概述

**文件名**：`Haru.model3.json`  
**文件类型**：JSON 配置文件  
**作用**：Live2D Cubism 3+ 模型的**入口配置文件**  
**重要性**：⭐⭐⭐⭐⭐（必需文件）

### 核心作用

这是 Live2D 模型加载时的**入口文件**，程序通过以下代码加载：

```python
model = live2d.LAppModel()
model.LoadModelJson("Resources/v3/Haru/Haru.model3.json")
```

SDK 会解析此文件，自动加载所有引用的资源文件。

---

## 📐 文件结构

```json
{
    "Version": 3,                    // 版本号
    "FileReferences": {              // 文件引用部分
        "Moc": "...",                // MOC 文件
        "Textures": [...],           // 纹理文件列表
        "Physics": "...",            // 物理配置文件
        "Pose": "...",               // 姿势配置文件
        "DisplayInfo": "...",        // 显示信息文件
        "Expressions": [...],        // 表情文件列表
        "Motions": {...},            // 动作文件分组
        "UserData": "..."            // 用户数据文件
    },
    "Groups": [...],                 // 参数组定义
    "HitAreas": [...]                // 点击区域定义
}
```

---

## 🔍 字段详解

### 1. `Version` - 版本号

```json
"Version": 3
```

**含义**：
- 指定 Live2D 模型格式版本
- `3` 表示 Cubism 3.0+ 格式
- 支持更高级的功能（物理、姿势、表情等）

**修改建议**：
- ⚠️ **不要修改**，除非你确定要升级到新版本
- 版本不匹配会导致模型无法加载

---

### 2. `FileReferences` - 文件引用部分

这是文件的核心部分，定义了模型所需的所有资源文件。

#### 2.1 `Moc` - 模型核心数据文件

```json
"Moc": "Haru.moc3"
```

**含义**：
- 指向模型的 MOC（Model Object Container）文件
- 包含模型的网格、骨骼、变形器等核心数据
- 这是模型的基础结构文件

**路径说明**：
- 相对路径，相对于 `Haru.model3.json` 所在目录
- 如果文件在同一目录，直接写文件名

**修改建议**：
- ⚠️ **不要修改**，除非你更换了模型
- 如果更换模型，确保新 MOC 文件与模型兼容

---

#### 2.2 `Textures` - 纹理贴图列表

```json
"Textures": [
    "Haru.2048/texture_00.png",
    "Haru.2048/texture_01.png"
]
```

**含义**：
- 模型的纹理贴图文件列表（数组）
- 包含模型的所有可见部分（皮肤、衣服、头发等）
- `2048` 表示纹理分辨率为 2048x2048 像素

**路径说明**：
- 相对路径，相对于 `Haru.model3.json` 所在目录
- 可以包含子目录（如 `Haru.2048/`）

**修改场景**：
- ✅ **可以添加**：添加新的纹理文件（如换装功能）
  ```json
  "Textures": [
      "Haru.2048/texture_00.png",
      "Haru.2048/texture_01.png",
      "Haru.2048/texture_02.png"  // 新增纹理
  ]
  ```
- ✅ **可以替换**：替换现有纹理文件（保持文件名不变）
- ⚠️ **注意**：确保纹理文件与 MOC 文件兼容

---

#### 2.3 `Physics` - 物理配置文件

```json
"Physics": "Haru.physics3.json"
```

**含义**：
- 物理模拟配置文件
- 定义头发、衣服等部件的物理参数（重力、弹性、阻力等）
- 让模型产生自然的晃动效果

**可选性**：
- ✅ **可选**：如果不需要物理效果，可以删除此字段
- 删除后，模型仍然可以正常显示，但不会有物理晃动效果

**修改建议**：
- 如果需要调整物理效果，编辑 `Haru.physics3.json` 文件
- 不建议直接修改此字段的路径

---

#### 2.4 `Pose` - 姿势配置文件

```json
"Pose": "Haru.pose3.json"
```

**含义**：
- 姿势联动配置文件
- 定义部件之间的联动关系（如左右手联动、左右眼联动）

**可选性**：
- ✅ **可选**：如果不需要姿势联动，可以删除此字段

**修改建议**：
- 如果需要调整联动关系，编辑 `Haru.pose3.json` 文件
- 不建议直接修改此字段的路径

---

#### 2.5 `DisplayInfo` - 显示信息文件

```json
"DisplayInfo": "Haru.cdi3.json"
```

**含义**：
- 显示信息配置文件
- 包含画布尺寸、原点位置、像素密度等显示元数据
- 提供参数的中文名称映射

**重要性**：
- ⭐⭐⭐⭐ 重要，但不删除也能运行（SDK 会使用默认值）

**修改建议**：
- 如果需要调整显示参数，编辑 `Haru.cdi3.json` 文件
- 不建议直接修改此字段的路径

---

#### 2.6 `Expressions` - 表情文件列表

```json
"Expressions": [
    {
        "Name": "F01",
        "File": "expressions/F01.exp3.json"
    },
    {
        "Name": "F02",
        "File": "expressions/F02.exp3.json"
    },
    // ... 共 8 个表情
]
```

**含义**：
- 表情文件列表（数组）
- 每个表情包含一个 `Name`（表情名称）和 `File`（文件路径）
- 程序通过 `Name` 来引用表情

**在代码中的使用**：
```python
# 通过 Name 设置表情
model.SetExpression("F01")  # 使用 Name 字段的值
model.SetRandomExpression()  # 随机选择表情
```

**修改场景**：

1. **添加新表情**：
   ```json
   "Expressions": [
       // ... 现有表情
       {
           "Name": "F09",  // 新的表情名称
           "File": "expressions/F09.exp3.json"  // 新的表情文件
       }
   ]
   ```
   然后在代码中使用：
   ```python
   model.SetExpression("F09")
   ```

2. **删除表情**：
   - 从数组中删除对应的对象
   - 确保对应的 `.exp3.json` 文件存在（如果程序需要）

3. **重命名表情**：
   - 修改 `Name` 字段（注意：代码中引用表情的地方也需要修改）

**注意事项**：
- `Name` 字段是程序引用表情的标识，建议使用有意义的名称
- `File` 路径是相对路径，相对于 `Haru.model3.json` 所在目录

---

#### 2.7 `Motions` - 动作文件分组

```json
"Motions": {
    "Idle": [
        {
            "File": "motions/haru_g_idle.motion3.json",
            "FadeInTime": 0.5,
            "FadeOutTime": 0.5
        },
        {
            "File": "motions/haru_g_m15.motion3.json",
            "FadeInTime": 0.5,
            "FadeOutTime": 0.5
        }
    ],
    "TapBody": [
        {
            "File": "motions/haru_g_m26.motion3.json",
            "FadeInTime": 0.5,
            "FadeOutTime": 0.5,
            "Sound": "sounds/haru_talk_13.wav"
        },
        // ... 更多动作
    ]
}
```

**含义**：
- 动作文件分组（对象）
- 每个键（如 `"Idle"`、`"TapBody"`）是一个动作组名称
- 每个动作组包含一个动作文件数组

**动作对象字段**：

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `File` | string | ✅ | 动作文件路径（相对路径） |
| `FadeInTime` | number | ❌ | 淡入时间（秒），默认 0 |
| `FadeOutTime` | number | ❌ | 淡出时间（秒），默认 0 |
| `Sound` | string | ❌ | 关联的音频文件路径（相对路径） |

**在代码中的使用**：
```python
# 通过动作组名称播放随机动作
model.StartRandomMotion("Idle", priority=300)      # 从 Idle 组随机选择
model.StartRandomMotion("TapBody", priority=3)     # 从 TapBody 组随机选择

# 播放指定动作组的指定动作
model.StartMotion("TapBody", 0, priority=3)  # 播放 TapBody 组的第 0 个动作
```

**修改场景**：

1. **添加新动作到现有组**：
   ```json
   "TapBody": [
       // ... 现有动作
       {
           "File": "motions/haru_g_m27.motion3.json",
           "FadeInTime": 0.5,
           "FadeOutTime": 0.5,
           "Sound": "sounds/haru_new_sound.wav"
       }
   ]
   ```

2. **创建新的动作组**：
   ```json
   "Motions": {
       "Idle": [...],
       "TapBody": [...],
       "TapHead": [  // 新的动作组
           {
               "File": "motions/haru_g_m01.motion3.json",
               "FadeInTime": 0.5,
               "FadeOutTime": 0.5
           }
       ]
   }
   ```
   然后在代码中使用：
   ```python
   model.StartRandomMotion("TapHead", priority=3)
   ```

3. **调整淡入淡出时间**：
   ```json
   {
       "File": "motions/haru_g_m26.motion3.json",
       "FadeInTime": 1.0,    // 改为 1 秒淡入
       "FadeOutTime": 0.3     // 改为 0.3 秒淡出
   }
   ```

4. **添加或修改音频**：
   ```json
   {
       "File": "motions/haru_g_m26.motion3.json",
       "FadeInTime": 0.5,
       "FadeOutTime": 0.5,
       "Sound": "sounds/new_audio.wav"  // 修改音频文件
   }
   ```

**注意事项**：
- 动作组名称（如 `"Idle"`、`"TapBody"`）是程序引用动作组的标识
- `FadeInTime`/`FadeOutTime` 让动作切换更平滑，建议设置为 0.3-1.0 秒
- `Sound` 字段是可选的，如果指定了音频文件，需要在代码中实现音频播放逻辑

---

#### 2.8 `UserData` - 用户数据文件

```json
"UserData": "Haru.userdata3.json"
```

**含义**：
- 用户自定义数据文件
- 包含模型的扩展元数据（如部件标签、自定义信息等）

**可选性**：
- ✅ **可选**：如果不需要用户数据，可以删除此字段

**修改建议**：
- 如果需要添加自定义数据，编辑 `Haru.userdata3.json` 文件
- 不建议直接修改此字段的路径

---

### 3. `Groups` - 参数组定义

```json
"Groups": [
    {
        "Target": "Parameter",
        "Name": "EyeBlink",
        "Ids": [
            "ParamEyeLOpen",
            "ParamEyeROpen"
        ]
    },
    {
        "Target": "Parameter",
        "Name": "LipSync",
        "Ids": [
            "ParamMouthOpenY"
        ]
    }
]
```

**含义**：
- 将相关的参数归类到逻辑组中
- 方便程序批量操作参数

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `Target` | string | 目标类型，通常是 `"Parameter"` |
| `Name` | string | 组名称（如 `"EyeBlink"`、`"LipSync"`） |
| `Ids` | array | 属于该组的参数 ID 列表 |

**作用**：

1. **EyeBlink 组**（眨眼组）：
   - 包含左右眼开合参数
   - SDK 的自动眨眼功能会操作这两个参数
   - 程序也可以手动控制：
     ```python
     model.SetParameterValue("ParamEyeLOpen", 0)  # 闭左眼
     model.SetParameterValue("ParamEyeROpen", 0)   # 闭右眼
     ```

2. **LipSync 组**（口型同步组）：
   - 包含嘴部张合参数
   - 程序在音频播放时通过此参数驱动口型：
     ```python
     model.SetParameterValue(StandardParams.ParamMouthOpenY, value)
     ```

**修改场景**：

1. **添加新的参数组**：
   ```json
   "Groups": [
       // ... 现有组
       {
           "Target": "Parameter",
           "Name": "FaceExpression",  // 新组名称
           "Ids": [
               "ParamMouthForm",
               "ParamEyeForm"
           ]
       }
   ]
   ```

2. **修改现有组**：
   - 添加或删除 `Ids` 数组中的参数 ID
   - 注意：确保参数 ID 在模型中存在

**注意事项**：
- `Name` 字段主要用于逻辑分组，程序通常直接使用参数 ID
- 参数 ID 必须与模型中的实际参数名称匹配

---

### 4. `HitAreas` - 点击区域定义

```json
"HitAreas": [
    {
        "Id": "HitArea",
        "Name": "Head"
    },
    {
        "Id": "HitArea2",
        "Name": "Body"
    }
]
```

**含义**：
- 定义模型的可交互区域
- 用于检测鼠标点击/悬停位置

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `Id` | string | 区域 ID（在 MOC 文件中定义） |
| `Name` | string | 区域名称（用于程序识别） |

**在代码中的使用**：
```python
# 检测点击位置
hit_part_ids = model.HitPart(x, y, False)
# 返回命中的部件 ID 列表

# 可以根据命中的区域触发不同的动作
if "Head" in hit_part_ids:
    model.StartRandomMotion("TapHead", priority=3)
elif "Body" in hit_part_ids:
    model.StartRandomMotion("TapBody", priority=3)
```

**修改场景**：

1. **添加新的点击区域**：
   ```json
   "HitAreas": [
       // ... 现有区域
       {
           "Id": "HitArea3",
           "Name": "Hand"
       }
   ]
   ```
   **注意**：`Id` 必须在 MOC 文件中定义，不能随意添加

2. **修改区域名称**：
   - 修改 `Name` 字段（不影响功能，只是方便程序识别）

**注意事项**：
- `Id` 字段必须在 MOC 文件中定义，不能随意添加
- 如果 MOC 文件中没有定义对应的 HitArea，该区域将无法检测
- `Name` 字段是程序识别的标识，建议使用有意义的名称

---

## 🛠️ 修改指南

### 修改前的准备

1. **备份原文件**：
   ```bash
   cp Haru.model3.json Haru.model3.json.bak
   ```

2. **验证 JSON 格式**：
   - 使用 JSON 验证工具检查语法
   - 确保所有引号、逗号、括号匹配

3. **测试修改**：
   - 修改后运行程序测试
   - 确保所有引用的文件都存在

### 常见修改场景

#### 场景 1：添加新表情

```json
// 在 Expressions 数组中添加
"Expressions": [
    // ... 现有表情
    {
        "Name": "F09",
        "File": "expressions/F09.exp3.json"
    }
]
```

#### 场景 2：添加新动作到现有组

```json
// 在 TapBody 数组中添加
"TapBody": [
    // ... 现有动作
    {
        "File": "motions/haru_g_m27.motion3.json",
        "FadeInTime": 0.5,
        "FadeOutTime": 0.5,
        "Sound": "sounds/new_sound.wav"
    }
]
```

#### 场景 3：创建新的动作组

```json
// 在 Motions 对象中添加新键
"Motions": {
    "Idle": [...],
    "TapBody": [...],
    "TapHead": [  // 新动作组
        {
            "File": "motions/haru_g_m01.motion3.json",
            "FadeInTime": 0.5,
            "FadeOutTime": 0.5
        }
    ]
}
```

#### 场景 4：调整淡入淡出时间

```json
{
    "File": "motions/haru_g_m26.motion3.json",
    "FadeInTime": 1.0,    // 改为 1 秒
    "FadeOutTime": 0.3    // 改为 0.3 秒
}
```

---

## ⚠️ 注意事项

### 1. 路径问题

- ✅ **使用相对路径**：所有文件路径都是相对于 `Haru.model3.json` 所在目录
- ✅ **保持目录结构**：确保引用的文件存在于指定路径
- ❌ **不要使用绝对路径**：会导致跨平台兼容性问题

### 2. JSON 格式

- ✅ **保持 JSON 格式正确**：确保所有引号、逗号、括号匹配
- ✅ **使用 UTF-8 编码**：避免中文乱码
- ❌ **不要添加注释**：标准 JSON 不支持注释（虽然很多解析器支持）

### 3. 文件引用

- ✅ **确保文件存在**：引用的所有文件必须存在
- ✅ **检查文件路径**：路径大小写敏感（Linux/Mac）
- ❌ **不要引用不存在的文件**：会导致加载失败

### 4. 版本兼容性

- ⚠️ **不要修改 Version**：除非确定要升级版本
- ⚠️ **保持格式一致**：确保所有引用的文件都是 Cubism 3 格式

### 5. 动作组名称

- ✅ **使用有意义的名称**：如 `"Idle"`、`"TapBody"`、`"TapHead"`
- ✅ **保持命名一致**：代码中引用的名称必须与此处一致
- ❌ **不要使用特殊字符**：避免空格、中文等（虽然支持，但不推荐）

---

## 🔍 调试技巧

### 1. 验证文件存在

```python
import os

model_json_path = "Resources/v3/Haru/Haru.model3.json"
base_dir = os.path.dirname(model_json_path)

# 读取 JSON 文件
import json
with open(model_json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 检查所有引用的文件是否存在
refs = config["FileReferences"]
if "Moc" in refs:
    moc_path = os.path.join(base_dir, refs["Moc"])
    print(f"MOC 文件存在: {os.path.exists(moc_path)}")

for texture in refs.get("Textures", []):
    texture_path = os.path.join(base_dir, texture)
    print(f"纹理文件存在: {os.path.exists(texture_path)} - {texture}")
```

### 2. 检查 JSON 格式

```bash
# 使用 Python 验证 JSON
python3 -m json.tool Haru.model3.json > /dev/null && echo "JSON 格式正确" || echo "JSON 格式错误"
```

### 3. 查看加载日志

```python
# 启用 Live2D 日志
live2d.enableLog(True)
live2d.setLogLevel(live2d.Live2DLogLevels.LV_DEBUG)

# 加载模型时会输出详细的加载信息
model.LoadModelJson("Resources/v3/Haru/Haru.model3.json")
```

---

## 📚 相关文档

- `README.md` - 模型使用说明
- `目录结构说明.md` - 文件结构详解
- `StartRandomMotion详解.md` - 动作播放函数详解

---

## 📝 总结

`Haru.model3.json` 是 Live2D 模型的入口配置文件，它：

1. **定义所有资源引用**：MOC、纹理、物理、姿势、表情、动作等
2. **组织动作分组**：将动作文件按功能分组（Idle、TapBody 等）
3. **定义参数组**：将相关参数归类（眨眼、口型同步等）
4. **定义交互区域**：定义可点击的区域（头部、身体等）

**修改建议**：
- ✅ 可以安全修改：表情列表、动作列表、动作组
- ⚠️ 谨慎修改：文件路径、参数组、点击区域
- ❌ 不要修改：Version 字段、核心文件引用（除非更换模型）

**最佳实践**：
- 修改前备份文件
- 修改后测试验证
- 保持 JSON 格式正确
- 确保所有引用的文件存在

---

**最后更新**：2024年  
**适用版本**：Live2D Cubism 3.0+

