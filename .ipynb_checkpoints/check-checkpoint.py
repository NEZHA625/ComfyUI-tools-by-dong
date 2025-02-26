import os
from su import c

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
Authorization_path = os.path.join(ComfyUI_path, "Authorization.txt")

def check():
    if not os.path.exists(Authorization_path):
        return False
    a = c()
    with open(Authorization_path, 'r') as file:
        b = file.read().strip()
    if a == b:
        return True
    else:
        return False