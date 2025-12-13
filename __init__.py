import os
import sys
current_script_path = os.path.dirname(os.path.abspath(__file__))
custom_nodes_path = os.path.join(current_script_path)
sys.path.append(custom_nodes_path)
from .check import check
from .su import c
from .huggingface_upload_node import HuggingFaceUploadNode
from .url_to_img_node import ImageDownloader  
from .lora_iterator import LoraIterator
from .move_by_prefix import FileMoveNode
from .Data_handle import Data_handle_Node
from .rename import RenameNode
from .Logic_Tools import LogicToolsNode
from .CategorizeNode import CategorizeNode
from .ZIPwith7zNode import ZIPwith7zNode
from .save_the_txt import SaveTXTNode
from .Image2GIF import Image2GIFNode
from .A1111_style_Flux import A1111_FLUX_DATA_NODE
from .TranslateAPI import TranslateAPINode
from .LibLib_upload import LibLib_upload_Node
from .folder_iterator import FolderIteratorNODE
from .DeepSeek_Node import DeepSeek_Node
from .RandomNumbers import RandomNumbersNode
from .HashCalculations import HashCalculationsNode
from .Get_json_value import Get_json_value_Node
from .resolution import ResolutionNode
from .set_api import set_api_Node
from .text_to_json import TextToJsonNode
from .path_join_Node import path_join_Node
from .set_appid import SetAppidNode
from .get_cookies import Get_cookies_Node
from .img2url import IMG2URLNode
from .img_understanding import img_understanding_Node
from .save_img import save_img_NODE
from .Klingai_post_node import klingai_video_Node
from .Klingai_get_node import Get_video_Node
from .Downloader import Downloader
from .Delay_node import Delay_node
from .Dong_Text_Node import Dong_Text_Node
# from .DongShowTextNode import DongShowTextNode
from .PromptConcatNode import PromptConcatNode
from .ImageResizeNode import ImageResizeNode
from .Dong_Pixelate_Node import Dong_Pixelate_Node
from .find_files_by_extension_Node import find_files_by_extension_Node
from .Delete_folder_Node import Delete_folder_Node
# from .Notice_Node import Notice_Node
from .text_replace_node import text_replace_node
from .cogview_3_flash_Node import cogview_3_flash_Node
from .file_analysis_Node import file_analysis_Node
from .cogvideox_flash_post_Node import cogvideox_flash_post_Node
from .cogvideox_flash_get_Node import cogvideox_flash_get_Node
from .Wan21_post_Node import Wan21_post_Node
from .Wan21_get_Node import Wan21_get_Node
from .get_video_from_url_Node import get_video_from_url_Node
# from .douyin_remove_watermark_Node import douyin_remove_watermark_Node
from .AudioPathToAudioNode import AudioPathToAudioNode
from .AudioDurationNode import AudioDurationNode
from .img2url_v2_Node import img2url_v2_Node
from .bailian_model_select_Node import bailian_model_select_Node
from .DownloadNode import DownloadNode
from .CountFilesFromFolderNode import CountFilesFromFolderNode
from .GetImageListFromFloderNode import GetImageListFromFloderNode
from .GetImageListFromFloderNode2 import GetImageListFromFloderNode2
from .INTNODE import INTNODE
from .DouBao import doubaoNode
from .image_iterator import image_iterator
from .img_understanding_v2 import GLM_Node
from .save_img_v2 import save_img_v2_NODE
from .get_image_list import GetRefModelImageListNode
from .get_text_from_list import get_text_from_list_Node
from .Check_Vram import checkvram_node
from .Qwen3VL_30B_A3B_Thinking import Qwen3VL_30_Node
from .Qwen3VL_235B_A22B_Thinking import Qwen3VL_235_Node
from .QwenVL import QwenVL_Node
from .IFEXISTTEXTNODE import IFEXISTTEXTNODE
from .kie_nano_post_node import kie_nano_post_node
from .kie_nano_get_node import kie_nano_get_node
from .kie_base64_upload_node import kie_base64_upload_node
from .suchuang_nano_post_node import suchuang_nano_post_node
from .suchuang_get_node import suchuang_get_node

