# -*- coding: UTF-8 -*-

import os
import time
import re
import jieba
import whisper
import tempfile
import logging
import subprocess
import speech_recognition as sr
from typing import Optional, Tuple
from pathlib import Path
from gtts import gTTS


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log/video_processing.log"), logging.StreamHandler()],
)


class 视频处理器:
    """
    视频处理核心类，提供专业级音频提取和转录功能

    特性：
    - 安全的临时文件管理
    - 音频格式自动检测
    - 多重重试机制
    - 详细的错误处理
    - 进度回调支持
    """

    def __init__(
        self,
        视频路径: str,
        语言: str = "zh",
        采样率: int = 16000,
        最大重试次数: int = 3,
        日志器: Optional[logging.Logger] = None,
    ) -> None:
        self.视频路径 = Path(视频路径)
        self.语言 = 语言
        self.采样率 = 采样率
        self.最大重试次数 = 最大重试次数
        self.logger = 日志器 or logging.getLogger(__name__)

        self.model = whisper.load_model("base")
        self.logger.info("Whisper模型加载完成")

        self.输出目录 = Path(__file__).parent.parent / "output/temp"
        self.输出目录.mkdir(parents=True, exist_ok=True)

        if not self.视频路径.exists():
            raise FileNotFoundError(f"视频文件不存在: {self.视频路径}")

        if not self.视频路径.is_file():
            raise ValueError(f"路径不是文件: {self.视频路径}")

    def 美化中文(self, 文本: str) -> str:
        """
        美化中文文本格式

        处理步骤:
        1. 规范化空格
        2. 添加适当的标点符号
        3. 分词优化
        """

        文本 = re.sub(r"\s+", "", 文本)
        文本 = re.sub(r"([。！？])", r"\1\n", 文本)
        分词文本 = " ".join(jieba.cut(文本))

        return 分词文本

    def 提取音频(
        self, 输出路径: Optional[Path] = None, 进度回调: Optional[callable] = None
    ) -> Path:
        音频路径 = 输出路径 or (self.输出目录 / f"audio_{int(time.time())}.wav")

        try:
            # 配置 ffmpeg 命令参数
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",
                "-i",
                str(self.视频路径),
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                str(self.采样率),
                "-ac",
                "1",
                "-hide_banner",
                "-loglevel",
                "error",
                str(音频路径),
            ]

            self.logger.info(f"开始提取音频: {self.视频路径.name}")

            # 启动 ffmpeg 进程
            process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            # 监控处理进度
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output and "frame=" in output and 进度回调:
                    进度回调(output)

            # 检查处理结果
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, ffmpeg_cmd)

            self.logger.info(f"成功生成音频文件: {音频路径}")
            return 音频路径

        except subprocess.CalledProcessError as e:
            self.logger.error(f"音频提取失败: {e}")
            if 音频路径.exists():
                音频路径.unlink()
            raise
        except Exception as e:
            self.logger.error(f"未知错误: {str(e)}", exc_info=True)
            if 音频路径.exists():
                音频路径.unlink()
            raise

        成功, 转录结果 = self.转录音频(音频路径)
        if 成功:
            self.logger.info(f"转录结果: {转录结果}")
            print(f"转录结果: {转录结果}")
        else:
            self.logger.warning("音频转录失败")

    def 转录音频(self, 音频路径: Path, 重试: int = 0) -> Tuple[bool, str]:
        try:
            # 使用 Whisper 进行转录
            result = self.model.transcribe(
                str(音频路径),
                language=self.语言,
                task="transcribe",
            )

            if result["text"]:
                return True, result["text"]
            return False, ""

        except Exception as e:
            if 重试 < self.最大重试次数:
                self.logger.warning(
                    f"转录失败，正在重试 ({重试+1}/{self.最大重试次数})"
                )
                return self.转录音频(音频路径, 重试 + 1)
            self.logger.error(f"转录失败: {str(e)}")
            return False, ""

    def 执行转录(self, 保留音频: bool = False) -> str:
        try:
            音频文件 = self.输出目录 / f"audio_{int(time.time())}.wav"
            音频路径 = self.提取音频(音频文件)
            成功, 结果 = self.转录音频(音频路径)

            if not 成功:
                raise RuntimeError("语音识别失败")

            美化结果: str = self.美化中文(文本=结果)

            self.logger.info(f"[v] 转录结果: {美化结果}")

            return 美化结果
        finally:
            if not 保留音频 and 音频文件.exists():
                try:
                    音频文件.unlink()
                    self.logger.info("[v] 已清理临时音频文件")
                except Exception as e:
                    self.logger.warning(f"[x] 清理文件失败: {str(e)}")

    def 文本转语音(self, 文本: str, 语言: str) -> str:
        # 创建临时目录
        临时目录 = "output/temp"
        os.makedirs(临时目录, exist_ok=True)

        # 生成临时音频文件路径
        音频路径 = os.path.join(临时目录, "tts_output.mp3")

        # 生成语音
        tts = gTTS(text=文本, lang=语言)
        tts.save(音频路径)

        return 音频路径

    def 合并视频音频(self, 视频路径: str, 音频路径: str, 输出路径: str) -> None:
        try:
            # 使用 FFmpeg 合并视频和音频
            ffmpeg_cmd = [
                "ffmpeg",
                "-i",
                str(视频路径),
                "-i",
                str(音频路径),
                "-c:v",
                "copy",  # 复制视频流，不重新编码
                "-c:a",
                "aac",  # 将音频编码为 AAC
                "-strict",
                "experimental",
                "-map",
                "0:v:0",  # 使用第一个视频流
                "-map",
                "1:a:0",  # 使用第二个音频流
                "-y",  # 覆盖已存在的文件
                str(输出路径),
            ]

            self.logger.info("开始合并视频和音频")
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            self.logger.info("视频合并完成")

        except subprocess.CalledProcessError as e:
            self.logger.error(f"合并失败: {e.stderr.decode()}")
            raise RuntimeError("视频合并失败") from e
