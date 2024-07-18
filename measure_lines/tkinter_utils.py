import tkinter as tk
from tkinter import filedialog
from datetime import datetime 

# FD. save_as_dialog()
# purp. set the folder to store the measurement's output
def save_as_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        open(file_path.split("//")[-1],"w").close()
        print(f"File will be saved to: {file_path}")
        return file_path
        # You can now use file_path to save the file
    else:
        print("Save dialog was canceled.")

def get_formatted_timestamp():
    now = datetime.now()
    formatted_time = now.strftime("%Y_%m_%d\t%H:%M")
    return formatted_time

if __name__ == "__main__":
    save_as_dialog()