NODE_CLASS_MAPPINGS = {
    "HuggingFaceUploadNode": HuggingFaceUploadNode,
    "ImageDownloader": ImageDownloader,
    "LoraIterator": LoraIterator,
    "FileMoveNode": FileMoveNode,
    "Data_handle_Node": Data_handle_Node,
    "RenameNode": RenameNode,
    "LogicToolsNode": LogicToolsNode,
    "CategorizeNode": CategorizeNode,
    "ZIPwith7zNode": ZIPwith7zNode,
    "SaveTXTNode": SaveTXTNode,
    "Image2GIFNode": Image2GIFNode,
    "A1111_FLUX_DATA_NODE": A1111_FLUX_DATA_NODE,
    "TranslateAPINode":TranslateAPINode,
    "LibLib_upload_Node":LibLib_upload_Node,    
    "FolderIteratorNODE":FolderIteratorNODE,
    "DeepSeek_Node":DeepSeek_Node,  
    "RandomNumbersNode":RandomNumbersNode,
    "HashCalculationsNode":HashCalculationsNode,
    "Get_json_value_Node":Get_json_value_Node,
    "ResolutionNode":ResolutionNode,
    "set_api_Node":set_api_Node,
    "TextToJsonNode":TextToJsonNode,
    "path_join_Node":path_join_Node,
    "SetAppidNode":SetAppidNode,
    "Get_cookies_Node":Get_cookies_Node,
    "IMG2URLNode":IMG2URLNode,
    "img_understanding_Node":img_understanding_Node,
    "save_img_NODE":save_img_NODE,
    "klingai_video_Node":klingai_video_Node,
    "Get_video_Node":Get_video_Node,
    "Downloader":Downloader,
    "Delay_node":Delay_node,
    "Dong_Text_Node":Dong_Text_Node,
    # "DongShowTextNode":DongShowTextNode,
    "PromptConcatNode":PromptConcatNode,
    "ImageResizeNode":ImageResizeNode,
    "Dong_Pixelate_Node":Dong_Pixelate_Node,
    "find_files_by_extension_Node":find_files_by_extension_Node,
    "Delete_folder_Node":Delete_folder_Node,
    # "Notice_Node":Notice_Node,
    "text_replace_node":text_replace_node,
    "cogview_3_flash_Node":cogview_3_flash_Node,
    "file_analysis_Node":file_analysis_Node,
    "cogvideox_flash_post_Node":cogvideox_flash_post_Node,
    "cogvideox_flash_get_Node":cogvideox_flash_get_Node,
    "Wan21_post_Node":Wan21_post_Node,
    "Wan21_get_Node":Wan21_get_Node,
    "get_video_from_url_Node":get_video_from_url_Node,
    # "douyin_remove_watermark_Node":douyin_remove_watermark_Node,
    "AudioPathToAudioNode":AudioPathToAudioNode,
    "AudioDurationNode":AudioDurationNode,
    "img2url_v2_Node":img2url_v2_Node,
    "bailian_model_select_Node":bailian_model_select_Node,
    "DownloadNode":DownloadNode,
    "CountFilesFromFolderNode":CountFilesFromFolderNode,
    "GetImageListFromFloderNode":GetImageListFromFloderNode,
    "GetImageListFromFloderNode2":GetImageListFromFloderNode2,
    "INTNODE":INTNODE,
    "doubaoNode":doubaoNode,
    "image_iterator":image_iterator,
    "GLM_Node":GLM_Node,
    "save_img_v2_NODE":save_img_v2_NODE,
    "GetRefModelImageListNode":GetRefModelImageListNode,
    "get_text_from_list_Node":get_text_from_list_Node,
    "checkvram_node":checkvram_node,
    "Qwen3VL_30_Node":Qwen3VL_30_Node,
    "Qwen3VL_235_Node":Qwen3VL_235_Node,
    "QwenVL_Node":QwenVL_Node,
    "IFEXISTTEXTNODE":IFEXISTTEXTNODE,
    "kie_nano_post_node":kie_nano_post_node,
    "kie_nano_get_node":kie_nano_get_node,
    "kie_base64_upload_node":kie_base64_upload_node,
    "suchuang_nano_post_node":suchuang_nano_post_node,
    "suchuang_get_node":suchuang_get_node,
}

