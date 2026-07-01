import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import config
from modules.handler import FileHandler


class apple:

    def __init__(self, root):
        self.root = root
        self.root.title("Line Geometry Calculator")
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        self.root.resizable(True, True)
    
        self.setup_styles()

        self.start_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.calculation_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.history_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")

        self.setup_start_menu()
        self.setup_calculation_menu()
        self.export_button()

        self.start_menu()

    def setup_styles(self):
        self.style = ttk.Style()

        self.style.configure("TFrame", background=config.background_colour)
        self.style.configure("TFrame", font=config.button_font)

        self.style.configure("TLabel", font=config.normal_font, background=config.background_colour)
        self.style.configure("Header.TLabel", font=config.header_font, background=config.background_colour)

    def setup_start_menu(self):
        self.header_title = ttk.Label(
            self.start_frame,
            text="Coordinate Geometry Solver",
            style="Header.TLabel"
        )
        self.header_title.pack(pady=(0, 20))

        self.start_button = ttk.Button(
            self.start_frame,
            text="Start",
            command=self.calculation_menu
        )
        self.start_button.pack(pady=(50))

    def start_menu(self):
        self.calculation_frame.pack_forget()
        self.history_frame.pack_forget()

        self.start_frame.pack(fill=tk.BOTH, expand=True)

    def setup_calculation_menu(self):
        self.calc_title = ttk.Label(
            self.calculation_frame,
            text="Calculation",
            style="Header.TLabel"
        )
        self.calc_title.pack(pady=(0,20))

        self.instructions = ttk.Label(
            self.calculation_frame,
            text="",
            style="TLabel"
        )

    def calculation_menu(self):
        self.start_frame.pack_forget()
        self.history_frame.pack_forget()

        self.calculation_frame.pack(fill=tk.BOTH, expand=True)

    def export_button(self):
        export_button = ttk.Button(
            self.history_frame,
            text="Export History",
            command=self.export_history
        )
        export_button.pack(side=tk.LEFT, padx=5)

    def export_history(self):
        try:
            filename = FileHandler.export_history_to_csv(
                parent_window=self.root
            )
            if filename:
                messagebox.showinfo("Export Successful", f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export History: {str(e)}")