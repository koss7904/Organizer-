import tkinter as tk
from tkinter import filedialog, messagebox
import os

from file_analyzer import FileAnalyzer
from file_categorizer import FileCategorizer
from file_organizer import FileOrganizer
from report_writer import ReportWriter
from rollback_manager import RollbackManager
from directory_tools import flatten_directory



class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортування файлів")
        self.root.geometry("500x400")

        self.path_label = tk.Label(root, text="Введіть або оберіть директорію:")
        self.path_label.pack(pady=5)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        # Поля для налаштування розміру малих зображень
        self.size_frame = tk.Frame(root)
        self.size_frame.pack(pady=5)

        tk.Label(self.size_frame, text="Мін. ширина (px):").grid(row=0, column=0)
        self.min_width_entry = tk.Entry(self.size_frame, width=6)
        self.min_width_entry.insert(0, "300")
        self.min_width_entry.grid(row=0, column=1)

        tk.Label(self.size_frame, text="Мін. висота (px):").grid(row=0, column=2)
        self.min_height_entry = tk.Entry(self.size_frame, width=6)
        self.min_height_entry.insert(0, "300")
        self.min_height_entry.grid(row=0, column=3)

        self.browse_btn = tk.Button(root, text="Огляд...", command=self.browse_folder)
        self.browse_btn.pack(pady=5)

        self.sort_type_btn = tk.Button(root, text="Сортувати за типами файлів", command=self.sort_by_type)
        self.sort_type_btn.pack(pady=5)

        self.preview_btn = tk.Button(root, text="Переглянути перед сортуванням", command=self.preview_sorting)
        self.preview_btn.pack(pady=5)


        self.sort_category_btn = tk.Button(root, text="Сортувати за категоріями", command=self.sort_by_category)
        self.sort_category_btn.pack(pady=5)

        self.rollback_btn = tk.Button(root, text="Відкат сортування", command=self.rollback_sorting)
        self.rollback_btn.pack(pady=5)

        self.size_btn = tk.Button(root, text="Показати розмір за категоріями", command=self.show_size_by_category)
        self.size_btn.pack(pady=5)

        self.remove_empty_var = tk.BooleanVar(value=True)
        self.remove_empty_check = tk.Checkbutton(
            root,
            text="Видаляти порожні папки після сортування",
            variable=self.remove_empty_var
        )
        self.remove_empty_check.pack(pady=5)
        self.flatten_var = tk.BooleanVar()
        self.flatten_check = tk.Checkbutton(root, text="Спочатку перемістити файли з усіх підпапок у корінь", variable=self.flatten_var)
        self.flatten_check.pack(pady=5)

    def is_recursive(self):
        return False



    def preview_sorting(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Помилка", "Невірна директорія!")
            return

        recursive = self.is_recursive()
        analyzer = FileAnalyzer(directory)


        # Аналіз обох варіантів
        preview = ""

        # За типами
        file_types = analyzer.analyze_file_types()
        preview += "📁 Сортування за типами:\n"
        for ext, files in file_types.items():
            folder = ext[1:] if ext != 'no_extension' else 'no_extension'
            for file in files:
                preview += f"{file} → {folder}/\n"

        preview += "\n\n"

        # За категоріями
        categorized_files = analyzer.analyze_by_category(recursive=recursive)
        preview += "📁 Сортування за категоріями:\n"
        for category, files in categorized_files.items():
            for file in files:
                subfolder = category
                if category == "Зображення":
                    width, height = self.get_image_size_threshold()
                    organizer = FileOrganizer(directory, min_width=width, min_height=height)
                    src = os.path.join(directory, file)
                    if organizer.is_small_image(src):
                        subfolder += "/Малі"
                preview += f"{file} → {subfolder}/\n"
        # Зберегти preview.txt
        preview_path = os.path.join(directory, "preview.txt")
        try:
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(preview)
            print(f"Попередній перегляд збережено у {preview_path}")
        except Exception as e:
            print(f"Не вдалося зберегти preview.txt: {e}")

        # Показ у новому вікні
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Попередній перегляд")
        text_widget = tk.Text(preview_window, wrap="word", width=80, height=30)
        text_widget.insert("1.0", preview)
        text_widget.config(state="disabled")
        text_widget.pack(padx=10, pady=10)

    def show_size_by_category(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Помилка", "Невірна директорія!")
            return

        if self.flatten_var.get():
            flatten_directory(directory)


        analyzer = FileAnalyzer(directory)
        categorized_files = analyzer.analyze_by_category()

        result = "📊 Розмір за категоріями:\n\n"
        total = 0

        for category, files in categorized_files.items():
            size = 0
            for filename in files:
                filepath = os.path.join(directory, filename)
                if os.path.exists(filepath):
                    size += os.path.getsize(filepath)
                elif os.path.exists(os.path.join(directory, category, "Малі", filename)):
                    size += os.path.getsize(os.path.join(directory, category, "Малі", filename))
            mb = size / (1024 * 1024)
            total += mb
            result += f"{category}: {mb:.2f} МБ\n"

        result += f"\n🔸 Загалом: {total:.2f} МБ"

        # Відображення
        size_window = tk.Toplevel(self.root)
        size_window.title("Розмір за категоріями")
        text = tk.Text(size_window, width=50, height=20)
        text.insert("1.0", result)
        text.config(state="disabled")
        text.pack(padx=10, pady=10)

    def rollback_sorting(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Помилка", "Невірна директорія!")
            return

        try:
            manager = RollbackManager(directory)
            manager.load_report()
            manager.rollback()
            manager.flatten_selected_folders(["Документи", "Програми", "pdf", "apk"])  # ⬅️ додано
            messagebox.showinfo("Готово", "Файли повернуто назад у вихідну директорію!")
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл report.txt не знайдено!")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def get_image_size_threshold(self):
        try:
            width = int(self.min_width_entry.get())
            height = int(self.min_height_entry.get())
            return width, height
        except ValueError:
            messagebox.showerror("Помилка", "Некоректне значення розміру зображення!")
            return 300, 300


    def sort_by_type(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Помилка", "Невірна директорія!")
            return


        if self.flatten_var.get():
            flatten_directory(directory)

        recursive = self.is_recursive()
        analyzer = FileAnalyzer(directory)
        file_types = analyzer.analyze_file_types(recursive=recursive)

        width, height = self.get_image_size_threshold()
        organizer = FileOrganizer(directory, min_width=width, min_height=height)
        organizer.create_folders(file_types)
        report = ReportWriter(directory)

        for ext, files in file_types.items():
            folder = ext[1:] if ext != 'no_extension' else 'no_extension'
            for filename in files:
                # Замість name_only — записуємо повний відносний шлях
                report.add_entry("Тип", filename, folder)

        organizer.move_files(file_types)
        report.save()

        if self.remove_empty_var.get():
            organizer.remove_empty_folders()

        messagebox.showinfo("Готово", "Файли відсортовано за типами!")


    def sort_by_category(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Помилка", "Невірна директорія!")
            return

        recursive = self.is_recursive()
        analyzer = FileAnalyzer(directory)
        categorized_files = analyzer.analyze_by_category(recursive=recursive)

        width, height = self.get_image_size_threshold()
        organizer = FileOrganizer(directory, min_width=width, min_height=height)
        organizer.create_category_folders(categorized_files)
        report = ReportWriter(directory)

        for category, files in categorized_files.items():
            for filename in files:
                subfolder = category
                src = os.path.join(directory, filename)
                if category == "Зображення":
                    if organizer.is_small_image(src):
                        subfolder += "/Малі"
                # Замість name_only — записати весь відносний шлях
                report.add_entry("Категорія", filename, subfolder)

        organizer.move_files_to_categories(categorized_files)
        report.save()

        if self.remove_empty_var.get():
            organizer.remove_empty_folders()

        messagebox.showinfo("Готово", "Файли відсортовано за категоріями!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()
