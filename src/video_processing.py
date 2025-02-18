import os
import time
import whisper
import moviepy.editor as mp
import ffmpeg


class VideoProcessing:
    """视频处理类，用于视频转录功能"""

    def __init__(self, video_path: str, language: str = "zh") -> None:
        """
        初始化视频处理类
        参数:
            video_path: 视频文件路径
            language: 转录语言，默认为中文
        """
        super(VideoProcessing, self).__init__()

        self.video_path = video_path
        self.language = language
        # 初始化Whisper模型，使用base模型以平衡性能和准确度
        self.model = whisper.load_model("base")

    def transcribe_video(self, video_path) -> str:
        # 设置临时音频文件路径
        audio_path = "../temp/temp_audio.wav"

        try:
            # 使用ffmpeg从视频提取音频文件
            ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)

            # 使用Whisper模型进行音频转录
            result = self.model.transcribe(
                audio_path, language=self.language, task="transcribe"
            )

            return result["text"]
        except Exception as e:
            print(f"转录失败: {str(e)}")
            return ""
        finally:
            # 确保临时文件被删除
            if os.path.exists(audio_path):
                os.remove(audio_path)
            video.close()
