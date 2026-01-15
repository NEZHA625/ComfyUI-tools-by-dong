import torch
import folder_paths
import math

class 音频时长计算节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "音频": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("时长",)
    FUNCTION = "get_duration"
    CATEGORY = "dong_tools/audio_duration_by_dong"

    def get_duration(self, 音频):
        waveform = 音频["waveform"]
        sample_rate = 音频["sample_rate"]

        samples = waveform.shape[-1]
        duration_seconds = samples / sample_rate

        rounded_duration = math.floor(duration_seconds * 10) / 10.0
        return (rounded_duration,)
