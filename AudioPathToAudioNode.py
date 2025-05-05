import torchaudio
import folder_paths
import torch

class AudioPathToAudioNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_path": ("AUDIOPATH",),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "convert"
    CATEGORY = "dong_tools/audio_path_to_audio_by_dong"

    def convert(self, audio_path):
        file_path = folder_paths.get_annotated_filepath(audio_path)
        waveform, sample_rate = torchaudio.load(file_path)

        # 标准化为 [batch, channels, samples]
        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0).unsqueeze(0)  # [1, 1, samples]
        elif waveform.dim() == 2:
            waveform = waveform.unsqueeze(0)  # [1, channels, samples]

        return ({
            "waveform": waveform,           # 标准字段
            "sample_rate": sample_rate      # 标准字段
        },)
