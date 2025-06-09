import os
from datetime import datetime

class ReportWriter:
    def __init__(self, directory):
        self.directory = directory
        self.lines = []

    def add_entry(self, method, file, destination_folder):
        self.lines.append(f"[{method}] {os.path.normpath(file)} → {destination_folder}/")

    def save(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_path = os.path.join(self.directory, "report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Звіт сортування файлів — {timestamp}\n")
            f.write(f"{'-'*50}\n")
            for line in self.lines:
                f.write(line + "\n")
