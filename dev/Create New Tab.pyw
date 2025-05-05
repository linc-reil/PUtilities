"""
PUtilities Tab Creator Utility
Designed for developers of PUtilities to quickly create a new tab.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from string import ascii_lowercase, ascii_uppercase

class CodeMySh1t:
    ind = "    "

    def __init__(self, tab_name: str, class_name: str, tab_description: str, set_name: bool, define_create_widgets: bool, define_tab_commands: bool, define_file_methods: bool):
        self.lines: list[str] = []
        self.tab_name = tab_name
        self.class_name = class_name
        self.tab_description = tab_description
        self.set_name = set_name
        self.define_create_widgets = define_create_widgets
        self.define_tab_commands = define_tab_commands
        self.define_file_methods = define_file_methods
        if not self.tab_description or self.tab_description == "":
            self.tab_description = "No description available."
        self.create()
    
    def add(self, string: str = "") -> None:
        self.lines.append(string)
    
    def add_indent1(self, string: str = "") -> None:
        self.add(self.ind + string)
    
    def add_indent2(self, string: str = "") -> None:
        self.add(self.ind + self.ind + string)

    def create(self) -> None:
        self.add("\"\"\"")
        self.add(f"{self.tab_name} (tab)")
        self.add(self.tab_description)
        self.add("\"\"\"")
        self.add()

        self.add("from classes.Utilities import *")
        self.add()
        self.add(f"class {self.class_name[:-3]}(TabFrame):")
        self.add_indent1(f"_name = \'{self.tab_name}\'")
        self.add_indent1(f"_description = \'{self.tab_description}\'")
        self.add_indent1(f"_icon = \'default_tab_icon.png\'")

        self.add_indent1("def init(self) -> None:")
        if not self.set_name and not self.set_description and not self.define_create_widgets and not self.define_file_methods:
            self.add_indent2("...")
        else:
            if self.set_name: self.add_indent2(f"self.tabname = \"{self.tab_name}\"")
            if self.define_file_methods: self.add_indent2("self.filepath = None")
            if self.define_create_widgets: self.add_indent2("self.create_widgets()")
        self.add_indent1()

        if self.define_create_widgets:
            self.add_indent1("def create_widgets(self) -> None:")
            self.add_indent2("...")
            self.add_indent1()
        
        if self.define_tab_commands:
            self.add_indent1("def createTabCommands(self) -> None:")
            self.add_indent2("...")
            self.add_indent1()
        
        if self.define_file_methods:
            self.add_indent1("def save(self) -> None:")
            self.add_indent2("if not self.filepath:")
            self.add_indent2(self.ind + "self.saveAs()")
            self.add_indent2("return")
            self.add_indent1()
            self.add_indent1("def saveAs(self) -> None:")
            self.add_indent2("if self.filepath: self.save()")
            self.add_indent1()
            self.add_indent1("def open(self) -> None:")
            self.add_indent2("if self.filepath: self.save()")
            self.add_indent1()
            self.add_indent1("def new(self) -> None:")
            self.add_indent2("if self.filepath: self.save()")
            self.add_indent1()
            self.add_indent1("def autoload(self, filepath: str) -> None:")
            self.add_indent2("if not filepath or not os.path.exists(filepath) or not os.path.isfile(filepath): return")
            self.add_indent1()
        
        self.result = "\n".join(self.lines)

class NewTabCreator(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PUtilities Tab Creator")
        self.resizable(False, False)
        self.create_widgets()
        self.tick()
    
    def start(self) -> None:
        self.mainloop()
    
    def tick(self) -> None:
        self.filename = list(self.name_entry.get().strip().title())
        i = 0
        while i < len(self.filename):
            if not self.filename[i] in ascii_lowercase + ascii_uppercase + "0123456789":
                self.filename.pop(i)
                i -= 1
            i += 1
        self.filename = "".join(self.filename) + ".py"
        if self.filename == ".py": self.filename = None
        self.filename_descriptor.config(text=self.filename)

        self.after(10, self.tick)

    def create_widgets(self) -> None:
        self.header = ttk.Label(self, text="Create Tab", font=("Arial", 14))
        self.header.pack(side="top", anchor="n")
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="top", anchor="w", fill="x")
        
        self.name_label = ttk.Label(self.main_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.name_entry = ttk.Entry(self.main_frame, width=35)
        self.name_entry.grid(row=0, column=1, sticky="nw", padx=5, pady=2)

        self.filename_label = ttk.Label(self.main_frame, text="Filename:")
        self.filename_label.grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.filename_descriptor = ttk.Label(self.main_frame, text="")
        self.filename_descriptor.grid(row=1, column=1, sticky="nw", padx=5, pady=2)

        self.set_name = tk.BooleanVar(self, True)
        self.set_name_checkbox = ttk.Checkbutton(self.main_frame, text="Set Tab Name", variable=self.set_name)
        self.set_name_checkbox.grid(row=2, column=0, columnspan=2, sticky="nw", padx=5, pady=2)

        self.define_create_widgets = tk.BooleanVar(self, True)
        self.define_create_widgets_checkbox = ttk.Checkbutton(self.main_frame, text="Define 'create_widgets()' Method", variable=self.define_create_widgets)
        self.define_create_widgets_checkbox.grid(row=4, column=0, columnspan=2, sticky="nw", padx=5, pady=2)

        self.define_tab_commands = tk.BooleanVar(self, False)
        self.define_tab_commands_checkbox = ttk.Checkbutton(self.main_frame, text="Define 'createTabCommands()' Method", variable=self.define_tab_commands)
        self.define_tab_commands_checkbox.grid(row=5, column=0, columnspan=2, sticky="nw", padx=5, pady=2)

        self.define_file_methods = tk.BooleanVar(self, False)
        self.define_file_methods_checkbox = ttk.Checkbutton(self.main_frame, text="Define File Methods", variable=self.define_file_methods)
        self.define_file_methods_checkbox.grid(row=6, column=0, columnspan=2, sticky="nw", padx=5, pady=2)

        self.description_label = ttk.Label(self.main_frame, text="Description:")
        self.description_label.grid(row=8, column=0, columnspan=2, sticky="nw", padx=5, pady=2)
        self.description = tk.Text(self.main_frame, width=35, height=6)
        self.description.grid(row=9, column=0, columnspan=2, sticky="nw", padx=5, pady=2)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side="top", anchor="nw", fill="x")
        self.create_button = ttk.Button(self, text="Create!", command=self.create)
        self.create_button.pack(side="right", anchor="e")
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side="right", anchor="e")
    
    def create(self) -> None:
        if not self.filename: return
        text = CodeMySh1t(self.name_entry.get(), self.filename, self.description.get("1.0", tk.END).strip(),
        self.set_name.get(), self.define_create_widgets.get(),
        self.define_tab_commands.get(), self.define_file_methods.get()).result
        filepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + f"/classes/{self.filename}"
        with open(filepath, "w") as f:
            f.write(text)
        messagebox.showinfo("Success!", "Tab successfully created. Exiting tab creator utility...")
        self.destroy()


if __name__ == "__main__":
    program = NewTabCreator()
    program.start()