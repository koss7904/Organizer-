class FileCategorizer:
    categories = {
        "Документи": [
            '.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx',
            '.ppt', '.pptx', '.csv', '.vsdx', '.odt', '.rtf'
        ],
        "Зображення": [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'
        ],
        "Відео": ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
        "Аудіо": ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
        "Архіви": ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
        "Програми": ['.exe', '.msi', '.bat', '.sh', '.apk'],
        "Код": ['.py', '.java', '.cpp', '.js', '.html', '.css', '.c', '.h'],
        "Google Colab": ['.ipynb'],
        "Інше": []  # Все, що не входить до вказаних вище
    }

    @classmethod
    def get_category(cls, extension):
        for category, extensions in cls.categories.items():
            if extension in extensions:
                return category
        return "Інше"
