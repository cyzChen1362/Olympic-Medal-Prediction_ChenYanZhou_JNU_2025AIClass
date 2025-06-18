import os
import ast
import sys
import importlib

src_path = r'..\src'
all_imports = set()

# 遍历所有 .py 文件
for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read(), filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                all_imports.add(alias.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                all_imports.add(node.module.split('.')[0])
                except Exception as e:
                    print(f"❌ 解析失败：{file_path}，原因：{e}")

# 输出导入包及版本
print("📦 依赖包及版本：\n")
for pkg in sorted(all_imports):
    try:
        mod = importlib.import_module(pkg)
        version = getattr(mod, '__version__', '（无版本信息）')
        print(f"{pkg}=={version}")
    except ModuleNotFoundError:
        print(f"{pkg}（未安装）")
    except Exception as e:
        print(f"{pkg}（读取版本失败: {e}）")
