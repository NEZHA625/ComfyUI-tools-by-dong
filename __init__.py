import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .check import check
from .su import c
from .音频时长计算节点 import 音频时长计算节点
from .宫格图切分节点 import 宫格图切分节点
from .小显存检测节点 import 小显存检测节点
from .数据存在性检测节点 import 数据存在性检测节点
from .删除文件节点 import 删除文件节点
from .文本输入节点 import 文本输入节点
from .字符存在性检测节点 import 字符存在性检测节点
from .图像迭代节点 import 图像迭代节点
from .分辨率节点 import 分辨率节点
from .翻译节点 import 翻译节点
from .文件下载节点 import 文件下载节点
from .移动文件节点 import 移动文件节点
from .随机数节点 import 随机数节点
from .压缩节点 import 压缩节点
from .重命名节点 import 重命名节点
from .计算文件数量节点 import 计算文件数量节点
from .保存文本节点 import 保存文本节点
from .模型下载节点 import 模型下载节点
from .获取图像列表节点 import 获取图像列表节点
from .JSON取值节点 import JSON取值节点
from .保存图像节点 import 保存图像节点
from .DeepSeek节点 import DeepSeek节点
from .QwenVL节点 import QwenVL节点
from .Banana节点 import Banana节点
from .Sora2节点 import Sora2节点
from .段落数计算节点 import 段落数计算节点
from .从文本列表获取文本节点 import 从文本列表获取文本节点
from .逻辑节点 import 逻辑节点
from .通用API节点 import 通用API节点
from .JSON单键值构建节点 import JSON单键值构建节点
from .JSON多键值构建节点 import JSON多键值构建节点
from .JSON合并节点 import JSON合并节点
from .仙宫云环境变量节点 import 仙宫云环境变量节点
from .取整函数节点 import 取整函数节点
from .文件夹迭代节点 import 文件夹迭代节点
from .路径加入节点 import 路径加入节点
from .获取视频路径节点 import 获取视频路径节点
from .外补画板节点 import 外补画板节点
from .Sora2节点 import Sora2节点

NODE_CLASS_MAPPINGS = {
    "音频时长计算节点":音频时长计算节点,
    "宫格图切分节点":宫格图切分节点,
    "小显存检测节点":小显存检测节点,
    "数据存在性检测节点":数据存在性检测节点,
    "删除文件节点":删除文件节点,
    "文本输入节点":文本输入节点,
    "字符存在性检测节点":字符存在性检测节点,
    "图像迭代节点":图像迭代节点,
    "分辨率节点":分辨率节点,
    "翻译节点":翻译节点,
    "文件下载节点":文件下载节点,
    "移动文件节点":移动文件节点,
    "随机数节点":随机数节点,
    "压缩节点":压缩节点,
    "重命名节点":重命名节点,
    "计算文件数量节点":计算文件数量节点,
    "保存文本节点":保存文本节点,
    "模型下载节点":模型下载节点,
    "获取图像列表节点":获取图像列表节点,
    "JSON取值节点":JSON取值节点,
    "保存图像节点":保存图像节点,
    "DeepSeek节点":DeepSeek节点,
    "QwenVL节点":QwenVL节点,
    "Banana节点":Banana节点,
    "Sora2节点":Sora2节点,
    "段落数计算节点":段落数计算节点,
    "从文本列表获取文本节点":从文本列表获取文本节点,
    "逻辑节点":逻辑节点,
    "通用API节点":通用API节点,
    "JSON单键值构建节点":JSON单键值构建节点,
    "JSON多键值构建节点":JSON多键值构建节点,
    "JSON合并节点":JSON合并节点,
    "仙宫云环境变量节点":仙宫云环境变量节点,
    "取整函数节点":取整函数节点,
    "文件夹迭代节点":文件夹迭代节点,
    "路径加入节点":路径加入节点,
    "获取视频路径节点":获取视频路径节点,
    "外补画板节点":外补画板节点,
    "Sora2节点":Sora2节点,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "音频时长计算节点": "音频时长计算",
    "宫格图切分节点":"宫格切分",
    "小显存检测节点":"小显存检测",
    "数据存在性检测节点":"数据存在性检测",
    "删除文件节点":"删除文件或文件夹",
    "文本输入节点":"文本",
    "字符存在性检测节点":"字符检测",
    "图像迭代节点":"图像迭代",
    "分辨率节点":"分辨率",
    "翻译节点":"翻译",
    "文件下载节点":"文件下载",
    "移动文件节点":"移动文件",
    "随机数节点":"随机数",
    "压缩节点":"压缩",
    "重命名节点":"重命名",
    "计算文件数量节点":"计算文件数量",
    "保存文本节点":"保存文本",
    "模型下载节点":"模型下载",
    "获取图像列表节点":"获取图像列表",
    "JSON取值节点":"JSON取值",
    "保存图像节点":"保存图像",
    "DeepSeek节点":"DeepSeek",
    "QwenVL节点":"QwenVL",
    "Banana节点":"nano_banana_pro",
    "Sora2节点":"Sora2",
    "段落数计算节点":"段落数计算",
    "从文本列表获取文本节点":"索引文本",
    "逻辑节点":"逻辑",
    "通用API节点":"通用API",
    "JSON单键值构建节点":"JSON_Build",
    "JSON多键值构建节点":"JSON_Build_Multi",
    "JSON合并节点":"JSON合并",
    "仙宫云环境变量节点":"仙宫云环境变量",
    "取整函数节点":"取整函数",
    "文件夹迭代节点":"文件夹迭代",
    "路径加入节点":"路径加入",
    "获取视频路径节点":"获取视频路径",
    "外补画板节点":"外补画板",
    "Sora2节点":"Sora2",
}
