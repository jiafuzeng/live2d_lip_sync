# 如何查找 Groups 中 Ids 字段可用的参数名称

在 `Haru.model3.json` 的 `Groups` 部分，`Ids` 字段需要填入参数 ID。本文档介绍如何查找这些参数 ID。

---

## 📋 方法一：查看 `Haru.cdi3.json` 文件（推荐）

**最直接的方法**：查看 `Haru.cdi3.json` 文件中的 `Parameters` 数组。

### 文件位置
```
Resources/v3/Haru/Haru.cdi3.json
```

### 查看方式

打开 `Haru.cdi3.json` 文件，找到 `Parameters` 数组，每个参数对象都包含 `Id` 字段：

```json
{
    "Version": 3,
    "Parameters": [
        {
            "Id": "ParamAngleX",        // ← 这就是参数 ID
            "GroupId": "ParamGroupFace",
            "Name": "角度 X"
        },
        {
            "Id": "ParamAngleY",         // ← 参数 ID
            "GroupId": "ParamGroupFace",
            "Name": "角度 Y"
        },
        {
            "Id": "ParamMouthForm",      // ← 参数 ID
            "GroupId": "ParamGroupMouth",
            "Name": "口　変形"
        },
        {
            "Id": "ParamEyeForm",        // ← 参数 ID
            "GroupId": "ParamGroupEyes",
            "Name": "眼　変形"
        }
        // ... 更多参数
    ]
}
```

### Haru 模型的所有参数 ID 列表

根据 `Haru.cdi3.json` 文件，以下是所有可用的参数 ID：

#### 面部参数（Face）
- `ParamAngleX` - 角度 X
- `ParamAngleY` - 角度 Y
- `ParamAngleZ` - 角度 Z
- `ParamTere` - 照れ（害羞）
- `ParamFaceForm` - 顔の拡縮（脸部缩放）

#### 眼睛参数（Eyes）
- `ParamEyeLOpen` - 左目　開閉（左眼开合）
- `ParamEyeLSmile` - 左目　笑顔（左眼笑容）
- `ParamEyeROpen` - 右目　開閉（右眼开合）
- `ParamEyeRSmile` - 右目　笑顔（右眼笑容）
- `ParamEyeForm` - 眼　変形（眼睛变形）
- `ParamEyeBallForm` - 目玉　収縮（眼球收缩）
- `ParamTear` - 涙（眼泪）
- `ParamEyeBallX` - 目玉 X（眼球 X）
- `ParamEyeBallY` - 目玉 Y（眼球 Y）

#### 眉毛参数（Brows）
- `ParamBrowLY` - 左眉　上下（左眉上下）
- `ParamBrowRY` - 右眉　上下（右眉上下）
- `ParamBrowLX` - 左眉　左右（左眉左右）
- `ParamBrowRX` - 右眉　左右（右眉左右）
- `ParamBrowLAngle` - 左眉　角度（左眉角度）
- `ParamBrowRAngle` - 右眉　角度（右眉角度）
- `ParamBrowLForm` - 左眉　変形（左眉变形）
- `ParamBrowRForm` - 右眉　変形（右眉变形）

#### 嘴巴参数（Mouth）
- `ParamMouthForm` - 口　変形（嘴巴变形）
- `ParamMouthOpenY` - 口　開閉（嘴巴开合）

#### 身体参数（Body）
- `ParamScarf` - スカーフ揺れ（围巾摆动）
- `ParamBodyAngleX` - 体の回転　X（身体旋转 X）
- `ParamBodyAngleY` - 体の回転　Y（身体旋转 Y）
- `ParamBodyAngleZ` - 体の回転　Z（身体旋转 Z）
- `ParamBodyUpper` - 上体（上半身）
- `ParamBreath` - 呼吸（呼吸）
- `ParamBustY` - 胸　揺れ（胸部摆动）

#### 手臂参数（Arms）
- `ParamArmLA` - 左腕 A（左臂 A）
- `ParamArmRA` - 右腕 A（右臂 A）
- `ParamArmLB` - 左腕 B（左臂 B）
- `ParamArmRB` - 右腕 B（右臂 B）
- `ParamHandChangeR` - 右手切替（右手切换）
- `ParamHandAngleR` - 右手首角度（右手腕角度）
- `ParamHandDhangeL` - 左手切替（左手切换）
- `ParamHandAngleL` - 左手首角度（左手腕角度）

