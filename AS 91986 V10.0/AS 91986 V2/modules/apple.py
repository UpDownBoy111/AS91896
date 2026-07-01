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
        lines = []

        self.calc_title = ttk.Label(
            self.calculation_frame,
            text="Calculation",
            style="Header.TLabel"
        )
        self.calc_title.pack(pady=(0,20))

        def get_lines():
            user_input_line = self.amount_of_lines.get()
            lines.append(user_input_line)
            lines_container.destroy()
            x_y_start(self)

        lines_container = ttk.Frame(self.calculation_frame)
        lines_container.pack(pady=(0,40))
        self.instructions = ttk.Label(
            lines_container,
            text="How many lines do you want to solve?",
            style="TLabel"
        )
        self.instructions.pack(pady=(0,40))
            
        self.amount_of_lines = ttk.Entry(
            lines_container,
        )
        self.amount_of_lines.pack(pady=(0,60))
            
        self.submit_lines = ttk.Button(
            lines_container,
            command=get_lines
        )
        self.submit_lines.pack(pady=(0, 70))

        def x_y_start(self):
            coordinate = {"x": [], "y": []}
            for n in lines:
                number = n
            x = coordinate["x"]
            y = coordinate["y"]
            x_iter = iter(x)
            y_iter = iter(y)
            
            x_container = ttk.Frame(self.calculation_frame)
            x_container.pack(pady=(0,40))

            y_container = ttk.Frame(self.calculation_frame)
            y_container.pack(pady=(0,40))

            def x_input():
                user_x_input = self.xcoordinate.get()
                x_container.destroy()
                
                self.yinstructions = ttk.Label(
                    y_container,
                    text="Please input 'Y' coordinate",
                    style="TLabel"
                )
                self.yinstructions.pack(pady=(0,40))

                self.ycoordinate = ttk.Entry(
                    y_container,
                )
                self.ycoordinate.pack(pady=(0,60))

                self.submit_y = ttk.Button(
                    y_container,
                    command=x_input
                )
                self.submit_y.pack(pady=(0,80))

            self.xinstructions = ttk.Label(
                x_container,
                text="Please input 'X' coordinate",
                style="TLabel"
            )
            self.xinstructions.pack(pady=(0,40))
            
            self.xcoordinate = ttk.Entry(
                x_container,
            )
            self.xcoordinate.pack(pady=(0,60))

            self.submit_x = ttk.Button(
                x_container,
                command=x_input
            )
            self.submit_x.pack(pady=(0,80))

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