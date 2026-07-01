import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

import config
from modules.handler import FileHandler

class apple: 

    class WrappingLabel(tk.Label):
        def __init__(self, master=None, **kwargs):
            tk.Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

    def __init__(self, root):
        self.root = root
        self.root.title("Line Geometry Calculator")
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        self.root.resizable(True, True)
    
        self.setup_styles()

        self.coordinate = {"x": [], "y": []}
        self.lines = []
        self.amount = self.lines

        self.start_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.calculation_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.history_frame = ttk.Frame(self.calculation_frame)

        self.setup_start_menu()
        self.setup_calculation_menu()

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
        
        number = tk.IntVar(value=1)
        
        self.calc_title = ttk.Label(
            self.calculation_frame,
            text="Calculation",
            style="Header.TLabel"
        )
        self.calc_title.pack(pady=(0,20))

        export_button = ttk.Button(
            self.history_frame,
            text="Export History",
            command=self.export_history
        )
        export_button.pack(side=tk.LEFT, pady=5)

        restart_button = ttk.Button(
            self.history_frame,
            text="Restart Calculator",
            command=self.restart_button
        )
        restart_button.pack(side=tk.LEFT, pady=5)

        def get_lines(event=None):
            
            user_input_line = self.amount_of_lines.get()
            try:
                if int(user_input_line) > 0:
                    self.lines.append(user_input_line)
                    self.lines_container.destroy()
                    valid_amount_frame.destroy()
                    valid_amount_zero_frame.destroy()
                    x_y_start(self)
                    self.xcoordinate.focus()
                else:
                    valid_amount_frame.pack_forget()
                    valid_amount_zero_frame.pack(pady=(0,80))

            except ValueError:
                valid_amount_zero_frame.pack_forget()
                valid_amount_frame.pack_forget()
                valid_amount_frame.pack(pady=(0,80))

        valid_amount_frame = ttk.Frame(self.calculation_frame)
        valid_amount_zero_frame = ttk.Frame(self.calculation_frame)

        self.not_integer = ttk.Label(
            valid_amount_frame,
            text="Please enter valid integer.",
            style="TLabel"
        )
        self.not_integer.pack(pady=(0,90))

        self.not_integer_zero = ttk.Label(
            valid_amount_zero_frame,
            text="Please enter valid integer above '0'.",
            style="TLabel"
        )
        self.not_integer_zero.pack(pady=(0,90))

        self.lines_container = ttk.Frame(self.calculation_frame)
        self.instructions = ttk.Label(
            self.lines_container,
            text="How many lines do you want to solve?",
            style="TLabel"
        )
        self.instructions.pack(pady=(0,40))
            
        self.amount_of_lines = ttk.Entry(
            self.lines_container,
        )
        self.amount_of_lines.pack(pady=(0,60))
        self.submit_lines = ttk.Button(
            self.lines_container,
            text="Enter",
            command=get_lines
        )
        self.submit_lines.pack(pady=(0, 70))
        
        self.amount_of_lines.bind('<Return>', get_lines)
        
        def x_y_start(self):
            
            valid_number_frame = ttk.Frame(self.calculation_frame)
            
            self.not_valid_number = ttk.Label(
                valid_number_frame,
                text="Please enter valid integer.",
                style="TLabel"
            )
            self.not_valid_number.pack(pady=(0,90))

            def user_valid_number(prompt):
                try:
                    return float(prompt)
                except ValueError:
                    valid_number_frame.pack_forget()
                    valid_number_frame.pack(pady=(0,80))


            def y_input(event=None):
                user_y_input = self.ycoordinate.get()
                if user_valid_number(user_y_input):
                    valid_number_frame.pack_forget()
                    self.coordinate["y"].extend([float(user_y_input)])
                    y_container.pack_forget()
                    x_container.pack(pady=(0,40))
                    current_number = number.get()
                    number.set(current_number + 1)
                    self.xcoordinate.focus_set()
                    self.ycoordinate.delete(0, 'end')

                if (int(self.amount[0])*2) < int(number.get()):
                    x_container.destroy()
                    y_container.destroy()
                    calculation_results()

            def x_input(event=None):
                user_x_input = self.xcoordinate.get()
                if user_valid_number(user_x_input):
                    valid_number_frame.pack_forget()
                    self.coordinate["x"].extend([float(user_x_input)])
                    x_container.pack_forget()
                    y_container.pack(pady=(0,40))
                    self.ycoordinate.focus_set()
                    self.xcoordinate.delete(0, 'end')

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

            self.xcoordinate.bind('<Return>', x_input)
            self.ycoordinate.bind('<Return>', y_input)

        def calculation_results():
            
            self.history_frame.pack(pady=(0,10))
            line_results_container = ttk.Frame(self.calculation_frame)
            line_results_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            line_results_scrollbar = ttk.Scrollbar(line_results_container)
            line_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            line_results_canvas = tk.Canvas(
                line_results_container,
                yscrollcommand=line_results_scrollbar.set,
                highlightthickness=0,
                background=config.background_colour
            )
            line_results_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, )

            line_results_scrollbar.config(command=line_results_canvas.yview)

            self.line_frame = ttk.Frame(line_results_canvas, style="TFrame")

            line_results_canvas_frame = line_results_canvas.create_window(
                (0,0),
                window=self.line_frame,
                anchor=tk.NW,
                width=line_results_canvas.winfo_width(),
            )

            def configure_line_results_frame(event):
                line_results_canvas.itemconfig(line_results_canvas_frame, width=event.width)
            line_results_canvas.bind('<Configure>', configure_line_results_frame)

            def configure_line_scrollbar(event):
                line_results_canvas.configure(scrollregion=line_results_canvas.bbox("all"))
            self.line_frame.bind('<Configure>', configure_line_scrollbar)
            
            self.end_line_results()

    def end_line_results(self):
        number = 1
        x = self.coordinate["x"]
        y = self.coordinate["y"]
        x_iter = iter(x)
        y_iter = iter(y)

        def x_y_coords():
            x_coord1 = next(x_iter)
            x_coord2 = next(x_iter)
            y_coord1 = next(y_iter)
            y_coord2 = next(y_iter)
            return x_coord1, x_coord2, y_coord1, y_coord2
        
        def calc():
            x_coord1, x_coord2, y_coord1, y_coord2 = x_y_coords()
            distance = round(float(math.sqrt((x_coord2 - x_coord1)**2 + (y_coord2 - y_coord1)**2)), 2)
            if x_coord1 == x_coord2 or y_coord1 == y_coord2:
                gradient = 0
            else:
                gradient = round(float(y_coord2 - y_coord1)/ (x_coord2 - x_coord1), 4)
            midpointx = round(float((x_coord1 + x_coord2)/2), 2)
            midpointy= round(float((y_coord1 + y_coord2)/2), 2)
            c = round(float(y_coord1 - round(float(gradient * x_coord1), 2)), 2)
            return x_coord1, x_coord2, y_coord1, y_coord2, distance, gradient, midpointx, midpointy, c

        while int(self.amount[0]) >= number:
            x_coord1, x_coord2, y_coord1, y_coord2, distance, gradient, midpointx, midpointy, c = calc()
            self.results_frame = ttk.Frame(self.line_frame, style="TFrame")
            self.results_frame.pack(fill=tk.X, pady=5, padx=10)

            line_name = self.WrappingLabel(
                self.results_frame,
                text=f"Line {number}",
                font=("Ariel", 14, "bold")
            )
            line_name.pack(anchor=tk.W, expand=True, fill=tk.X)

            line_calculations = self.WrappingLabel(
                self.results_frame,
                text=f"Coordinates 1: ({x_coord1}, {y_coord1})\nCoordinates 2: ({x_coord2}, {y_coord2})\nGradient: {gradient}\nDistance: {distance}\nMidpoint: ({midpointx}, {midpointy})\nEquation of the line: y={gradient}x+{c}",
                font=("Ariel", 14,)
            )
            line_calculations.pack(anchor=tk.W, expand=True, fill=tk.X)
            
            while True:
                try:
                    if int(self.amount[0]) >= 2:
                        seperator = ttk.Separator(self.line_frame, orient=tk.HORIZONTAL)
                        seperator.pack(fill=tk.X, pady=5, padx=10)
                        break
                    else:
                        break
                except ValueError:
                    print("ERROR")
            number += 1

    def calculation_menu(self):
        self.start_frame.pack_forget()
        self.history_frame.pack_forget()
        
        self.calculation_frame.pack(fill=tk.BOTH, expand=True)
        self.lines_container.pack(pady=(0,40))
        self.amount_of_lines.focus_set()

    def export_history(self):
        try:
            filename = FileHandler.export_history_to_csv(
                self.amount[0],
                self.coordinate,
            )
            if filename:
                messagebox.showinfo("Export Successful", f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export History: {str(e)}")
    
    def restart_button(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        apple(self.root)