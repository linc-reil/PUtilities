"""
PUtilties is a Utilities Workspace designed to make schoolwork and calculations as efficient as possible.
Created using Python and tkinter. PUtilities is designed not to use any external packages not native to a 
default python installation.
"""

import os, datetime
from tkinter import messagebox

try:
    from classes.Window import Window
except ImportError:
    messagebox.showerror("Fatal Error!", "Could not resolve import 'Window' from classes. Please reinstall.")

__filepath__ = os.path.abspath(os.path.dirname(__file__))
try:
    with open(__filepath__ + "/config/errorlog.md", "w") as f:
        f.write("# PUtilities Error Log\n\n")
        f.write("## Session Details\n")
        f.write(f"- Date: {datetime.datetime.now().strftime('%d/%m/%Y')}\n")
        f.write(f"- Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n")
        f.write("## Error Log\n")
except:
    messagebox.showwarning("Warning", "Could not create error log. Session will continue, but errors will not be recorded.")

def main() -> None:
    program = Window(__filepath__)
    program.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        messagebox.showerror("Fatal Error!", "Could not create PUtilities window. Please check installation. Error type: " + str(e))
