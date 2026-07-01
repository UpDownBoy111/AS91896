import tkinter as tk
from modules.apple import apple

def main():
    root = tk.Tk()

    pear = apple(root)
    root.mainloop()

if __name__ == "__main__":
    main()