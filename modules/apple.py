"""
Coordinate Geometry Solver Calculator
This file contains the main class that manages the calculator
"""
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
    """
    Main class that manages the calculator
    """

    class WrappingLabel(tk.Label):
        """
        Class that allows normal labels to wrap from resizing the window
        """

        # Initalise the wrapping of the text through the class
        def __init__(self, master=None, **kwargs):
            tk.Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), font=config.normal_font, background=config.background_colour))
    
    class WrappingHeader(tk.Label):
        """
        Class that allows header labels to wrap from resizing the window
        """

        # Initalise the wrapping of the text through the class
        def __init__(self, master=None, **kwargs):
            tk.Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), font=config.header_font, background=config.background_colour))

    def __init__(self, root):
        """
        Initialise the calculator
        """

        # Set up the main window configuration
        self.root = root
        self.root.title("Line Geometry Calculator")
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        self.root.resizable(True, True)

        # Set up main styles
        self.setup_styles()

        # Initialise variables
        self.coordinate = {"x": [], "y": []}
        self.lines = []
        self.amount = self.lines

        # Initialise pathing for images
        self.line_image = "Line_Example.png"
        self.image_path = os.path.join(config.image_dir, self.line_image)

        # Create frames for different menus
        self.start_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.calculation_frame = ttk.Frame(self.root, padding=config.padding, style="TFrame")
        self.line_canvas = tk.Canvas(self.calculation_frame, bg=config.line_result_colour, scrollregion=(10000, 10000, -10000, -10000), width=200, height=300)
        self.history_frame = ttk.Frame(self.calculation_frame)
        self.line_image_frame = tk.Frame(self.calculation_frame)

        #Initialise UI
        self.setup_start_menu()
        self.setup_calculation_menu()

        # Show start menu
        self.start_menu()

    def setup_styles(self):
        """Set up styles"""
        self.style = ttk.Style()

        # Configure frame style with background colour
        self.style.configure("TFrame", background=config.background_colour)

        # Configure button style with font
        self.style.configure("TFrame", font=config.button_font)

    def setup_start_menu(self):
        """Set up start menu"""

        # Create header with instructions
        self.header_title = self.WrappingHeader(
            self.start_frame,
            text="Coordinate Geometry Solver",
        )
        self.header_title.pack(pady=(0, 20), fill=tk.X)

        # Add instructions for the user
        self.start_description = self.WrappingLabel(
            self.start_frame,
            text="This is a line calculator, it calculates the distance, midpoint, gradient, and equation of your line, it draws each line in a different colour on a grid once finished.",
        )
        self.start_description.pack(pady=(0, 20), fill=tk.X)

        # Creates a button to go to calculation menu
        self.start_button = ttk.Button(
            self.start_frame,
            text="Start",
            command=self.calculation_menu
        )
        self.start_button.pack(pady=(50))

    def start_menu(self):
        """Displays start menu and hide other menus"""
        
        # Hide other menus
        self.calculation_frame.pack_forget()
        self.history_frame.pack_forget()
        
        # Show start menu
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        
    def setup_calculation_menu(self):
        """Set up the calculation menu"""

        # Initalise variable
        number = tk.IntVar(value=1)
        
        # Creates header for calculation menu
        self.calc_title = self.WrappingHeader(
            self.calculation_frame,
            text="Calculation",
        )
        self.calc_title.pack(pady=(0,20), fill=tk.X)

        # Creates button to export history
        export_button = ttk.Button(
            self.history_frame,
            text="Export History",
            command=self.export_history
        )
        export_button.pack(side=tk.LEFT, pady=5)

        # Creates button to restart the main class
        restart_button = ttk.Button(
            self.history_frame,
            text="Restart Calculator",
            command=self.restart_button
        )
        restart_button.pack(side=tk.LEFT, pady=5)

        def get_lines(event=None):
            """Gets the amount of lines from the user"""

            # Initalises variable from user
            user_input_line = self.amount_of_lines.get()
            
            try:
                # Makes sure variable is above 0
                if int(user_input_line) > 0:

                    # Adds to list
                    self.lines.append(user_input_line)

                    # Hides other frames
                    self.lines_container.pack_forget()
                    valid_amount_frame.pack_forget()
                    valid_amount_zero_frame.pack_forget()
                    self.line_image_frame.pack_forget()

                    # Show next frame
                    x_y_start(self)
                    
                    # Focus on entry
                    self.xcoordinate.focus()

                    # Show image
                    self.line_image_frame.pack(fill="both")
                
                else:
                    # Shows error to user
                    valid_amount_frame.pack_forget()
                    valid_amount_zero_frame.pack(fill="both")

            except ValueError:
                # Shows error to user
                valid_amount_zero_frame.pack_forget()
                valid_amount_frame.pack_forget()
                valid_amount_frame.pack(fill="both")

        # Creates frame for error
        valid_amount_frame = ttk.Frame(self.calculation_frame)
        valid_amount_zero_frame = ttk.Frame(self.calculation_frame)

        # Add instructions for invalid integer
        self.not_integer = self.WrappingLabel(
            valid_amount_frame,
            text="Please enter valid integer.",
        )
        self.not_integer.pack(fill=tk.X)

        # Add instrcutions for not above 0
        self.not_integer_zero = self.WrappingLabel(
            valid_amount_zero_frame,
            text="Please enter valid integer above '0'.",
        )
        self.not_integer_zero.pack(fill=tk.X)

        # Creates frame for inital calculation menu
        self.lines_container = ttk.Frame(self.calculation_frame)
        
        # Add instructions
        self.instructions = self.WrappingLabel(
            self.lines_container,
            text="How many lines do you want to solve?\n Each line requires 2 points.",
        )
        self.instructions.pack(pady=(0,30), fill=tk.X)
        
        # Creates entry
        self.amount_of_lines = ttk.Entry(
            self.lines_container,
        )
        self.amount_of_lines.pack(pady=(0,30))

        # Add enter button
        self.submit_lines = ttk.Button(
            self.lines_container,
            text="Enter",
            command=get_lines
        )
        self.submit_lines.pack()
        
        self.amount_of_lines.bind('<Return>', get_lines)

        # Create label for example line
        self.example_line = self.WrappingLabel(
            self.line_image_frame,
            text="Example Line:"
        )
        self.example_line.pack(fill=tk.X)

        # Ensures path for images
        if os.path.exists(self.image_path):
            # Initialise Variables
            real_line_image = tk.PhotoImage(file=self.image_path)
            self.image_line = tk.Label(self.line_image_frame, image=real_line_image)
            
            # Ensures image is not deleted
            self.image_line.image = real_line_image
            
            # Packs image
            self.image_line.pack()

        def x_y_start(self):
            """Display next frame in calculation menu"""
            
            # Initalise variables
            self.line_number = tk.IntVar(value=1)
            self.coordinate_increase = tk.IntVar(value=0)
            coordinate_point = tk.IntVar(value=1)
            valid_number_frame = ttk.Frame(self.calculation_frame)
            
            # Adds instructions for invalid integer
            self.not_valid_number = self.WrappingLabel(
                valid_number_frame,
                text="Please enter valid integer.",
            )
            self.not_valid_number.pack(fill=tk.X)

            def reset_image():
                """Resets line image"""

                self.line_image_frame.pack_forget()
                self.line_image_frame.pack(fill="both")
                self.ycoordinate.focus_set()
                self.xcoordinate.focus_set()

            def back_button_x():
                """Sets back to previous update"""

                # Hides frame
                valid_number_frame.pack_forget()

                if self.coordinate["y"]:
                    # Removes "y" value
                    self.coordinate["y"].pop()
                    
                    if int(self.line_number.get()) >= 2:
                        if int(coordinate_point.get()) == 2:
                            
                            # Updates variables
                            coordinate_point.set(coordinate_point.get() - 1)
                            number.set(number.get() - 1)
                            
                            # Updates display to previous state
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                            
                            # Hides frame
                            x_container.pack_forget()
                            
                            # Shows next frame
                            y_container.pack(fill="both")
                            
                            reset_image()
                        elif int(coordinate_point.get()) == 1:
                            
                            # Updates variables
                            self.line_number.set(self.line_number.get() - 1)
                            self.coordinate_increase.set(self.coordinate_increase.get() - 2)
                            number.set(number.get() - 1)
                            coordinate_point.set(coordinate_point.get() + 1)
                            
                            # Updates display to previous state
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), ({self.coordinate["x"][int(self.coordinate_increase.get())+1]}, y)")
                            
                            # Hides frame
                            x_container.pack_forget()

                            # Shows next frame
                            y_container.pack(fill="both")
                            
                            reset_image()                       
                    elif self.coordinate:
                        
                        # Hides frame
                        x_container.pack_forget()
                        
                        if int(coordinate_point.get()) == 2:
                            
                            # Updates variables
                            coordinate_point.set(coordinate_point.get() - 1)
                            number.set(number.get() - 1)
                            
                            # Updates display to previous state
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                        
                        else:
                            
                            # Updates display to previous state
                            self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                        
                        # Shows next frame
                        y_container.pack(fill="both")
                        
                        reset_image()
                else:
                    
                    # Hides frames
                    x_container.pack_forget()
                    y_container.pack_forget()
                    
                    # Updates lines variable
                    self.lines.clear()

                    # Shows previous frame
                    self.lines_container.pack(fill="both")
                    self.amount_of_lines.delete(0, 'end')

                    reset_image()

                    # Focus on entry
                    self.amount_of_lines.focus_set()

            def back_button_y():
                """Sets back to previous frame"""

                # Hides frame
                valid_number_frame.pack_forget()
                
                if self.coordinate["x"]:
                    # Removes "x" value
                    self.coordinate["x"].pop()
                    
                    if int(self.line_number.get()) >= 2:
                        if int(coordinate_point.get()) == 2:
                            
                            # Updates display to previous state
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                            
                            # Hides frame
                            y_container.pack_forget()
                            
                            # Shows previous frame
                            x_container.pack(fill="both")
                            
                            reset_image()
                        else:
                            
                            # Updates display to previous state
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                            
                            # Hides frame
                            y_container.pack_forget()
                            
                            # Shows previous frame
                            x_container.pack(fill="both")
                            
                            reset_image()
                    elif int(self.line_number.get()) == 1 and int(coordinate_point.get()) == 2:
                        
                        # Updates display to previous state
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                        
                        # Hides frame
                        y_container.pack_forget()

                        # Shows previous frame
                        x_container.pack(fill="both")
                        
                        reset_image()
                    elif self.coordinate:
                        
                        # Hides frame
                        y_container.pack_forget()

                        if int(coordinate_point.get()) == 2:
                            
                            # Updates variable
                            coordinate_point.set(coordinate_point.get() - 1)

                            # Updates display to previous state
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")
                        
                        else:
                            
                            # Updates display to previous state
                            self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                        
                            # Shows previous frame
                            x_container.pack(fill="both")
                            
                            reset_image()

            # Validates user input
            def user_valid_number(prompt):
                try:

                    # Return float of user input
                    return float(prompt)
                
                except ValueError:

                    # If invalid show instructions
                    valid_number_frame.pack_forget()
                    valid_number_frame.pack(pady=(0,80), fill=tk.X)

            def y_input(event=None):
                """User "y" input"""

                # Initialise variables
                user_y_input = self.ycoordinate.get()
                result = user_valid_number(user_y_input)

                if result is not None:

                    valid_number_frame.pack_forget()

                    # Add user variable to coorinate
                    self.coordinate["y"].extend([float(user_y_input)])

                    # Hide frame
                    y_container.pack_forget()

                    # Show next frame
                    x_container.pack(fill="both")

                    # Update variable
                    number.set(number.get() + 1)

                    reset_image()
                    self.ycoordinate.delete(0, 'end')
                
                    if int(coordinate_point.get()) >= 2:
                        
                        # Update variables
                        self.line_number.set(self.line_number.get() + 1)
                        self.coordinate_increase.set(self.coordinate_increase.get() + 2)
                        coordinate_point.set(coordinate_point.get() - 1)

                        # Update display
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current points: (x, y), (x, y)")
                    
                    else:
                        
                        # Update variable
                        coordinate_point.set(coordinate_point.get() + 1)

                        # Update display
                        self.xinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'X' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), (x, y)")

                if (int(self.amount[0])*2) < int(number.get()):
                    
                    # Destroy current frame
                    x_container.destroy()
                    y_container.destroy()

                    # Hide line image
                    self.line_image_frame.pack_forget()

                    # Show next calculation menu
                    calculation_results()

            def x_input(event=None):
                """User "x" input"""

                # Initialise variables
                user_x_input = self.xcoordinate.get()
                result = user_valid_number(user_x_input)

                if result is not None:

                    valid_number_frame.pack_forget()

                    # Add user variable to coordiante
                    self.coordinate["x"].extend([float(user_x_input)])

                    # Hide frame
                    x_container.pack_forget()

                    # Show next frame
                    y_container.pack(fill="both")

                    if int(coordinate_point.get()) >= 2:

                        # Update display
                        self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}nd 'Y' coordinate for line {int(self.line_number.get())}. Current points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, {self.coordinate["y"][int(self.coordinate_increase.get())]}), ({self.coordinate["x"][int(self.coordinate_increase.get())+1]}, y)")
                    
                    else:
                        
                        # Update display
                        self.yinstructions.config(text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current Points: ({self.coordinate["x"][int(self.coordinate_increase.get())]}, y), (x, y)")
                    
                    reset_image()
                    self.xcoordinate.delete(0, 'end')

            # Creates a frame for x inputs
            x_container = ttk.Frame(self.calculation_frame)
            x_container.pack(fill="both")
            
            # Creates a frame for y inputs
            y_container = ttk.Frame(self.calculation_frame)

            # Add back button for x
            self.x_back_button = ttk.Button(
                x_container,
                text="Back",
                command=back_button_x
            )
            self.x_back_button.pack()

            # Add back button for y
            self.y_back_button = ttk.Button(
                y_container,
                text="Back",
                command=back_button_y
            )
            self.y_back_button.pack()

            # Add display
            self.yinstructions = self.WrappingLabel(
                y_container,
                text=f"Please input {int(coordinate_point.get())}st 'Y' coordinate for line {int(self.line_number.get())}. Current Points: (x, y), (x, y)",
            )
            self.yinstructions.pack(pady=(0,20), fill=tk.X)

            # Creates entry
            self.ycoordinate = ttk.Entry(
                y_container,
            )
            self.ycoordinate.pack(pady=(0,20))

            # Create enter button
            self.submit_y = ttk.Button(
                y_container,
                text="Enter",
                command=y_input,
            )
            self.submit_y.pack()

            # Add display
            self.xinstructions = self.WrappingLabel(
                x_container,
                text=f"Please input {int(coordinate_point.get())}st 'X' coordinate for line {int(self.line_number.get())}. Current Points: (x, y), (x, y)",
            )
            self.xinstructions.pack(pady=(0,20), fill=tk.X)
            
            # Creates entry
            self.xcoordinate = ttk.Entry(
                x_container,
            )
            self.xcoordinate.pack(pady=(0,20))

            # Create enter button
            self.submit_x = ttk.Button(
                x_container,
                text="Enter",
                command=x_input
            )
            self.submit_x.pack()

            self.xcoordinate.bind('<Return>', x_input)
            self.ycoordinate.bind('<Return>', y_input)

        def calculation_results():
            """Display next frame in calculation menu"""

            # Hides previous header
            self.calc_title.pack_forget()
            
            # Creates header
            self.results_title = self.WrappingHeader(
                self.calculation_frame,
                text="Results"
            )
            self.results_title.pack(pady=(0,20), fill=tk.X)

            self.history_frame.pack(pady=(0,10))

            # Adds and move canvas
            self.line_canvas.pack(fill="both", expand=True)
            self.line_canvas.yview_scroll(+500, "units")
            self.line_canvas.xview_scroll(+67, "pages")
            
            # Creates frame
            line_results_container = ttk.Frame(self.calculation_frame)
            line_results_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Create scrollbar
            line_results_scrollbar = ttk.Scrollbar(line_results_container)
            line_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create canvas
            self.line_results_canvas = tk.Canvas(
                line_results_container,
                yscrollcommand=line_results_scrollbar.set,
                highlightthickness=0,
                background=config.background_colour
            )
            self.line_results_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, )

            line_results_scrollbar.config(command=self.line_results_canvas.yview)

            # Creates frame
            self.line_frame = ttk.Frame(self.line_results_canvas, style="TFrame")

            # Create window in canvas
            line_results_canvas_frame = self.line_results_canvas.create_window(
                (0,0),
                window=self.line_frame,
                anchor=tk.NW,
                width=self.line_results_canvas.winfo_width(),
            )

            # Makes the canvas resize the frame if the window is resized
            def configure_line_results_frame(event):
                self.line_results_canvas.itemconfig(line_results_canvas_frame, width=event.width)

            self.line_results_canvas.bind('<Configure>', configure_line_results_frame)

            # Update the scroll region if line results frame resizes
            def configure_line_scrollbar(event):
                self.line_results_canvas.configure(scrollregion=self.line_results_canvas.bbox("all"))

            self.line_frame.bind('<Configure>', configure_line_scrollbar)
            
            # Starts filling in results frame
            self.end_line_results()

    def end_line_results(self):
        """Fills results frame with current calculations"""

        # Initialise variables
        number = 1
        x = self.coordinate["x"]
        y = self.coordinate["y"]
        x_iter = iter(x)
        y_iter = iter(y)
        big_number = 100000
        other_lines_number = 1
        lines_number = 100

        # Updates the next value in coordiate
        def x_y_coords():
            x_coord1 = next(x_iter)
            x_coord2 = next(x_iter)
            y_coord1 = next(y_iter)
            y_coord2 = next(y_iter)
            return x_coord1, x_coord2, y_coord1, y_coord2
        
        #Creates variables for calculation output
        def calc():

            # Initalises variables
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
        
        def draw_infinite_line(x_coord1: float, y_coord1: float, x_coord2: float, y_coord2: float):
            """
            Draws line using coordinates from user
            
            Args:
                x_coord1 (float): First x point in line
                y_coord1 (float): First y point in line
                x_coord2 (float): Second x point in line
                y_coord2 (float): Second y point in line
            """

            # Initalise variables
            dx = x_coord2 - x_coord1
            dy = -y_coord2 - -y_coord1
            left = -10000
            right = 10000
            top = -10000
            bottom = 10000
            points = []

            # Find maximum edge of canvas for line using points from the left
            if dx != 0:
                t = (left - x_coord1) / dx
                y = -y_coord1 + t * dy
                if top <= y <= bottom:
                    points.append((left, y))

            # Find maximum edge of canvas for line using points from the right
            if dx != 0:
                t = (right - x_coord1) / dx
                y = -y_coord1 + t * dy
                if top <= y <= bottom:
                    points.append((right, y))

            # Find maximum edge of canvas for line using points from the bottom
            if dy != 0:
                t = (bottom - -y_coord1) / dy
                x = x_coord1 + t * dx
                if left <= x <= right:
                    points.append((x, bottom))

            # Find maximum edge of canvas for line using points from the top
            if dy != 0:
                t = (top + y_coord1) / dy
                x = x_coord1 + t * dx
                if left <= x <= right:
                    points.append((x, top))

            # Creates the the line
            if len(points) >= 2:
                self.line_canvas.create_line(
                    points[0][0], points[0][1],
                    points[1][0], points[1][1],
                    fill=random_hex,
                    width=3
                )
            
            # Creates circles at points on frame
            self.line_canvas.create_oval(x_coord1-3, -y_coord1-3, x_coord1+3, -y_coord1+3, fill="red")
            self.line_canvas.create_oval(x_coord2-3, -y_coord2-3, x_coord2+3, -y_coord2+3, fill="red")
        
        # Generates random colour in hex
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

        # Creates "x" and "y" lines from 0,0
        self.line_canvas.create_line(0, -big_number, 0, big_number, fill="black", width=3,)
        self.line_canvas.create_line(-big_number, 0, big_number, 0, fill="black", width=3,)

        # Creates smallers lines at every 100px intervals
        while 120 >= other_lines_number:
            self.line_canvas.create_line(lines_number, -big_number, lines_number, big_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-big_number, lines_number, big_number, lines_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-lines_number, -big_number, -lines_number, big_number, fill="dark gray", width=1,)
            self.line_canvas.create_line(-big_number, -lines_number, big_number, -lines_number, fill="dark gray", width=1,)
            
            lines_number += 100
            other_lines_number += 1

        while int(self.amount[0]) >= number:
            
            # Initialise variables
            x_coord1, x_coord2, y_coord1, y_coord2, distance, gradient, midpointx, midpointy, c = calc()
            random_hex = generate_hex()

            # Creates frame
            self.results_frame = ttk.Frame(self.line_frame, style="TFrame")
            self.results_frame.pack(fill=tk.X, pady=5, padx=10)
            
            self.results_frame.bind_all("<MouseWheel>", on_mousewheel)
            
            # Draws the line
            draw_infinite_line(x_coord1, y_coord1, x_coord2, y_coord2)

            # Creates title for line
            line_name = self.WrappingLabel(
                self.results_frame,
                text=f"Line {number}"
            )
            line_name.pack(anchor=tk.W, expand=True, fill=tk.X)

            # Creates label for all calculations
            line_calculations = self.WrappingLabel(
                self.results_frame,
                text=f"Coordinates 1: ({x_coord1}, {y_coord1})\nCoordinates 2: ({x_coord2}, {y_coord2})\nGradient: {gradient}\nDistance: {distance}\nMidpoint: ({midpointx}, {midpointy})\nEquation of the line: y={gradient}x+{c}", 
            )
            line_calculations.pack(anchor=tk.W, expand=True, fill=tk.X)

            # Adds label with line colour
            line_colour_text = self.WrappingLabel(
                self.results_frame,
                text="Line Colour",
                foreground=random_hex,
            )
            line_colour_text.pack(anchor=tk.W, expand=True, fill=tk.X)

            while True:
                try:
                    if int(self.amount[0]) >= 2:
                        
                        # Adds break in text
                        seperator = ttk.Separator(self.line_frame, orient=tk.HORIZONTAL)
                        seperator.pack(fill=tk.X, pady=5, padx=10)
                        
                        break
                    else:
                        break
                
                except ValueError as e:
                    print(f"Error seperatoring: {str(e)}")
            number += 1

    def calculation_menu(self):
        """Displays calculation menu"""

        # Hides other menus
        self.start_frame.pack_forget()
        self.history_frame.pack_forget()
        
        # Show menu
        self.calculation_frame.pack(fill=tk.BOTH, expand=True)
        self.lines_container.pack(pady=(0,40), fill="both")
        self.line_image_frame.pack()

        # Focus on entry
        self.amount_of_lines.focus_set()

    def export_history(self):
        """Export calculations to a CSV file"""
        try:
            
            # Export history to a CSV file with a fialdialog
            filename = FileHandler.export_history_to_csv(
                self.amount[0],
                self.coordinate,
            )

            # Check if user cancelled the operation (filname would be None)
            if filename:
                
                # Show success message with the filename
                messagebox.showinfo("Export Successful", f"History exported to {filename}")
        except Exception as e:

            # Show error message if export fails
            messagebox.showerror("Error", f"Failed to export History: {str(e)}")
    
    def restart_button(self):
        """Restarts calculator"""
        
        # Destroys current calculator
        for widget in self.root.winfo_children():
            widget.destroy()

        # Runs main class to restart calculator
        apple(self.root)