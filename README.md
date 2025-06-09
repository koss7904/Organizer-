Менеджер сортування файлів (File Organizer GUI)

Основні функції:

✅ Сортування за типами файлів (`.txt`, `.png`, `.mp3` тощо)
✅ Сортування за категоріями (`Документи`, `Зображення`, `Аудіо`, `Програми`, ...)
✅ Розпізнавання малих зображень та переміщення їх в окрему папку `Малі`
✅ Попередній перегляд структури перед сортуванням
✅ Звіт (`report.txt`) про всі переміщення
✅ Відкат сортування** — повернення всіх файлів назад
✅ Видалення порожніх папок
✅ Підрахунок розміру категорій/типів файлів
✅ Опція витягування усіх файлів з вкладених папок (flatten)
✅ Мінімальні налаштування — введення шляху, кнопки дій, опції



Інтерфейс користувача:
 Поле для вибору директорії
 Кнопки:
 "Сортувати за типами"
 "Сортувати за категоріями"
 "Переглянути перед сортуванням"
 "Відкат сортування"
 "Очистити порожні папки"
Опції:
Перемістити все в корінь перед сортуванням
Налаштування розміру малих зображень
Технології:
Python 3.10+
Tkinter
Pillow (для обробки зображень)

File Organizer GUI
Features:
Sort files by extension (e.g. `.txt`, `.png`)
Sort files by category (e.g. "Documents", "Programs")
Detect and move small images to subfolder
Preview sorting structure before applying
Save detailed report of actions
Undo file sorting using the report
Remove empty folders after sorting
Show total size per file type/category
Option to flatten nested folders
Lightweight and customizable

UI Overview:
Directory input
Buttons:
 "Sort by File Types"
 "Sort by Categories"
 "Preview Sorting"
 "Undo Sorting"
 "Remove Empty Folders"
Checkboxes:
Flatten all files to root
Settings:
Minimum image dimensions for "small"



Installation:

```bash
pip install pillow
python gui_main.py
```
