import os
import shutil
from PIL import Image

class FileOrganizer:
    def __init__(self, directory, min_width=300, min_height=300):
        self.directory = directory
        self.image_min_width = min_width
        self.image_min_height = min_height

    def create_folders(self, file_types):
        for ext in file_types:
            folder_name = ext[1:] if ext != 'no_extension' else 'no_extension'
            folder_path = os.path.join(self.directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)

    def create_category_folders(self, categorized_files):
        for category in categorized_files:
            folder_path = os.path.join(self.directory, category)
            os.makedirs(folder_path, exist_ok=True)
            if category == "Зображення":
                small_path = os.path.join(folder_path, "Малі")
                os.makedirs(small_path, exist_ok=True)

    def is_small_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                return width < self.image_min_width or height < self.image_min_height
        except Exception:
            return False

    def move_files(self, file_types):
        for ext, files in file_types.items():
            folder_name = ext[1:] if ext != 'no_extension' else 'no_extension'
            folder_path = os.path.join(self.directory, folder_name)
            for filename in files:
                src = os.path.join(self.directory, filename)
                dst = os.path.join(folder_path, filename)
                self._move_file_safe(src, dst)

    def move_files_to_categories(self, categorized_files):
        for category, files in categorized_files.items():
            folder_path = os.path.join(self.directory, category)
            for filename in files:
                src = os.path.join(self.directory, filename)
                dst = os.path.join(folder_path, filename)

                if category == "Зображення" and self.is_small_image(src):
                    dst = os.path.join(folder_path, "Малі", filename)

                self._move_file_safe(src, dst)

    def _move_file_safe(self, src, dst):
        if os.path.exists(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                print(f"Файл {os.path.basename(src)} вже існує (ідентичний) — пропускаємо.")
                return
            else:
                base, ext = os.path.splitext(os.path.basename(src))
                i = 1
                while True:
                    new_name = f"{base}_{i}{ext}"
                    new_dst = os.path.join(os.path.dirname(dst), new_name)
                    if not os.path.exists(new_dst):
                        dst = new_dst
                        break
                    i += 1

        os.makedirs(os.path.dirname(dst), exist_ok=True)  # ⬅️ Додано!
        shutil.move(src, dst)
        print(f"Переміщено: {os.path.basename(src)} → {dst}")


    def remove_empty_folders(self):
        for root, dirs, _ in os.walk(self.directory, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                if not os.listdir(folder_path):  # якщо порожня
                    try:
                        os.rmdir(folder_path)
                        print(f"Видалено порожню папку: {folder_path}")
                    except Exception as e:
                        print(f"Помилка при видаленні {folder_path}: {e}")
