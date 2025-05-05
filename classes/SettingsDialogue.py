import tkinter as tk
from tkinter import ttk, filedialog
from classes.Utilities import *

class _settingsPanel(ttk.Frame):
    """Class to inherit from for other settings panels."""
    def __init__(self, master = None, scrollable: bool = False):
        super().__init__(master.configPanel)
        self.window = master
        self._header = ttk.Label(self, text="", font=("Arial", 18))
        self._header.grid(row=0, column=0, sticky="w", columnspan=2, pady=2)
        self.window.configPanel.scrollableWithMouse = scrollable
        self.init()
    
    def init(self) -> None:
        ...
    
    @property
    def header(self) -> None:
        return self._header

    @header.setter
    def header(self, text: str) -> None:
        self._header.config(text=text)
    
    def save(self) -> dict[str: typing.Any]:
        ...

class GeneralSettingsPanel(_settingsPanel):
    def init(self, master=None) -> None:
        self.header = "General Settings"
        self.usernameLabel = ttk.Label(self, text="Username:")
        self.usernameLabel.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.usernameEntry = ttk.Entry(self, width=45)
        self.usernameEntry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.usernameEntry.insert(tk.END, CONFIGURATION.username)

        self.decimalPlacesOptions = ["No Rounding", "0 Decimal Places", "1 Decimal Place", "2 Decimal Places", "3 Decimal Places", "5 Decimal Places"]
        if isinstance(CONFIGURATION.rounding, int):
            self.decimalPlacesVariable = tk.StringVar(self, f"{CONFIGURATION.rounding} Decimal Places")
        else:
            self.decimalPlacesVariable = tk.StringVar(self, "No Rounding")
        self.decimalPlacesLabel = ttk.Label(self, text="Round Answers to:")
        self.decimalPlacesLabel.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.decimalPlacesSelector = ttk.Combobox(self, values=self.decimalPlacesOptions, textvariable=self.decimalPlacesVariable)
        self.decimalPlacesSelector.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        self.angle_measure_options = ["Degrees", "Radians"]
        self.angle_measure_variable = tk.StringVar(self, CONFIGURATION.angle_unit)
        self.angle_measure_label = ttk.Label(self, text="Default angle unit:")
        self.angle_measure_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.angle_measure_selector = ttk.Combobox(self, textvariable=self.angle_measure_variable, values=self.angle_measure_options)
        self.angle_measure_selector.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        self.show_error_windows_variable = tk.BooleanVar(self, CONFIGURATION.show_error_windows)
        self.show_error_windows_selector = ttk.Checkbutton(self, text="Show error windows", variable=self.show_error_windows_variable)
        self.show_error_windows_selector.grid(row=4, column=0, sticky="w", padx=5, pady=2, columnspan=2)

        self.default_tab_options = ["Home Tab", "Text Editor", "Terminal", "Simple Calculator", "Lesson Editor", "File Explorer"]
        _temp = CONFIGURATION.default_tab
        self.default_tab_variable = tk.StringVar(self, _temp)
        self.default_tab_label = ttk.Label(self, text="Default tab:")
        self.default_tab_label.grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.default_tab_selector = ttk.Combobox(self, textvariable=self.default_tab_variable, values=self.default_tab_options)
        self.default_tab_selector.grid(row=5, column=1, sticky="w", padx=5, pady=2)

        self.terminal_prompt_label = ttk.Label(self, text="Terminal Prompt: ")
        self.terminal_prompt_label.grid(row=6, column=0, sticky=tk.NW, padx=5, pady=2)
        self.terminal_prompt_entry = ttk.Entry(self, width=35)
        self.terminal_prompt_entry.grid(row=6, column=1, sticky=tk.NW, padx=5, pady=2)
        self.terminal_prompt_entry.insert(tk.END, CONFIGURATION.terminal_prompt)

    def save(self):
        rounding = None if self.decimalPlacesVariable.get() == "No Rounding" else int(self.decimalPlacesVariable.get()[0])
        return {"username": self.usernameEntry.get().strip(), "rounding": rounding, "angle_unit": self.angle_measure_variable.get(),
                "show_error_windows": self.show_error_windows_variable.get(), "default_tab": self.default_tab_variable.get(),
                "terminalprompt": self.terminal_prompt_entry.get()}

class TerminalSettingsPanel(_settingsPanel):
    def init(self):
        self.header = "Terminal Configuration"
        self.promptLabel = ttk.Label(self, text="Terminal Prompt")
        self.promptLabel.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.promptEntry = ttk.Entry(self, width=45)
        self.promptEntry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.promptEntry.insert(tk.END, CONFIGURATION.terminal_prompt)
    
    def save(self):
        return {"terminalprompt": self.promptEntry.get()}

