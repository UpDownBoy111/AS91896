"""
Coordinate Geometry Solver Calculator
This file handles file operations for the calculator
"""

import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import math


class FileHandler:
    """
    Class for handling file operations in the calculator
    Manages saving and exporting history data
    """


    def export_history_to_csv(amount: int, coordinate: dict, parent_window = None):
        """
        Export calculation history to a csv file with file dialog for selecting location

        Args:
            amount (int): The amount of lines from the user
            coordinate (dict): The coordinate points from the user
            parent_window (tk.Tk, optional): Parent window for the fial dialog
        
        Returns:
            str: The filename the history were exported to, or None if cancelled
        """

        # Initalise variables
        number = 1
        x = coordinate["x"]
        y = coordinate["y"]
        x_iter = iter(x)
        y_iter = iter(y)
        
        # Updates the next value in coordiate
        def x_y_coords():
            x_coord1 = next(x_iter)
            x_coord2 = next(x_iter)
            y_coord1 = next(y_iter)
            y_coord2 = next(y_iter)
            return x_coord1, x_coord2, y_coord1, y_coord2

        #Creates variables for calculation output
        def calc():
            
            # Initialises variables
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

        # Create default filename
        default_filename = f"Calculation_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Open fial dialog to let user choose the file location
        filename = filedialog.asksaveasfilename(
            parent=parent_window,
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="History"
        )

        # If user cancels dialog, return None
        if not filename:
            return None
        
        try:
            # Write CSV file
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Write Header
                writer.writerow([f"Calculation History"])
                
                while int(amount) >= number:
                    try:
                        # Get variables for calculation history
                        x_coord1, x_coord2, y_coord1, y_coord2, distance, gradient, midpointx, midpointy, c = calc()
                        
                        # Write calculation history in detail
                        writer.writerow([f"Line Number", f"{number}"])
                        writer.writerow([f"Coordinate One: ({x_coord1} {y_coord1})"])
                        writer.writerow([f"Coordinate Two: ({x_coord2} {y_coord2})"])
                        writer.writerow([])
                        writer.writerow([f"Gradient: {gradient}"])
                        writer.writerow([f"Distance: {distance}"])
                        writer.writerow([f"Midpoint: ({midpointx} {midpointy})"])
                        writer.writerow([f"Equation of the line: y = {gradient}x + {c}"])
                        writer.writerow([])
                        
                        # Add 1 till loop stop
                        number += 1
                    
                    except Exception as e:
                        # Raise exception if error occurs
                        raise Exception(f"Failed to export history: {str(e)}")
            
            # Return CSV filename
            return filename
        except Exception as e:
            # Raise exception if error occurs
            raise Exception(f"Failed to export history: {str(e)}")