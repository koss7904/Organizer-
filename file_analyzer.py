import os
from collections import defaultdict
from file_categorizer import FileCategorizer

class FileAnalyzer:
    def __init__(self, directory):
        self.directory = directory  # ← правильний шлях до папки
        self.exclude_dirs = {
            "Документи", "Зображення", "Аудіо", "Відео", "Архіви",
            "Код", "Програми", "Google Colab", "Інше"
        }

    def analyze_file_types(self, recursive=False):
        file_types = defaultdict(list)

        if recursive:
            for root, _, files in os.walk(self.directory):
                if any(os.path.normpath(ex) in os.path.normpath(root) for ex in self.exclude_dirs):
                    continue
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower() or 'no_extension'
                    file_types[ext].append(os.path.relpath(os.path.join(root, filename), self.directory))
        else:
            for filename in os.listdir(self.directory):
                filepath = os.path.join(self.directory, filename)
                if os.path.isfile(filepath) and not filename.startswith("report") and not filename.startswith("preview"):
                    ext = os.path.splitext(filename)[1].lower() or 'no_extension'
                    file_types[ext].append(filename)

        return file_types


    def analyze_by_category(self, recursive=False):
        categorized_files = defaultdict(list)

        if recursive:
            for root, _, files in os.walk(self.directory):
                if any(os.path.normpath(ex) in os.path.normpath(root) for ex in self.exclude_dirs):
                    continue
                for filename in files:
                    if filename.startswith("report") or filename.startswith("preview"):
                        continue
                    ext = os.path.splitext(filename)[1].lower()
                    category = FileCategorizer.get_category(ext)
                    full_path = os.path.relpath(os.path.join(root, filename), self.directory)
                    categorized_files[category].append(full_path)
        else:
            for filename in os.listdir(self.directory):
                filepath = os.path.join(self.directory, filename)
                if os.path.isfile(filepath) and not filename.startswith("report") and not filename.startswith("preview"):
                    ext = os.path.splitext(filename)[1].lower()
                    category = FileCategorizer.get_category(ext)
                    categorized_files[category].append(filename)

        return categorized_files

