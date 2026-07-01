import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

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
        global coordinate
        lines = [] 
        coordinate = {"x": [], "y": []}
        number = tk.IntVar(value=1)

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
            text="Enter",
            command=get_lines
        )
        self.submit_lines.pack(pady=(0, 70))

        def x_y_start(self):

            amount = lines[0] 

            def y_input():
                user_y_input = self.ycoordinate.get()
                coordinate["y"].extend([user_y_input])
                y_container.pack_forget()
                x_container.pack(pady=(0,40))
                
                current_number = number.get()
                number.set(current_number + 1)
                
                if (int(amount)*2) < int(number.get()):
                    x_container.pack_forget()
                    y_container.pack_forget()
                    x_y_calculation()

            def x_input():
                user_x_input = self.xcoordinate.get()
                coordinate["x"].extend([user_x_input])
                x_container.pack_forget()
                y_container.pack(pady=(0,40))

            x_container = ttk.Frame(self.calculation_frame)
            x_container.pack(pady=(0,40))

            y_container = ttk.Frame(self.calculation_frame)
            y_container.pack(pady=(0,40))

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
                text="Enter",
                command=y_input,
            )
            self.submit_y.pack(pady=(0,80))
            y_container.pack_forget()


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
                text="Enter",
                command=x_input
            )
            self.submit_x.pack(pady=(0,80))

        def x_y_calculation():

            line_results_container = ttk.Frame(self.calculation_frame)
            line_results_container.pack(pady=(0,40))

            line_results_scrollbar = ttk.Scrollbar(line_results_container)
            line_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            line_results_canvas = tk.Canvas(
                line_results_container,
                yscrollcommand=line_results_scrollbar.set,
                highlightthickness=0,
                background=config.background_colour
            )
            line_results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            line_results_scrollbar.config(command=line_results_canvas.yview)

            self.line_frame = ttk.Frame(line_results_canvas, style="TFrame")

            line_results_canvas_frame = line_results_canvas.create_window(
                (0,0),
                window=self.line_frame,
                anchor=tk.NW,
                width=line_results_canvas.winfo_width()
            )

            def configure_line_results_frame(event):
                line_results_canvas.itemconfig(line_results_canvas_frame, width=event.width)
            line_results_canvas.bind('<Configure>', configure_line_results_frame)

            def configure_line_scrollbar(event):
                line_results_canvas.configure(scrollregion=line_results_canvas.bbox("all"))
            self.line_frame.bind('<Configure>', configure_line_scrollbar)

            self.end_line_results()
    
    def end_line_results(self):
        global coordinate
        
        print(coordinate)

        x = coordinate["x"]
        y = coordinate["y"]
        x_iter = iter(x)
        y_iter = iter(y)
        
        def x_y_coords():
            x1 = next(x_iter)
            x2 = next(x_iter)
            y1 = next(y_iter)
            y2 = next(y_iter)
            return x1, x2, y1, y2
        x1, x2, y1, y2 = x_y_coords()

        for widget in self.line_frame.winfo_children():
            widget.destory()

        for x, y in enumerate(coordinate):
            results_frame = ttk.Frame(self.line_frame, style="TFrame")
            results_frame.pack(fill=tk.X, pady=5, padx=10)

            line_name = ttk.Label(
                results_frame,
                text="Line One",
                font=("Ariel", 14, "bold"),
                style="TLabel"
            )
            line_name.pack(anchor=tk.W)

            line_x = ttk.Label(
                results_frame,
                text=x1,
                font=("Ariel", 14, "bold"),
                style="TLabel"
            )
            line_x.pack(anchor=tk.W)

            line_y = ttk.Label(
                results_frame,
                text=y1,
                font=("Ariel", 14, "bold"),
                style="TLabel"
            )
            line_y.pack(anchor=tk.W)

            if x < len(coordinate["x"]) - 1:
                seperator = ttk.Separator(self.line_frame, orient=tk.HORIZONTAL)
                seperator.pack(fill=tk.X, pady=5, padx=10)

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