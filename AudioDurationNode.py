import torch
import folder_paths
import math

class AudioDurationNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("duration",)
    FUNCTION = "get_duration"
    CATEGORY = "dong_tools/audio_duration_by_dong"

    def get_duration(self, audio):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        # waveform shape: [batch, channels, samples]
        samples = waveform.shape[-1]
        duration_seconds = samples / sample_rate
        # float(duration_seconds)
        rounded_duration = math.floor(duration_seconds * 10) / 10.0
        return (rounded_duration,)
