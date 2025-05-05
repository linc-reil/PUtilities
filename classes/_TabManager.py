"""
PUtilities Tab Manager
Includes a list of tabs and all tab imports.
"""

import classes._imports as tabs
from classes.Utilities import *

class TabSelector(TabFrame):
    """Main PUtilities Tab Selector tab."""
    _name = "Tab Selector"
    _description = "Select and open a PUtilities tab."

    def init(self) -> None:
        self.tabname = "Tab Selector"
        self.description = "Open a tab from the full list of PUtilities tabs."
        self.create_widgets()
    
    def create_widgets(self) -> None:
        self.header = ttk.Label(self, text="PUtilities Tab Selector", font=PConstants.arial_24)
        self.header.pack()
        self.subtitle = ttk.Label(self, text="Select a tab from the full list.")
        self.subtitle.pack()

        self.tabs_frame = ttk.Frame(self)
        self.tabs_frame.pack(fill=tk.BOTH, expand=1)
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill=tk.X)

        self.tab_selectors: list[ttk.Button] = []
        self.tab_selector_icons: list[tk.PhotoImage] = []
        self.create_buttons()

    def create_buttons(self) -> None:
        num_columns = 5
        count = 0
        for item in tabs.TABS_LIST:
            self.tab_selector_icons.append(PFileHandler.get_tab_icon(item._icon))
            self.tab_selectors.append(ttk.Button(
                self.tabs_frame,
                text=item.get_name(),
                compound="top",
                image=self.tab_selector_icons[-1],
                command=lambda item=item: self.window.newTab(item(self.window))
            ))
            self.tab_selectors[-1].grid(row=count // num_columns, column=count % num_columns, sticky=tk.NW, padx=5, pady=5)
            count += 1