class MiscellaneousSettingsPanel(_settingsPanel):
    def init(self):
        self.header = "Miscellaneous Settings"
        self.clear_recent_files_button = ttk.Button(self, text="Clear Recent Files", command=self.clear_recent_files)
        self.clear_recent_files_button.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
    
    def clear_recent_files(self) -> None:
        if not messagebox.askokcancel("Confirm", "Recent files will be cleared. Confirm?"): return
        CONFIGURATION._write_value("recent_files", [])

class SubjectEditorPanel(_settingsPanel):
    def init(self):
        self.master = self.window.configPanel
        self.subjects = CONFIGURATION.subject_list
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.header = "Subject Editor"

        # Listbox to display subjects
        self.subject_listbox = tk.Listbox(self, height=10, width=30)
        self.subject_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=10)

        # Add subject entry
        self.add_label = ttk.Label(self, text="Add Subject:")
        self.add_label.grid(row=1, column=1, pady=5)

        self.subject_entry = ttk.Entry(self)
        self.subject_entry.grid(row=2, column=1, pady=5)

        # Add Button
        self.add_button = ttk.Button(self, text="Add", command=self.add_subject)
        self.add_button.grid(row=3, column=1, pady=5)

        # Delete Button
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_subject)
        self.delete_button.grid(row=4, column=1, pady=5)

        if self.subjects:
            self.update_subject_list()
        self.subject_entry.bind("<Return>", self.add_subject)

    def add_subject(self, event=None):
        subject = self.subject_entry.get().strip()
        if subject and subject not in self.subjects:
            self.subjects.append(subject)
            self.update_subject_list()
            self.subject_entry.delete(0, tk.END)  # Clear entry field

    def delete_subject(self):
        try:
            selected_index = self.subject_listbox.curselection()[0]
            selected_subject = self.subject_listbox.get(selected_index)
            self.subjects.remove(selected_subject)
            self.update_subject_list()
        except IndexError:
            pass  # No subject selected, do nothing

    def update_subject_list(self):
        # Update the listbox with the current subjects
        self.subject_listbox.delete(0, tk.END)
        for subject in self.subjects:
            self.subject_listbox.insert(tk.END, subject)
    
    def save(self):
        return {"subjects": self.subjects}

