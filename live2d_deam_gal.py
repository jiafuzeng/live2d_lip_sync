"""
live2d_deam_G.py - Live2D 模型管理器（G 模型专用）

封装 Live2D 模型相关操作，包括口型同步、表情控制等
适配 gal 模型（Resources/v3/gal）
支持基于 aeiou 的元音/口型驱动（英文文本 → viseme → ParamMouthOpenY / ParamMouthForm）
"""

import json
import os
import sys
from typing import Optional

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
import live2d.v3 as live2d
from live2d.v3 import StandardParams
from image_compat import Image
from aeiou.phoneme_viseme import LipMode, text_to_lip_units
from aeiou.phoneme_viseme import text_to_timed_visemes_fallback
from background.img_ import get_background_image_path

# MS viseme ID → (open, form) 近似映射（0.0–1.0），用于 MS_ID 模式下驱动嘴型
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

# 初始化 Live2D 日志
live2d.enableLog(True)
live2d.setLogLevel(live2d.Live2DLogLevels.LV_INFO)


def _make_pygame_window_key_macos() -> None:
    """
    macOS：让当前 Pygame 窗口成为 key window 并前置，便于直接收到按键。
    即使从终端直接运行，SDL2 创建的新窗口有时不会自动获得键盘焦点；
    对 NSWindow 调 makeKeyAndOrderFront 可提高第一次按空格就触发的概率。
    """
    if sys.platform != "darwin":
        return
    try:
        info = pygame.display.get_wm_info()
        nswindow_ptr = info.get("window") or info.get("nswindow")
        if not nswindow_ptr:
            return
        import ctypes
        from ctypes import c_void_p

        objc = ctypes.CDLL("/usr/lib/libobjc.A.dylib")
        objc.sel_registerName.restype = c_void_p
        objc.sel_registerName.argtypes = [ctypes.c_char_p]
        objc.objc_msgSend.restype = c_void_p
        objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
        sel = objc.sel_registerName(b"makeKeyAndOrderFront:")
        objc.objc_msgSend(ctypes.c_void_p(nswindow_ptr), sel, ctypes.c_void_p(0))
    except Exception:
        pass


