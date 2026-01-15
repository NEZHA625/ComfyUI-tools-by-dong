import torchaudio
import folder_paths
import torch

class 音频路径到音频节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "音频路径": ("AUDIOPATH",),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "convert"
    CATEGORY = "dong_tools/audio_path_to_audio_by_dong"

    def convert(self, 音频路径):
        file_path = folder_paths.get_annotated_filepath(音频路径)
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
