from .huggingface_upload_node import HuggingFaceUploadNode
from .url_to_img_node import ImageDownloader  
from .lora_iterator import LoraIterator
from .move_by_prefix import FileMoveNode
from .Input_Detection import InputDetectionNode
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
from .LLM_Node import LLM_Node
from .RandomNumbers import RandomNumbersNode
from .HashCalculations import HashCalculationsNode
from .Get_json_value import Get_json_value_Node

# 定义节点映射
NODE_CLASS_MAPPINGS = {
    "HuggingFaceUploadNode": HuggingFaceUploadNode,
    "ImageDownloader": ImageDownloader,
    "LoraIterator": LoraIterator,
    "FileMoveNode": FileMoveNode,
    "InputDetectionNode": InputDetectionNode,
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
    "LLM_Node":LLM_Node,  
    "RandomNumbersNode":RandomNumbersNode,
    "HashCalculationsNode":HashCalculationsNode,
    "Get_json_value_Node":Get_json_value_Node
}

# 定义节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "HuggingFaceUploadNode": "HuggingFace_upload_by_dong",
    "ImageDownloader": "Download_img_by_dong",
    "LoraIterator": "Lora_Iterator_by_dong",
    "FileMoveNode": "Move_files_by_dong",
    "InputDetectionNode": "Input_Detection_by_dong",
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
    "LLM_Node":"LLM_by_dong",
    "RandomNumbersNode":"Random_Numbers_by_dong",
    "HashCalculationsNode":"Hash_Calculations_by_dong",
    "Get_json_value_Node":"Get_json_value_by_dong",
}
