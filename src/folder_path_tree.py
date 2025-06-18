import os

def print_tree(start_path, indent=""):
    for i, item in enumerate(sorted(os.listdir(start_path))):
        path = os.path.join(start_path, item)
        connector = "└── " if i == len(os.listdir(start_path)) - 1 else "├── "
        print(indent + connector + item)
        if os.path.isdir(path):
            extension = "    " if i == len(os.listdir(start_path)) - 1 else "│   "
            print_tree(path, indent + extension)

# 修改为你自己的文件夹路径
folder_path = r'..\src'
print(folder_path)
print_tree(folder_path)
