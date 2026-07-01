import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path
import math
import random
import os

import config
from modules.handler import FileHandler

class apple: 

    class WrappingLabel(tk.Label):
        def __init__(self, master=None, **kwargs):
            tk.Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), font=config.normal_font, background=config.background_colour))
    
    class WrappingHeader(tk.Label):
        def __init__(self, master=None, **kwargs):
            tk.Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), font=config.header_font, background=config.background_colour))

    def __init__(self, root):
        self.root = root
        self.root.title("Line Geometry Calculator")
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        self.root.resizable(True, True)
    
        self.setup_styles()

        self.coordinate = {"x": [], "y": []}
        self.lines = []
        self.amount = self.lines

        self.line_image = "Line_Example.png"
        self.image_path = os.path.join(config.image_dir, self.line_image)

        self.start_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.calculation_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.line_canvas = tk.Canvas(self.calculation_frame, bg=config.line_result_colour, scrollregion=(10000, 10000, -10000, -10000), width=200, height=300)
        self.history_frame = ttk.Frame(self.calculation_frame)
        self.line_image_frame = tk.Frame(self.calculation_frame)

        self.setup_start_menu()
        self.setup_calculation_menu()

        self.start_menu()

    def setup_styles(self):
        self.style = ttk.Style()

        self.style.configure("TFrame", background=config.background_colour)
        self.style.configure("TFrame", font=config.button_font)

    def setup_start_menu(self):
        self.header_title = self.WrappingHeader(
            self.start_frame,
            text="Coordinate Geometry Solver",
        )
        self.header_title.pack(pady=(0, 20), fill=tk.X)

        self.start_description = self.WrappingLabel(
            self.start_frame,
            text="This is a line calculator, it calculates the distance, midpoint, gradient, and equation of your line, it draws each line in a different colour on a grid once finished.",
        )
        self.start_description.pack(pady=(0, 20), fill=tk.X)

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
        
        self.calc_title = self.WrappingHeader(
            self.calculation_frame,
            text="Calculation",
        )
        self.calc_title.pack(pady=(0,20), fill=tk.X)

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
                    self.lines_container.pack_forget()
                    valid_amount_frame.pack_forget()
                    valid_amount_zero_frame.pack_forget()
                    self.line_image_frame.pack_forget()
                    x_y_start(self)
                    self.xcoordinate.focus()
                    self.line_image_frame.pack(fill="both")
                else:
                    valid_amount_frame.pack_forget()
                    valid_amount_zero_frame.pack(fill="both")

            except ValueError:
                valid_amount_zero_frame.pack_forget()
                valid_amount_frame.pack_forget()
                valid_amount_frame.pack(fill="both")

        valid_amount_frame = ttk.Frame(self.calculation_frame)
        valid_amount_zero_frame = ttk.Frame(self.calculation_frame)

        self.not_integer = self.WrappingLabel(
            valid_amount_frame,
            text="Please enter valid integer.",
        )
        self.not_integer.pack(fill=tk.X)

        self.not_integer_zero = self.WrappingLabel(
            valid_amount_zero_frame,
            text="Please enter valid integer above '0'.",
        )
        self.not_integer_zero.pack(fill=tk.X)

        self.lines_container = ttk.Frame(self.calculation_frame)
        
        self.instructions = self.WrappingLabel(
            self.lines_container,
            text="How many lines do you want to solve?\n Each line requires 2 points.",
        )
        self.instructions.pack(pady=(0,30), fill=tk.X)
            
        self.amount_of_lines = ttk.Entry(
            self.lines_container,
        )
        self.amount_of_lines.pack(pady=(0,30))
        self.submit_lines = ttk.Button(
            self.lines_container,
            text="Enter",
            command=get_lines
        )
        self.submit_lines.pack()
        
        self.amount_of_lines.bind('<Return>', get_lines)

        self.example_line = self.WrappingLabel(
            self.line_image_frame,
            text="Example Line:"
        )
        self.example_line.pack(fill=tk.X)

        if os.path.exists(self.image_path):
            real_line_image = tk.PhotoImage(file=self.image_path)
            self.image_line = tk.Label(self.line_image_frame, image=real_line_image)
            self.image_line.image = real_line_image
            self.image_line.pack()

        def x_y_start(self):
            self.line_number = tk.IntVar(value=1)
            self.coordinate_increase = tk.IntVar(value=0)
            coordinate_point = tk.IntVar(value=1)
            valid_number_frame = ttk.Frame(self.calculation_frame)
            
            self.not_valid_number = self.WrappingLabel(
                valid_number_frame,
                text="Please enter valid integer.",
            )
            self.not_valid_number.pack(fill=tk.X)

            def reset_image():
                self.line_image_frame.pack_forget()
                self.line_image_frame.pack(fill="both")
                self.ycoordinate.focus_set()
                self.xcoordinate.focus_set()

            def back_button_x():
                valid_number_frame.pack_forget()
                if self.coordinate["y"]:
                    self.coordinate["y"].pop()
                    if int(self.line_number.get()) >= 2:
                        if int(coordinate_point.get()) == 2:
                            coordinate_point.set(coordinate_point.get() - 1)
                            number.set(number.get() - 1)
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                            x_container.pack_forget()
                            y_container.pack(fill="both")
                            reset_image()
                        elif int(coordinate_point.get()) == 1:
                            self.line_number.set(self.line_number.get() - 1)
                            self.coordinate_increase.set(self.coordinate_increase.get() - 2)
                            number.set(number.get() - 1)
                            coordinate_point.set(coordinate_point.get() + 1)
                            x_container.pack_forget()
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), ({self.coordinate["x"][int(self.coordinate_increase.get())+1]}, y)")
                            y_container.pack(fill="both")
                            reset_image()
                        
                    elif self.coordinate:
                        x_container.pack_forget()
                        if int(coordinate_point.get()) == 2:
                            coordinate_point.set(coordinate_point.get() - 1)
                            number.set(number.get() - 1)
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                        else:
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                        y_container.pack(fill="both")
                        reset_image()
                else:
                    x_container.pack_forget()
                    y_container.pack_forget()
                    self.lines.clear()
                    self.lines_container.pack(fill="both")
                    self.amount_of_lines.delete(0, 'end')
                    reset_image()
                    self.amount_of_lines.focus_set()

            def back_button_y():
                valid_number_frame.pack_forget()
                if self.coordinate["x"]:
                    self.coordinate["x"].pop()
                    if int(self.line_number.get()) >= 2:
                        if int(coordinate_point.get()) == 2:
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                            y_container.pack_forget()
                            x_container.pack(fill="both")
                            reset_image()
                        else:
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                            y_container.pack_forget()
                            x_container.pack(fill="both")
                            reset_image()
                    elif int(self.line_number.get()) == 1 and int(coordinate_point.get()) == 2:
                        y_container.pack_forget()
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                        x_container.pack(fill="both")
                        reset_image()
                    elif self.coordinate:
                        y_container.pack_forget()
                        if int(coordinate_point.get()) == 2:
                            coordinate_point.set(coordinate_point.get() - 1)
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                        else:
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                        x_container.pack(fill="both")
                        reset_image()

            def user_valid_number(prompt):
                try:
                    return float(prompt)
                except ValueError:
                    valid_number_frame.pack_forget()
                    valid_number_frame.pack(pady=(0,80), fill=tk.X)

            def y_input(event=None):
                user_y_input = self.ycoordinate.get()
                result = user_valid_number(user_y_input)
                if result is not None:
                    valid_number_frame.pack_forget()
                    self.coordinate["y"].extend([float(user_y_input)])
                    y_container.pack_forget()
                    x_container.pack(fill="both")
                    number.set(number.get() + 1)
                    reset_image()
                    self.ycoordinate.delete(0, 'end')
                
                    if int(coordinate_point.get()) >= 2:
                        self.line_number.set(self.line_number.get() + 1)
                        self.coordinate_increase.set(self.coordinate_increase.get() + 2)
                        coordinate_point.set(coordinate_point.get() - 1)
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                    else:
                        coordinate_point.set(coordinate_point.get() + 1)
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")

                if (int(self.amount[0])*2) < int(number.get()):
                    x_container.destroy()
                    y_container.destroy()
                    self.line_image_frame.pack_forget()
                    calculation_results()

            def x_input(event=None):
                user_x_input = self.xcoordinate.get()
                result = user_valid_number(user_x_input)
                if result is not None:
                    valid_number_frame.pack_forget()
                    self.coordinate["x"].extend([float(user_x_input)])
                    x_container.pack_forget()
                    y_container.pack(fill="both")
                    if int(coordinate_point.get()) >= 2:
                        self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), ({self.coordinate["x"][int(self.coordinate_increase.get())+1]}, y)")
                    else:
                        self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current Points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                    reset_image()
                    self.xcoordinate.delete(0, 'end')

            x_container = ttk.Frame(self.calculation_frame)
            x_container.pack(fill="both")
            
            y_container = ttk.Frame(self.calculation_frame)
            y_container.pack(fill="both")

            self.x_back_button = ttk.Button(
                x_container,
                text="Back",
                command=back_button_x
            )
            self.x_back_button.pack()

            self.y_back_button = ttk.Button(
                y_container,
                text="Back",
                command=back_button_y
            )
            self.y_back_button.pack()

            self.yinstructions = self.WrappingLabel(
                y_container,
                text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current Points: (x, y), (x, y)",
            )
            self.yinstructions.pack(pady=(0,20), fill=tk.X)

            self.ycoordinate = ttk.Entry(
                y_container,
            )
            self.ycoordinate.pack(pady=(0,20))

            self.submit_y = ttk.Button(
                y_container,
                text="Enter",
                command=y_input,
            )
            self.submit_y.pack()
            y_container.pack_forget()

            self.xinstructions = self.WrappingLabel(
                x_container,
                text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current Points: (x, y), (x, y)",
            )
            self.xinstructions.pack(pady=(0,20), fill=tk.X)
            
            self.xcoordinate = ttk.Entry(
                x_container,
            )
            self.xcoordinate.pack(pady=(0,20))

            self.submit_x = ttk.Button(
                x_container,
                text="Enter",
                command=x_input
            )
            self.submit_x.pack()

            self.xcoordinate.bind('<Return>', x_input)
            self.ycoordinate.bind('<Return>', y_input)

        def calculation_results():
            self.calc_title.pack_forget()
            
            self.results_title = self.WrappingHeader(
                self.calculation_frame,
                text="Results"
            )
            self.results_title.pack(pady=(0,20), fill=tk.X)

            self.history_frame.pack(pady=(0,10))
            self.line_canvas.pack(fill="both", expand=True)
            self.line_canvas.yview_scroll(+500, "units")
            self.line_canvas.xview_scroll(+67, "pages")
            line_results_container = ttk.Frame(self.calculation_frame)
            line_results_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            line_results_scrollbar = ttk.Scrollbar(line_results_container)
            line_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.line_results_canvas = tk.Canvas(
                line_results_container,
                yscrollcommand=line_results_scrollbar.set,
                highlightthickness=0,
                background=config.background_colour
            )
            self.line_results_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, )

            line_results_scrollbar.config(command=self.line_results_canvas.yview)

            self.line_frame = ttk.Frame(self.line_results_canvas, style="TFrame")

            line_results_canvas_frame = self.line_results_canvas.create_window(
                (0,0),
                window=self.line_frame,
                anchor=tk.NW,
                width=self.line_results_canvas.winfo_width(),
            )

            def configure_line_results_frame(event):
                self.line_results_canvas.itemconfig(line_results_canvas_frame, width=event.width)
            self.line_results_canvas.bind('<Configure>', configure_line_results_frame)

            def configure_line_scrollbar(event):
                self.line_results_canvas.configure(scrollregion=self.line_results_canvas.bbox("all"))
            self.line_frame.bind('<Configure>', configure_line_scrollbar)
            
            self.end_line_results()

    def end_line_results(self):
        number = 1
        x = self.coordinate["x"]
        y = self.coordinate["y"]
        x_iter = iter(x)
        y_iter = iter(y)
        big_number = 100000
        other_lines_number = 1
        lines_number = 100

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
        
        def draw_infinite_line(x_coord1, y_coord1, x_coord2, y_coord2):
            dx = x_coord2 - x_coord1
            dy = -y_coord2 - -y_coord1

            left = -10000
            right = 10000
            top = -10000
            bottom = 10000

            points = []

            if dx != 0:
                t = (left - x_coord1) / dx
                y = -y_coord1 + t * dy
                if top <= y <= bottom:
                    points.append((left, y))

            if dx != 0:
                t = (right - x_coord1) / dx
                y = -y_coord1 + t * dy
                if top <= y <= bottom:
                    points.append((right, y))

            if dy != 0:
                t = (bottom - -y_coord1) / dy
                x = x_coord1 + t * dx
                if left <= x <= right:
                    points.append((x, bottom))

            if dy != 0:
                t = (top + y_coord1) / dy
                x = x_coord1 + t * dx
                if left <= x <= right:
                    points.append((x, top))

            if len(points) >= 2:
                self.line_canvas.create_line(
                    points[0][0], points[0][1],
                    points[1][0], points[1][1],
                    fill=random_hex,
                    width=3
                )
            
            self.line_canvas.create_oval(x_coord1-3, -y_coord1-3, x_coord1+3, -y_coord1+3, fill="red")
            self.line_canvas.create_oval(x_coord2-3, -y_coord2-3, x_coord2+3, -y_coord2+3, fill="red")
        
        def generate_hex():
            return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

        def scroll_start(event):
           self.line_canvas.scan_mark(event.x, event.y)

        def scroll_move(event):
            self.line_canvas.scan_dragto(event.x, event.y, gain=1)

        def on_mousewheel(event):
            self.line_results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.line_canvas.bind("<ButtonPress-1>", scroll_start)
        self.line_canvas.bind("<B1-Motion>", scroll_move)

        self.line_canvas.create_line(0, -big_number, 0, big_number, fill="black", width=3,)
        self.line_canvas.create_line(-big_number, 0, big_number, 0, fill="black", width=3,)

        while 120 >= other_lines_number:
            self.line_canvas.create_line(lines_number, -big_number, lines_number, big_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-big_number, lines_number, big_number, lines_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-lines_number, -big_number, -lines_number, big_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-big_number, -lines_number, big_number, -lines_number, fill="dark gray", width=1,)
            lines_number += 100
            other_lines_number += 1

        while int(self.amount[0]) >= number:
            x_coord1, x_coord2, y_coord1, y_coord2, distance, gradient, midpointx, midpointy, c = calc()
            self.results_frame = ttk.Frame(self.line_frame, style="TFrame")
            self.results_frame.pack(fill=tk.X, pady=5, padx=10)
            self.results_frame.bind_all("<MouseWheel>", on_mousewheel)
            random_hex = generate_hex()
            draw_infinite_line(x_coord1, y_coord1, x_coord2, y_coord2)

            line_name = self.WrappingLabel(
                self.results_frame,
                text=f"Line {number}"
            )
            line_name.pack(anchor=tk.W, expand=True, fill=tk.X)

            line_calculations = self.WrappingLabel(
                self.results_frame,
                text=f"Coordinates 1: ({x_coord1}, {y_coord1})\nCoordinates 2: ({x_coord2}, {y_coord2})\nGradient: {gradient}\nDistance: {distance}\nMidpoint: ({midpointx}, {midpointy})\nEquation of the line: y={gradient}x+{c}", 
            )
            line_calculations.pack(anchor=tk.W, expand=True, fill=tk.X)

            line_colour_text = self.WrappingLabel(
                self.results_frame,
                text="Line Colour",
                foreground=random_hex,
            )
            line_colour_text.pack(anchor=tk.W, expand=True, fill=tk.X)

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
        self.lines_container.pack(pady=(0,40), fill="both")
        self.line_image_frame.pack()
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