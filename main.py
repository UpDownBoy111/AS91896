"""
Coordinate Geometry Solver Calculator
This file is the entry point for the calculator
"""

import tkinter as tk
from modules.apple import Apple

def main():
    """
    Main function to intialise and run the calculator
    Create the root Tkinker window and starts calculator
    """
    
    # Create the root window
    root = tk.Tk()

    # Initalise the calculator
    apple_pie = Apple(root)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()