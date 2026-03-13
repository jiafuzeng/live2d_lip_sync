## Haru 模型配置说明（model3.json）

本目录内的 `Haru.model3.json` 是 Live2D Cubism 3+ 模型的入口配置文件。程序在 `main.py` 中通过 `model.LoadModelJson(...)` 读取它，SDK 会按该文件引用加载所有资源。下文按字段解释其作用及常见用法。

### 版本
- `Version`: `3` 表示 Cubism 3 及以上格式。

### FileReferences：资源清单（路径相对本文件所在目录）
- `Moc`: 核心模型数据（网格、骨骼、变形器）。
- `Textures`: 贴图列表，支持多张（如 2048x2048）。可用于换装或分块贴图。
- `Physics`: 物理配置，控制头发/衣物的重力、弹性、阻尼。
- `Pose`: 姿势与部件关联（如左右手、左右眼联动）。
- `DisplayInfo`: 画布尺寸、原点、像素密度等显示元数据。
- `Expressions`: 表情列表，每个表情文件保存一组参数值（眼睛、嘴角等）。
  - 代码调用：`model.SetExpression("F01")` 或 `model.SetRandomExpression()`。
- `Motions`: 动作分组（如 `Idle` 待机、`TapBody` 点击身体触发）。
  - 支持 `FadeInTime`/`FadeOutTime` 平滑切换。
  - `Sound` 可选，若有音频需在程序侧实现播放逻辑。
  - 代码调用：`model.StartRandomMotion("Idle", priority)` 或 `model.StartRandomMotion("TapBody", priority)`。
- `UserData`: 自定义元数据（版权、作者、标签等），按需扩展。

### Groups：参数分组
- `EyeBlink`: 眨眼参数（如 `ParamEyeLOpen`、`ParamEyeROpen`），可由 SDK 自动眨眼或手动设置。
- `LipSync`: 口型同步参数（如 `ParamMouthOpenY`），可用音频 RMS 驱动。
- 代码示例：`model.SetParameterValue(StandardParams.ParamMouthOpenY, value)`。

### HitAreas：可交互区域
- 例如 `Head`、`Body`。配合 `model.HitPart(x, y)` 检测点击/悬停命中部件。
- 可按命中的区域触发不同动作或效果。

### 代码中的典型交互流程（参见 `main.py`）
1) 加载模型：`model.LoadModelJson(path)` → SDK 自动加载上面引用的 moc、纹理、物理、表情、动作等。
2) 表情：点击等事件中调用 `model.SetRandomExpression()` 切换表情。
3) 动作：在待机场景用 `StartRandomMotion("Idle")`；点击事件可用 `StartRandomMotion("TapBody")`。
4) 口型同步：音频响度驱动 `ParamMouthOpenY` 实现说话效果。
5) 点击检测：`model.HitPart(x, y)` 与 HitAreas 配合，决定触发何种动作或高亮。

---

## StartRandomMotion 函数详解

### 函数签名
```python
model.StartRandomMotion(
    group: str = None,              # 动作组名称（如 "Idle"、"TapBody"）
    priority: int = None,           # 动作优先级（数值越大优先级越高）
    onStartMotionHandler: callable = None,   # 动作开始回调函数
    onFinishMotionHandler: callable = None   # 动作结束回调函数
)
```

### 1. `StartRandomMotion("Idle")` - 待机动作

**作用**：从 `Idle` 动作组中随机选择一个动作播放，通常用于模型空闲时的循环动画。

**配置说明**（在 `model3.json` 中）：
```json
"Idle": [
    {
        "File": "motions/haru_g_idle.motion3.json",
        "FadeInTime": 0.5,    // 淡入时间（秒）
        "FadeOutTime": 0.5     // 淡出时间（秒）
    },
    {
        "File": "motions/haru_g_m15.motion3.json",
        "FadeInTime": 0.5,
        "FadeOutTime": 0.5
    }
]
```

**特点**：
- `Idle` 组包含 2 个动作文件，函数会随机选择其中一个
- 通常没有关联音频（`Sound` 字段），因为待机动作是循环播放的
- `FadeInTime`/`FadeOutTime` 让动作切换更平滑，避免突兀

**使用场景**：
```python
# 程序启动时，让模型开始播放待机动作
model.StartRandomMotion("Idle", priority=300)

# 或者在模型空闲时自动循环播放
# 通常配合定时器或空闲检测逻辑使用
```

**代码示例**（来自 `main.py` 第 188 行）：
```python
# 启动随机动作（TapBody 组，优先级 300）
fc = None  # 完成回调
sc = None  # 开始回调
model.StartRandomMotion("TapBody", 300, sc, fc)
```

---

### 2. `StartRandomMotion("TapBody")` - 点击触发动作

**作用**：从 `TapBody` 动作组中随机选择一个动作播放，通常用于用户点击模型身体时的交互反馈。

**配置说明**（在 `model3.json` 中）：
```json
"TapBody": [
    {
        "File": "motions/haru_g_m26.motion3.json",
        "FadeInTime": 0.5,
        "FadeOutTime": 0.5,
        "Sound": "sounds/haru_talk_13.wav"  // 关联的音频文件
    },
    // ... 共 4 个动作，每个都有不同的音频
]
```

**TapBody 组包含的 4 个动作详解**：