#### 头发参数（Hair）
- `ParamHairFront` - 髪揺れ　前（前发摆动）
- `ParamHairSide` - 髪揺れ　横（侧发摆动）
- `ParamHairBack` - 髪揺れ　後（后发摆动）

---

## 💻 方法二：通过代码获取（运行时）

在程序运行时，可以通过代码获取所有参数信息。

### 代码示例

```python
# 在 main.py 中已有此代码（第 145-149 行）
for i in range(model.GetParameterCount()):
    param = model.GetParameter(i)
    print(f"参数 ID: {param.id}")
    print(f"  类型: {param.type}")
    print(f"  当前值: {param.value}")
    print(f"  范围: [{param.min}, {param.max}]")
    print(f"  默认值: {param.default}")
    print()
```

### 输出示例

```
参数 ID: ParamAngleX
  类型: 0
  当前值: 0.0
  范围: [-30.0, 30.0]
  默认值: 0.0

参数 ID: ParamEyeLOpen
  类型: 0
  当前值: 1.0
  范围: [0.0, 1.0]
  默认值: 1.0

参数 ID: ParamMouthForm
  类型: 0
  当前值: 0.0
  范围: [-1.0, 1.0]
  默认值: 0.0
...
```

### 提取所有参数 ID

```python
# 获取所有参数 ID 列表
param_ids = []
for i in range(model.GetParameterCount()):
    param = model.GetParameter(i)
    param_ids.append(param.id)

# 打印所有参数 ID
print("所有参数 ID:")
for param_id in param_ids:
    print(f"  - {param_id}")

# 保存到文件
with open("param_ids.txt", "w", encoding="utf-8") as f:
    for param_id in param_ids:
        f.write(f"{param_id}\n")
```

---

## 📚 方法三：查看标准参数类

查看 `StandardParams` 类中定义的标准参数名称。

### 文件位置
```
venv/lib/python3.13/site-packages/live2d/v3/params.py
```

### 标准参数列表

```python
class StandardParams:
    ParamAngleX = "ParamAngleX"
    ParamAngleY = "ParamAngleY"
    ParamAngleZ = "ParamAngleZ"
    ParamEyeLOpen = "ParamEyeLOpen"
    ParamEyeLSmile = "ParamEyeLSmile"
    ParamEyeROpen = "ParamEyeROpen"
    ParamEyeRSmile = "ParamEyeRSmile"
    ParamEyeBallX = "ParamEyeBallX"
    ParamEyeBallY = "ParamEyeBallY"
    ParamEyeBallForm = "ParamEyeBallForm"
    ParamBrowLY = "ParamBrowLY"
    ParamBrowRY = "ParamBrowRY"
    ParamBrowLX = "ParamBrowLX"
    ParamBrowRX = "ParamBrowRX"
    ParamBrowLAngle = "ParamBrowLAngle"
    ParamBrowRAngle = "ParamBrowRAngle"
    ParamBrowLForm = "ParamBrowLForm"
    ParamBrowRForm = "ParamBrowRForm"
    ParamMouthForm = "ParamMouthForm"
    ParamMouthOpenY = "ParamMouthOpenY"
    ParamCheek = "ParamCheek"
    ParamBodyAngleX = "ParamBodyAngleX"
    ParamBodyAngleY = "ParamBodyAngleY"
    ParamBodyAngleZ = "ParamBodyAngleZ"
    ParamBreath = "ParamBreath"
    ParamArmLA = "ParamArmLA"
    ParamArmRA = "ParamArmRA"
    ParamArmLB = "ParamArmLB"
    ParamArmRB = "ParamArmRB"
    ParamHandL = "ParamHandL"
    ParamHandR = "ParamHandR"
    ParamHairFront = "ParamHairFront"
    ParamHairSide = "ParamHairSide"
    ParamHairBack = "ParamHairBack"
    ParamHairFluffy = "ParamHairFluffy"
    ParamShoulderY = "ParamShoulderY"
    ParamBustX = "ParamBustX"
    ParamBustY = "ParamBustY"
    ParamBaseX = "ParamBaseX"
    ParamBaseY = "ParamBaseY"
```

**注意**：`StandardParams` 只包含标准参数，模型可能有自定义参数，这些参数不会出现在 `StandardParams` 中。

---

## 🎯 实际应用示例

### 示例 1：创建 FaceExpression 组

根据参数列表，可以创建如下组：