class Live2DModelManager:
    """Live2D 模型管理器（gal 模型），封装模型相关操作"""

    # 窗口配置
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 1200

    # 动画配置
    FPS = 60  # 默认帧率

    # gal 模型资源路径
    MODEL_PATH_V3 = "v3/gal/gal.model3.json"
    #MODEL_PATH_V3 = "v3/Haru/Haru.model3.json"
    BACKGROUND_IMAGE = "RING.png"

    # 口型驱动模式（默认使用 Polly(open/form)；也可以切换为 MS viseme ID）
    LIP_MODE: LipMode = LipMode.POLLY
    #LIP_MODE: LipMode = LipMode.MS_ID

    # 口型参数名 → Live2D StandardParams 映射
    PARAM_MAP = {
        "ParamMouthOpenY": StandardParams.ParamMouthOpenY,
        "ParamMouthForm": StandardParams.ParamMouthForm,
    }

    def __init__(
        self,
        model_path: Optional[str] = None,
        display_size: Optional[tuple[int, int]] = None,
        background_path: Optional[str] = None,
        title: str = "Live2D 数字人聊天界面（gal 模型）",
    ):
        """初始化管理器并从路径加载模型"""
        if model_path is None:
            model_path = self.MODEL_PATH_V3
        if display_size is None:
            display_size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        if background_path is None:
            background_path = self.BACKGROUND_IMAGE

        # 初始化 pygame 环境
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            # 某些 macOS 环境下 CoreAudio 可能不可用；本脚本不依赖音频播放，忽略即可
            pass
        pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)
        _make_pygame_window_key_macos()

        # 初始化 Live2D 框架
        live2d.init()
        live2d.glInit()

        # 创建并加载模型
        self.model = live2d.LAppModel()

        full_path = os.path.join("Resources", model_path)
        self.model.LoadModelJson(full_path)

        self.model.Resize(*display_size)
        self.model.SetAutoBlinkEnable(True)  # 启用自动眨眼
        self.model.SetAutoBreathEnable(False)

        self.current_audio_rms = 0.0
        self.current_emotion: str | None = None
        self.clock = pygame.time.Clock()

        # 尝试从 background/img_.py 获取背景图绝对路径
        bg_abs_path = get_background_image_path()

        # 元音/口型播放：消费 list，按间隔取一条驱动嘴型，list 空则嘴型归 0
        self._timed_visemes: list[tuple[str, float, float, float, float]] = []
        self._next_consume_ticks: Optional[int] = None  # 下一帧可消费的时间点（ms）
        self._consume_interval_ms: int = 250  # 每条口型间隔（约 0.25s）

        # 从 model3.json 解析表情列表（FileReferences.Expressions[].Name）
        self.available_expressions = self._parse_expressions_from_model_json(full_path)
        print(f"✓ G 模型已加载，可用表情: {self.available_expressions}")

        # 加载背景图片
        try:
            self.background = Image(bg_abs_path) if bg_abs_path else None
        except Exception:
            self.background = None

    def _parse_expressions_from_model_json(self, model_json_path: str) -> list[str]:
        """从 model3.json 解析 FileReferences.Expressions 中的 Name 列表"""
        try:
            with open(model_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            expressions = data.get("FileReferences", {}).get("Expressions", [])
            return [e["Name"] for e in expressions if e.get("Name")]
        except Exception as e:
            print(f"⚠️ 解析 model3.json 表情失败: {e}")
            return []

    def draw_background(self) -> None:
        """绘制背景图片"""
        if self.background:
            self.background.Draw()

    def trigger_expression_from_text(self, text: str) -> None:
        """根据文本触发表情"""
        text_lower = text.lower()
        for name in self.available_expressions:
            if name.lower() in text_lower:
                self.set_expression(name)
                return
        self.set_random_expression()

    def update_lip_params(self, params: dict) -> None:
        """根据口型参数更新嘴型（ParamMouthOpenY、ParamMouthForm 等），与 live2d_manager 一致"""
        for key, value in params.items():
            if key in self.PARAM_MAP and isinstance(value, (int, float)):
                try:
                    result = round(float(value), 1)
                    #print(f"设置口型参数: {key}={result}")
                    self.model.SetParameterValue(self.PARAM_MAP[key], result)
                except Exception:
                    print(f"设置口型参数失败: {key}={value}")

    # 之前的元音参数驱动先保留为占位（当前恢复为通用 ParamMouthOpenY/ParamMouthForm 驱动）
    def _reset_vowel_params(self) -> None:
        """占位：当前口型归零在主循环里通过 update_lip_params 完成"""
        return

    def start_viseme_playback(self, text: str, sec_per_viseme: float = 0.08) -> bool:
        """
        使用 aeiou 将英文文本转为带时间轴的口型序列并开始播放。
        返回 True 表示成功启动，False 表示未安装 aeiou 或文本无有效口型。
        """
        try:
            self._timed_visemes = text_to_lip_units(text, mode=self.LIP_MODE)
            
            if not self._timed_visemes:
                return False
            self._next_consume_ticks = pygame.time.get_ticks()
            return True
        except Exception:
            return False

    def update_emotion(self, emotion: str | None) -> None:
        """更新表情（只有当表情改变时才设置）"""
        if emotion == self.current_emotion:
            return

        self.current_emotion = emotion
        if emotion:
            self.set_expression(emotion)

    def update(self) -> None:
        """更新模型动画"""
        self.model.Update()

    def draw(self) -> None:
        """绘制模型"""
        self.model.Draw()

    def handle_drag(self, x: int, y: int) -> None:
        """处理鼠标拖拽（使用屏幕像素坐标，与主聊天界面保持一致）"""
        self.model.Drag(x, y)

    def tick(self, fps: int = None) -> None:
        """控制帧率"""
        self.clock.tick(fps if fps is not None else self.FPS)

    def set_expression(self, expression_name: str) -> None:
        """设置表情"""
        if expression_name in self.available_expressions:
            try:
                self.model.SetExpression(expression_name)
            except Exception as e:
                print(f"设置表情失败: {e}")
        else:
            print(f"未知表情: {expression_name}")

    def reset_all_expressions(self) -> None:
        """重置所有表情"""
        try:
            self.model.ResetExpression()
        except Exception as e:
            print(f"重置表情失败: {e}")

    def set_random_expression(self) -> None:
        """随机设置一个表情"""
        try:
            self.model.SetRandomExpression()
        except Exception:
            if self.available_expressions:
                import random

                self.set_expression(random.choice(self.available_expressions))

    def play_idle_motion(self, priority: int = 300) -> None:
        """播放待机动作"""
        try:
            self.model.StartRandomMotion("Idle", priority=priority)
        except Exception:
            pass

    def play_tap_body_motion(self, priority: int = 3) -> None:
        """播放点击身体动作"""
        try:
            self.model.StartRandomMotion("TapBody", priority=priority)
        except Exception:
            pass

    def cleanup(self) -> None:
        """清理资源"""
        live2d.dispose()
        pygame.quit()


if __name__ == "__main__":
    """
    简单的本地调试入口：
    - 启动一个窗口渲染 G 模型
    - 支持关闭窗口退出、鼠标左键拖拽
    - 元音驱动口型：按 [空格] 播放示例句口型（依赖 aeiou + cmudict）
    """
    manager = Live2DModelManager()
    running = True

    manager.play_idle_motion()

    manager.LIP_MODE = LipMode.POLLY
    #manager.LIP_MODE = LipMode.MS_ID

    # 尝试加载 aeiou，成功后自动播放一句示例口型
    demo_sentence = "Hello, nice to meet you!"
    # 记录上一次成功触发空格播放口型的时间戳（ms）
    last_space_trigger_ticks = 0
    # 空格触发间隔（ms）：避免长按空格时过于频繁地重复触发
    SPACE_COOLDOWN_MS = 400

    while running:
        now_ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    manager.handle_drag(*pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # 满足其一即触发：本次非长按重复，或距上次触发已过 cooldown（避免误过滤首次按键）
                is_repeat = getattr(event, "repeat", False)
                cooldown_ok = (now_ticks - last_space_trigger_ticks) >= SPACE_COOLDOWN_MS
                if (not is_repeat) or cooldown_ok:
                    if manager.start_viseme_playback(demo_sentence):
                        last_space_trigger_ticks = now_ticks
                        print(f"  播放口型: {demo_sentence!r}")
                    else:
                        print("  口型未启动（请安装: pip install cmudict）")

        # 消费 list：有数据且到点则取一条更新嘴型，list 空则嘴型归 0
        now = pygame.time.get_ticks()
        if manager._timed_visemes and manager._next_consume_ticks is not None and now >= manager._next_consume_ticks:
            item = manager._timed_visemes.pop(0)

            # Polly 模式：item 带有 label/open/form
            if manager.LIP_MODE == LipMode.POLLY and "label" in item:
                label = str(item.get("label", "") or "")
                open_val = float(item.get("open", 0.0))
                form_val = float(item.get("form", 0.0))

                if False:
                    # 更精细的缩放：近似按长/短/非重读元音调整嘴巴开合
                    v = label.lower()
                    long_vowels = ("a", "i", "u", "o")      # 对应 AY/IY/UW/OW 等长元音
                    mid_vowels = ("e",)                    # 对应 AE/EH/IH 等中等开口
                    reduced_vowels = ("@",)                # 对应 AH0/AX/ER0 等非重读

                    if v in long_vowels:
                        open_scaled = max(0.5, min(1.0, open_val * 1.3))
                    elif v in mid_vowels:
                        open_scaled = max(0.3, min(0.8, open_val * 1.0))
                    elif v in reduced_vowels:
                        open_scaled = min(0.4, open_val * 0.7)
                    else:
                        open_scaled = min(0.35, open_val * 0.5)
                else:
                    open_scaled = open_val

                print(f"  播放口型: {label}, {open_scaled:.1f}, {form_val:.1f}")
                manager.update_lip_params({
                    "ParamMouthOpenY": open_scaled,
                    "ParamMouthForm": form_val,
                })

            # MS viseme ID 模式：item 只有 id，可在这里自定义 id→张嘴映射
            elif manager.LIP_MODE == LipMode.MS_ID and "id" in item:
                vid = int(item.get("id", 0))
                base_open, base_form = MS_VISEME_ID_TO_PARAMS.get(vid, (0.3, 0.0))
                print(f"  播放 MS viseme ID: {vid}, open={base_open:.1f}, form={base_form:.1f}")
                manager.update_lip_params({
                    "ParamMouthOpenY": base_open,
                    "ParamMouthForm": base_form,
                })

            manager._next_consume_ticks = now + manager._consume_interval_ms
            if not manager._timed_visemes:
                manager._next_consume_ticks = None
                # 播放完口型后只归零一次
                manager.update_lip_params({"ParamMouthOpenY": 0.0, "ParamMouthForm": 0.0})
        elif not manager._timed_visemes:
            manager._next_consume_ticks = None

        manager.update()
        manager.draw_background()
        manager.draw()
        pygame.display.flip()
        manager.tick()

    manager.cleanup()

