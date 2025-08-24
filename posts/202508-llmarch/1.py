import os

# 定义要删除的前缀字符串
# 注意：这里我们直接使用了URL编码后的字符串，因为文件名中就是这种形式
PREFIX_TO_REMOVE = "https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F"

def rename_files_in_current_directory(prefix, dry_run=True):
    """
    重命名当前目录下的文件，删除指定的前缀。

    Args:
        prefix (str): 要从文件名中删除的字符串前缀。
        dry_run (bool):
            如果为 True，则只打印会发生什么，不实际执行重命名。
            如果为 False，则实际执行重命名操作。
    """
    print(f"--- 文件重命名脚本 ---")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"要删除的前缀: '{prefix}'\n")

    files_to_rename = []

    # 遍历当前目录下的所有文件和文件夹
    for filename in os.listdir('.'):
        # 构造完整路径，以确保处理的是文件而不是目录
        full_path = os.path.join('.', filename)

        # 检查是否是文件以及文件名是否以指定前缀开头
        if os.path.isfile(full_path) and filename.startswith(prefix):
            new_filename = filename.replace(prefix, '')
            files_to_rename.append((filename, new_filename))

            # 打印预览
            print(f"  [PREVIEW] '{filename}'  ->  '{new_filename}'")
        elif os.path.isfile(full_path):
            # 这是一个文件，但不是我们需要处理的
            print(f"  [SKIPPING] '{filename}' 不符合重命名模式。")
        else:
            # 这是一个目录或其他非文件项
            print(f"  [SKIPPING] '{filename}' (非文件)。")

    if not files_to_rename:
        print("\n当前目录下没有找到符合重命名模式的文件。")
        return

    if dry_run:
        print("\n--- 干运行模式 (Dry Run) ---")
        print("以上是本次运行的预览。文件尚未被实际重命名。")
        confirmation = input("是否要执行实际的重命名操作？(输入 'yes' 确认): ").lower()
        if confirmation == 'yes':
            print("\n--- 开始实际重命名 ---")
            rename_files_in_current_directory(prefix, dry_run=False) # 再次调用，这次执行实际重命名
        else:
            print("用户取消了重命名操作。")
    else: # 实际执行模式
        print("\n--- 执行实际重命名 ---")
        for old_name, new_name in files_to_rename:
            try:
                os.rename(old_name, new_name)
                print(f"  重命名成功: '{old_name}' -> '{new_name}'")
            except OSError as e:
                print(f"  重命名失败 '{old_name}' 为 '{new_name}': {e}")
        print("\n--- 重命名完成 ---")

if __name__ == "__main__":
    # 默认以干运行模式启动
    rename_files_in_current_directory(PREFIX_TO_REMOVE, dry_run=True)
