import os
import json
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import config

class FileHandler:

    @staticmethod
    def directories_exist():
        directories = [config.data_dir, config.history_dir]
        for dir in directories:
            if not os.path.exists(dir):
                os.makedirs(dir)
    
    @staticmethod
    def save_history():
        FileHandler.directories_exist()
        history_data = {
            "Line": 2,
            "Answer": 3
        }
        filename = f"Calculation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(config.history_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(history_data, f, indent=4)
            return filepath
        except Exception as e:
            raise Exception(f"Failed to save history: {str(e)}")
    
    @staticmethod
    def export_history_to_csv(parent_window = None):
        default_filename = f"Calculation_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filename = filedialog.asksaveasfilename(
            parent=parent_window,
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="History"
        )
        if not filename:
            return None
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["History"])
                writer.writerow(["TEST"])
                writer.writerow([])
            return filename
        except Exception as e:
            raise Exception(f"Failed to export history: {str(e)}")