| 动作文件 | 音频文件 | 动作时长 | 推测动作类型 | 说明 |
|---------|---------|---------|------------|------|
| `haru_g_m26.motion3.json` | `haru_talk_13.wav` | 4.97 秒 | **说话动作** | 模型做出说话/交流的动作，配合语音播放 |
| `haru_g_m06.motion3.json` | `haru_Info_14.wav` | 4.53 秒 | **信息介绍动作** | 模型做出介绍/说明的动作，可能包含手势 |
| `haru_g_m20.motion3.json` | `haru_normal_6.wav` | 6.03 秒 | **日常动作** | 模型做出普通/日常的互动动作，时长最长 |
| `haru_g_m09.motion3.json` | `haru_Info_04.wav` | 4.03 秒 | **信息动作** | 模型做出另一个信息/说明的动作 |

**动作命名规则**：
- `haru_g_mXX` 中的 `XX` 是动作编号（motion number）
- 编号越大不一定表示动作更复杂，只是模型制作者的文件命名顺序
- `g` 可能表示 "general"（通用）或特定分类标识

**特点**：
- `TapBody` 组包含 4 个动作文件，每次点击随机选择其中一个
- **每个动作都有关联的音频文件**（`Sound` 字段），实现动作+语音的完整交互
- 动作播放完成后会自动停止（不像 `Idle` 那样循环）
- 所有动作都设置了 0.5 秒的淡入淡出时间，确保动作切换平滑

**使用场景**：
```python
# 在鼠标点击事件中触发
if event.type == pygame.MOUSEBUTTONDOWN:
    # 设置随机表情
    model.SetRandomExpression()
    # 播放随机点击动作（会随机选择 TapBody 组中的 4 个动作之一）
    model.StartRandomMotion("TapBody", priority=3, 
                           onFinishMotionHandler=on_finish_motion_callback)
```

**如何查看具体动作内容**：
1. **运行程序**：执行 `python main.py`，程序会加载 Haru 模型
2. **点击模型身体**：在窗口中点击模型的身体部分（Body 区域）
3. **观察动作**：每次点击会随机播放上述 4 个动作之一，可以看到：
   - 模型的身体动作（挥手、点头、转身等）
   - 表情变化（配合 `SetRandomExpression()`）
   - 如果实现了音频播放，还能听到对应的语音
4. **多次点击**：连续点击可以体验不同的动作组合

**动作文件结构说明**：
- 每个 `.motion3.json` 文件包含：
  - `Meta.Duration`：动作持续时间（秒）
  - `Meta.Fps`：帧率（通常 30 FPS）
  - `Meta.Loop`：是否循环（TapBody 动作通常为 `true`，但播放一次后停止）
  - `Curves`：参数曲线数组，定义了动作过程中各个参数（角度、位置、表情等）的变化

**代码示例**（来自 `main.py` 第 212-223 行）：
```python
# 鼠标点击事件
if event.type == pygame.MOUSEBUTTONDOWN:
    x, y = pygame.mouse.get_pos()
    
    # 设置随机表情并播放随机动作
    model.SetRandomExpression()
    model.StartRandomMotion(priority=3, onFinishMotionHandler=on_finish_motion_callback)
    # 注意：这里没有指定 group，会从所有动作组中随机选择
    # 如果想指定只从 TapBody 组选择，应该写：
    # model.StartRandomMotion("TapBody", priority=3, onFinishMotionHandler=on_finish_motion_callback)
```

---

### 关键区别对比

| 特性 | `StartRandomMotion("Idle")` | `StartRandomMotion("TapBody")` |
|------|------------------------------|--------------------------------|
| **动作数量** | 2 个动作 | 4 个动作 |
| **音频支持** | 通常无音频 | 每个动作都有音频文件 |
| **播放方式** | 循环播放（待机动画） | 单次播放（交互反馈） |
| **触发时机** | 程序启动、空闲时 | 用户点击时 |
| **优先级** | 通常较低（如 300） | 通常较高（如 3，数值越小优先级越高） |
| **淡入淡出** | 0.5 秒 | 0.5 秒 |

### 优先级说明

**注意**：Live2D 的优先级是**数值越小优先级越高**！
- `priority=3` 比 `priority=300` 优先级更高
- 高优先级动作可以打断低优先级动作
- `TapBody` 使用 `priority=3` 确保用户点击时能立即响应
- `Idle` 使用 `priority=300` 作为背景动画，可以被其他动作打断

### 回调函数

```python
# 动作开始回调
def on_start_motion_callback(group: str, no: int):
    print(f"动作开始: 组={group}, 编号={no}")
    # 可以在这里播放音频（如果动作配置中有 Sound 字段）
    # audioPath = os.path.join(resources.CURRENT_DIRECTORY, "path to wav file")
    # pygame.mixer.music.load(audioPath)
    # pygame.mixer.music.play()

# 动作结束回调
def on_finish_motion_callback():
    print("动作结束")
    # 可以在这里处理动作结束后的逻辑
```

### 实际应用建议

1. **待机循环**：程序启动时调用 `StartRandomMotion("Idle", 300)`，让模型持续播放待机动画
2. **点击交互**：鼠标点击时调用 `StartRandomMotion("TapBody", 3)`，提供即时反馈
3. **音频同步**：在 `on_start_motion_callback` 中根据动作配置的 `Sound` 字段播放对应音频
4. **动作队列**：可以连续调用多个 `StartRandomMotion`，SDK 会根据优先级和淡入淡出时间自动管理动作队列

### 调试与扩展建议
- 表情/动作扩展：在 `Expressions` / `Motions` 中添加新的文件条目，并在代码中引用对应名称或分组。
- 物理/姿势调优：编辑 `Physics`/`Pose` 文件可调整晃动强度、联动关系。
- 资源路径：所有引用为相对路径，保持目录结构一致即可直接替换或新增资源。