```json
{
    "Target": "Parameter",
    "Name": "FaceExpression",
    "Ids": [
        "ParamMouthForm",    // 嘴巴变形
        "ParamEyeForm"       // 眼睛变形
    ]
}
```

### 示例 2：创建完整面部表情组

```json
{
    "Target": "Parameter",
    "Name": "FullFaceExpression",
    "Ids": [
        "ParamMouthForm",      // 嘴巴变形
        "ParamMouthOpenY",      // 嘴巴开合
        "ParamEyeForm",        // 眼睛变形
        "ParamEyeLOpen",       // 左眼开合
        "ParamEyeROpen",       // 右眼开合
        "ParamBrowLForm",      // 左眉变形
        "ParamBrowRForm"       // 右眉变形
    ]
}
```

### 示例 3：创建身体动作组

```json
{
    "Target": "Parameter",
    "Name": "BodyMotion",
    "Ids": [
        "ParamBodyAngleX",     // 身体旋转 X
        "ParamBodyAngleY",     // 身体旋转 Y
        "ParamBodyAngleZ",     // 身体旋转 Z
        "ParamBodyUpper"       // 上半身
    ]
}
```

---

## ⚠️ 注意事项

### 1. 参数 ID 必须存在

- ✅ **必须使用模型中实际存在的参数 ID**
- ❌ **不能随意编造参数 ID**
- 如果使用不存在的参数 ID，程序可能无法正常工作

### 2. 参数 ID 区分大小写

- `ParamMouthForm` ✅ 正确
- `parammouthform` ❌ 错误（大小写不匹配）

### 3. 不同模型参数不同

- 每个 Live2D 模型的参数可能不同
- Haru 模型的参数列表可能与其他模型不同
- 建议为每个模型单独查看参数列表

### 4. 参数分组是逻辑分组

- `Groups` 中的分组是**逻辑分组**，用于程序批量操作
- 不影响参数的实际功能
- 一个参数可以属于多个组（虽然不常见）

---

## 🔍 快速查找技巧

### 技巧 1：使用文本编辑器搜索

在 `Haru.cdi3.json` 文件中：
1. 按 `Ctrl+F`（或 `Cmd+F`）打开搜索
2. 搜索 `"Id": "Param` 查找所有参数 ID
3. 或者搜索特定关键词，如 `"ParamMouth"` 查找所有嘴巴相关参数

### 技巧 2：使用命令行提取

```bash
# 提取所有参数 ID
grep -o '"Id": "[^"]*"' Haru.cdi3.json | grep Param | sed 's/"Id": "//g' | sed 's/"//g' > param_ids.txt
```

### 技巧 3：使用 Python 脚本提取

```python
import json

# 读取 cdi3.json 文件
with open("Haru.cdi3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 提取所有参数 ID
param_ids = [param["Id"] for param in data["Parameters"]]

# 打印参数 ID
print("所有参数 ID:")
for param_id in sorted(param_ids):
    print(f"  - {param_id}")

# 按类别分组
categories = {
    "Face": [p for p in param_ids if "Face" in p or "Angle" in p],
    "Eyes": [p for p in param_ids if "Eye" in p],
    "Brows": [p for p in param_ids if "Brow" in p],
    "Mouth": [p for p in param_ids if "Mouth" in p],
    "Body": [p for p in param_ids if "Body" in p],
    "Arms": [p for p in param_ids if "Arm" in p or "Hand" in p],
    "Hair": [p for p in param_ids if "Hair" in p]
}

for category, params in categories.items():
    if params:
        print(f"\n{category}:")
        for param in params:
            print(f"  - {param}")
```

---

## 📝 总结

查找参数 ID 的三种方法：

1. **查看 `Haru.cdi3.json`**（最推荐）
   - 直接查看文件中的 `Parameters` 数组
   - 每个参数的 `Id` 字段就是参数 ID

2. **通过代码获取**（运行时）
   - 使用 `model.GetParameterCount()` 和 `model.GetParameter(i)`
   - 获取 `param.id` 即可

3. **查看 `StandardParams` 类**（标准参数）
   - 只包含标准参数，可能不完整

**最佳实践**：
- 直接查看 `Haru.cdi3.json` 文件获取完整的参数列表
- 使用代码验证参数是否存在
- 确保参数 ID 拼写正确（区分大小写）

---

**相关文档**：
- `Haru.model3.json.README.md` - 配置文件详解
- `目录结构说明.md` - 文件结构说明