class TimetableSettingsPanel(_settingsPanel):
    def init(self):
        self.header = "Timetable Editor"
        self.subjects = CONFIGURATION.subject_list
        self.timetable = CONFIGURATION.timetable

        self.widgets = dict()
        self.createDay("Monday", 1)
        self.createDay("Tuesday", 6)
        self.createDay("Wednesday", 11)
        self.createDay("Thursday", 16)
        self.createDay("Friday", 21)
    
    def createDay(self, name: str, startingRow: int) -> None:
        inner = dict()
        inner["vars"] = {"Period 1": tk.StringVar(self, self.timetable.get(name, "No Subject Selected")[0]),
        "Period 2": tk.StringVar(self, self.timetable.get(name, "No Subject Selected")[1]),
        "Period 3": tk.StringVar(self, self.timetable.get(name, "No Subject Selected")[2]),
        "Period 4": tk.StringVar(self, self.timetable.get(name, "No Subject Selected")[3])}
        inner["label"] = ttk.Label(self, text=name, font=("Arial Bold", 12))
        inner["label"].grid(row=startingRow, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        inner["p1L"] = ttk.Label(self, text="Period 1:")
        inner["p1L"].grid(row=startingRow+1, column=0, sticky="w", padx=5, pady=2)
        inner["p1E"] = ttk.Combobox(self, values=self.subjects, textvariable=inner["vars"]["Period 1"])
        inner["p1E"].grid(row=startingRow+1, column=1, sticky="w", padx=5, pady=2)
        inner["p2L"] = ttk.Label(self, text="Period 2:")
        inner["p2L"].grid(row=startingRow+2, column=0, sticky="w", padx=5, pady=2)
        inner["p2E"] = ttk.Combobox(self, values=self.subjects, textvariable=inner["vars"]["Period 2"])
        inner["p2E"].grid(row=startingRow+2, column=1, sticky="w", padx=5, pady=2)
        inner["p3L"] = ttk.Label(self, text="Period 3:")
        inner["p3L"].grid(row=startingRow+3, column=0, sticky="w", padx=5, pady=2)
        inner["p3E"] = ttk.Combobox(self, values=self.subjects, textvariable=inner["vars"]["Period 3"])
        inner["p3E"].grid(row=startingRow+3, column=1, sticky="w", padx=5, pady=2)
        inner["p4L"] = ttk.Label(self, text="Period 4:")
        inner["p4L"].grid(row=startingRow+4, column=0, sticky="w", padx=5, pady=2)
        inner["p4E"] = ttk.Combobox(self, values=self.subjects, textvariable=inner["vars"]["Period 4"])
        inner["p4E"].grid(row=startingRow+4, column=1, sticky="w", padx=5, pady=2)
        self.widgets[name] = inner

    def save(self) -> None:
        result = dict()
        for key, value in self.widgets.items():
            result[key] = [value["vars"]["Period 1"].get(), value["vars"]["Period 2"].get(), value["vars"]["Period 3"].get(), value["vars"]["Period 4"].get()]
        result["Saturday"] = ["No Subject", "No Subject", "No Subject", "No Subject", "No Subject"]
        result["Sunday"] = ["No Subject", "No Subject", "No Subject", "No Subject", "No Subject"]
        return {"timetable": result}

class SettingsDialogue(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.title("PUtilties Configuration")
        self.geometry("580x300")
        self.resizable(False, False)
        self.createWidgets()
        self.grab_set()
        self.wait_window(self)
    
    def createWidgets(self) -> None:
        self.style = ttk.Style()
        self.style.configure("CustomSeparator.TSeparator", thickness=5)
        self.menuOptions: dict[str: ttk.Frame] = dict()
        self.selectorButtons = []

        self.selectorPanel = ttk.Frame(self, width=5)
        self.selectorPanel.grid(row=0, column=0, sticky="nw", padx=5)
        self.seperator = ttk.Separator(self, orient="vertical")
        self.seperator.grid(row=0, column=1, sticky="nw", padx=5)
        self.seperator.config(style="CustomSeparator.TSeparator")
        self.configPanel = ScrollableFrame(self)
        self.configPanel.grid(row=0, column=2, sticky="nsew", padx=5)

        self.addMenu("General Settings", GeneralSettingsPanel(self))
        self.showConfigPanel("General Settings")
        self.addMenu("Misc Settings", MiscellaneousSettingsPanel(self))
        self.addMenu("Subject Editor", SubjectEditorPanel(self))
        self.addMenu("Timetable Editor", TimetableSettingsPanel(self, True))

        self.buttonsFrame = ttk.Frame(self)
        self.buttonsFrame.grid(row=1, column=0, columnspan=3, sticky="sew")
        self.okButton = ttk.Button(self.buttonsFrame, text="Finish", command=self.ok)
        self.okButton.pack(side="right", anchor="e")
        self.cancelButton = ttk.Button(self.buttonsFrame, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side="right", anchor="e")
        self.applyButton = ttk.Button(self.buttonsFrame, text="Apply", command=self.apply)
        self.applyButton.pack(side="right", anchor="e")
        self.reset_to_defaults_button = ttk.Button(self.buttonsFrame, text="Reset to Default Configuration", command=self.reset_to_defaults)
        self.reset_to_defaults_button.pack(side="right", anchor="e")
    
    def cancel(self) -> None:
        confirmation = messagebox.askyesno("Confirm Cancellation", "Settings editor will be abandoned and all unsaved changes lost. Confirm?")
        if confirmation: self.destroy()
        else: self.grab_set()

    def reset_to_defaults(self) -> None:
        CONFIGURATION.reset_to_defaults(True)
        self.destroy()

    def ok(self) -> None:
        self.apply()
        self.destroy()

    def apply(self) -> None:
        data = dict()
        for name in self.menuOptions.keys():
            data = data | self.menuOptions[name].save()
        data["recent_files"] = CONFIGURATION.recent_files
        CONFIGURATION.write(data, True)

    def addMenu(self, name: str, menu: tk.Frame) -> None:
        """Add a menu to the settings selectorPanel."""
        self.menuOptions[name] = menu
        self.selectorButtons.append(ttk.Button(self.selectorPanel, text=name, padding=(5, 10), command=lambda: self.showConfigPanel(name)))
        self.selectorButtons[-1].pack(fill="x", anchor="nw")
    
    def showConfigPanel(self, name: str) -> None:
        self.configPanel.frame = self.menuOptions[name]

if __name__ == "__main__":
    window = SettingsDialogue()
    window.mainloop()