# 定义节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "HuggingFaceUploadNode": "HuggingFace_upload_by_dong",
    "ImageDownloader": "get_image",
    "LoraIterator": "Lora迭代器",
    "FileMoveNode": "移动文件",
    "Data_handle_Node": "数据处理",
    "RenameNode": "重命名",
    "LogicToolsNode": "逻辑",
    "CategorizeNode": "分类",
    "ZIPwith7zNode": "压缩",
    "SaveTXTNode": "保存文本",
    "Image2GIFNode": "图像转GIF",
    "A1111_FLUX_DATA_NODE": "A1111_FLUX_DATA_by_dong",
    "TranslateAPINode":"翻译",
    "LibLib_upload_Node":"LibLib_upload_by_dong",
    "FolderIteratorNODE":"文件夹迭代器",
    "DeepSeek_Node":"DeepSeek",
    "RandomNumbersNode":"种子",
    "HashCalculationsNode":"哈希计算",
    "Get_json_value_Node":"json取值",
    "ResolutionNode":"分辨率",
    "set_api_Node":"设置API",
    "TextToJsonNode":"save_to_json_by_dong",
    "path_join_Node":"路径加入",
    "SetAppidNode":"授权",
    "Get_cookies_Node":"登录",
    "IMG2URLNode":"Img2url_by_dong",
    "img_understanding_Node":"图片理解",
    "save_img_NODE":"保存图片",
    "klingai_video_Node":"video_by_dong",
    "Get_video_Node":"Get_video_by_dong",
    "Downloader":"下载器",
    "Delay_node":"sleep",
    "Dong_Text_Node":"文本",
    # "DongShowTextNode":"展示文本",
    "PromptConcatNode":"文本连接",
    "ImageResizeNode":"Image_Resize",
    "Dong_Pixelate_Node":"图片像素化",
    "find_files_by_extension_Node":"find_files_by_extension_by_dong",
    "Delete_folder_Node":"删除文件夹",
    # "Notice_Node":"通知",
    "text_replace_node":"文本替换",
    "cogview_3_flash_Node":"cogview_3_flash_by_dong",
    "file_extract_Node":"file_analysis_by_dong",
    "cogvideox_flash_post_Node":"cogvideox_flash_post_by_dong",
    "cogvideox_flash_get_Node":"cogvideox_flash_get_by_dong",
    "Wan21_post_Node":"Wan21_post_Node_by_dong",
    "Wan21_get_Node":"Wan21_get_Node_by_dong",
    "get_video_from_url_Node":"get_video_from_url_by_dong",
    # "douyin_remove_watermark_Node":"抖音去水印",
    "AudioPathToAudioNode":"从路径到音频",
    "AudioDurationNode":"获取音频时长",
    "img2url_v2_Node":"img2url_v2_by_dong",
    "bailian_model_select_Node":"百炼模型选择",
    "DownloadNode":"模型下载器",
    "CountFilesFromFolderNode":"文件数计算",
    "GetImageListFromFloderNode":"获取图像列表",
    "GetImageListFromFloderNode2":"获取图像列表2",
    "INTNODE":"INT",
    "doubaoNode":"豆包",
    "image_iterator":"图片递归迭代",
    "GLM_Node":"视觉识别",
    "save_img_v2_NODE":"保存图像_v2",
    "GetRefModelImageListNode":"获取图像列表_v2",
    "get_text_from_list_Node":"从列表获取文本",
    "checkvram_node":"是否低显存",
    "Qwen3VL_30_Node":"视觉识别_v2",
    "Qwen3VL_235_Node":"视觉识别_v3",
    "QwenVL_Node":"视觉识别_Pro",
    "IFEXISTTEXTNODE":"文字是否存在",
    "kie_nano_post_node":"nano_post",
    "kie_nano_get_node":"nano_get",
    "kie_base64_upload_node":"nano_upload",
    "suchuang_nano_post_node":"速创_nano_post_node",
    "suchuang_get_node":"速创_get_node",
}
