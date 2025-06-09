import os

def flatten_directory(root_directory):
    """
    Переміщує всі файли з підкаталогів у кореневу директорію.
    """
    moved_files = []
    for dirpath, _, filenames in os.walk(root_directory):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            if dirpath == root_directory:
                continue
            dst_path = os.path.join(root_directory, file)
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(file)
                i = 1
                while True:
                    new_name = f"{base}_flat_{i}{ext}"
                    dst_path = os.path.join(root_directory, new_name)
                    if not os.path.exists(dst_path):
                        break
                    i += 1
            os.rename(full_path, dst_path)
            moved_files.append((full_path, dst_path))
    return moved_files
