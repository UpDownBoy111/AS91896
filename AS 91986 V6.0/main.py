import tkinter as tk
from modules.apple import apple

def main():
    root = tk.Tk()

    apple_pie = apple(root)
    root.mainloop()

if __name__ == "__main__":
    main()