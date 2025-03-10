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
from .DongShowTextNode import DongShowTextNode
from .PromptConcatNode import PromptConcatNode
from .ImageResizeNode import ImageResizeNode
from .Dong_Pixelate_Node import Dong_Pixelate_Node

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
    "DongShowTextNode":DongShowTextNode,
    "PromptConcatNode":PromptConcatNode,
    "ImageResizeNode":ImageResizeNode,
    "Dong_Pixelate_Node":Dong_Pixelate_Node
}

# 定义节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "HuggingFaceUploadNode": "HuggingFace_upload_by_dong",
    "ImageDownloader": "Download_img_by_dong",
    "LoraIterator": "Lora_Iterator_by_dong",
    "FileMoveNode": "Move_files_by_dong",
    "Data_handle_Node": "Data_handle_by_dong",
    "RenameNode": "Rename_by_dong",
    "LogicToolsNode": "Logic_by_dong",
    "CategorizeNode": "Categorized_by_dong",
    "ZIPwith7zNode": "ZIP_with_7z_by_dong",
    "SaveTXTNode": "Save_txt_by_dong",
    "Image2GIFNode": "Image2GIF_by_dong",
    "A1111_FLUX_DATA_NODE": "A1111_FLUX_DATA_by_dong",
    "TranslateAPINode":"Translate_by_dong",
    "LibLib_upload_Node":"LibLib_upload_by_dong",
    "FolderIteratorNODE":"Folder_Iterator_by_dong",
    "DeepSeek_Node":"DeepSeek_by_dong",
    "RandomNumbersNode":"Random_Numbers_by_dong",
    "HashCalculationsNode":"Hash_Calculations_by_dong",
    "Get_json_value_Node":"Get_json_value_by_dong",
    "ResolutionNode":"Resolution_by_dong",
    "set_api_Node":"set_api_Node_by_dong",
    "TextToJsonNode":"save_to_json_by_dong",
    "path_join_Node":"path_join_by_dong",
    "SetAppidNode":"授权",
    "Get_cookies_Node":"登录",
    "IMG2URLNode":"Img2url_by_dong",
    "img_understanding_Node":"图片理解",
    "save_img_NODE":"save_img_by_dong",
    "klingai_video_Node":"video_by_dong",
    "Get_video_Node":"Get_video_by_dong",
    "Downloader":"Downloader_by_dong",
    "Delay_node":"Delay_by_dong",
    "Dong_Text_Node":"Text_by_Dong",
    "DongShowTextNode":"show_text_by_Dong",
    "PromptConcatNode":"Prompt_ConcatNode_by_Dong",
    "ImageResizeNode":"Image_Resize_by_Dong",
    "Dong_Pixelate_Node":"像素化",
}
