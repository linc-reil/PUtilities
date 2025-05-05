"""
ErrorLogViewer (tab)
View the PUtilities error log from within PUtilities.
"""

from classes.Utilities import *

class ErrorLogViewer(TabFrame):
    _name = "PUtilities Error Log"
    _description = "View the PUtilities error log within PUtilities."
    _icon = "error log icon.png"

    def init(self) -> None:
        self.tabname = "Error Log"
        self.description = """View the PUtilities error log from within PUtilities."""
        self.auto_refresh = tk.BooleanVar(self, value=True)
        self.create_widgets()
        self.process()
    
    def process(self) -> None:
        if self.auto_refresh.get(): self.rewrite()
        self.after(1000, self.process)
    
    def create_widgets(self) -> None:
        self.text_box = ScrollableTextBox(self)
        self.text_box.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=1)
        self.text_box.text_widget.config(state=tk.DISABLED)
    
    def rewrite(self) -> None:
        with open(self.root_filepath + "/config/errorlog.md", "r") as file:
            text = file.read()
        self.text_box.text_widget.config(state=tk.NORMAL)
        self.text_box.clear()
        self.text_box.insertAtEnd(text)
        self.text_box.text_widget.config(state=tk.DISABLED)
    
    def createTabCommands(self) -> None:
        self.addTabCheckbox("Auto-Refresh", self.auto_refresh)
        
    