import os
import shutil

class RollbackManager:
    def __init__(self, directory):
        self.directory = directory
        self.report_path = os.path.join(directory, "report.txt")
        self.entries = []

    def load_report(self):
        if not os.path.exists(self.report_path):
            raise FileNotFoundError("Файл звіту не знайдено!")

        with open(self.report_path, "r", encoding="utf-8") as f:
            for line in f:
                if "→" in line:
                    parts = line.strip().split("→")
                    file_part = parts[0].split("]")[-1].strip()
                    folder_part = parts[1].strip().rstrip("/")
                    self.entries.append((file_part, folder_part))

    def rollback(self):
        for filename, folder in self.entries:
            full_path = os.path.join(self.directory, folder, filename)
            base_filename = os.path.basename(filename)

            if os.path.exists(full_path):
                src_path = full_path
            elif os.path.exists(os.path.join(self.directory, folder, "Малі", base_filename)):
                src_path = os.path.join(self.directory, folder, "Малі", base_filename)
            elif os.path.exists(os.path.join(self.directory, folder, base_filename)):
                src_path = os.path.join(self.directory, folder, base_filename)
            else:
                print(f"⛔ Пропущено: {filename} — не знайдено в {folder}")
                continue

            dst_path = os.path.join(self.directory, base_filename)

            if os.path.exists(dst_path):
                base, ext = os.path.splitext(base_filename)
                i = 1
                while True:
                    new_name = f"{base}_rollback_{i}{ext}"
                    new_dst = os.path.join(self.directory, new_name)
                    if not os.path.exists(new_dst):
                        dst_path = new_dst
                        break
                    i += 1

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.move(src_path, dst_path)
            print(f"✅ Повернуто: {base_filename}")

        self.remove_empty_folders()

    def remove_empty_folders(self):
        for root, dirs, _ in os.walk(self.directory, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                if not os.listdir(folder_path):
                    try:
                        os.rmdir(folder_path)
                        print(f"🗑 Видалено порожню папку: {folder_path}")
                    except Exception as e:
                        print(f"⚠️ Помилка при видаленні {folder_path}: {e}")

    def flatten_selected_folders(self, folder_names=("Документи", "Програми", "pdf", "apk")):
        for folder in folder_names:
            folder_path = os.path.join(self.directory, folder)
            if not os.path.exists(folder_path):
                continue

            for root, _, files in os.walk(folder_path):
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(self.directory, file)

                    if os.path.exists(dst):
                        base, ext = os.path.splitext(file)
                        i = 1
                        while True:
                            new_name = f"{base}_from_{folder}_{i}{ext}"
                            new_dst = os.path.join(self.directory, new_name)
                            if not os.path.exists(new_dst):
                                dst = new_dst
                                break
                            i += 1

                    shutil.move(src, dst)
                    print(f"📂 Переміщено з {folder}: {file} → {dst}")

        self.remove_empty_folders()

