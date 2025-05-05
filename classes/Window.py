"""
PUtilties Window Controlling the tabs as well as overall functionality.
Imports fully from Utilities.py (under classes).
Imports _imports.pys (under classes). To get YOUR tab into the window, add it to the _imports.py file, and access it in this file using tabs.YourTabName.
"""


from classes.Utilities import *
from classes._TabManager import *
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk, WindowInterface):
    """
    Represents the main window of the PUtilities program.
    
    This class manages all other classes in the form of tabs. It also includes menus for file operations,
    mathematics, tab options, and more. It provides methods for adding tabs, switching tabs, and adding
    options to the various menus.
    
    Attributes:
        __version__ (str): The current version of PUtilities.
        filepath (str): The root filepath of the application, where the main.pyw file is stored, under the PUtilities/ directory.
        menubar (tk.Menu): The menu bar found at the top of the application window. Holds the file menu, mathematics menu, more menu, tab options menu, and close tab command.
        fileMenu (tk.Menu): The file menu of the application.
        newMenu (tk.Menu): The 'create new' menu of the application. Use the method add_command along with the label and a lambda expression to open a new tab using the Window.newTab method and add that command to the menu.
        openMenu (tk.Menu): The 'open' menu of the application. Use the same methods to add a command to this menu as the newMenu, but instead of using Window.newTab, use Window.newTabAndOpen to trigger the open command once the tab is opened.
        saveMenu (tk.Menu): The 'save' menu of the application. Includes commands for save, save as, and export, with export having inbuilt methods to be changed from the TabFrame class, which all tabs inherit from.
        exportMenu (tk.Menu): The 'export' menu of the application, under the save menu. Add commands to export for the different tabs, and is automatically cleared and re-loaded when switching between tabs.
        mathMenu (tk.Menu): The mathematics tool selector menu of the application. Use the same methods as the newMenu to add a given class and a command to open that tab class to this menu.
        moreMenu (tk.Menu): The miscellaneous menu containing options to configurate as well as test PUtilities. Placed on the main menubar.
        testingMenu (tk.Menu): A menu under moreMenu in which all testing can take place. If creating a new tab, use the testing menu to test it before adding it fully into the application.
        tabOptionsMenu (tk.Menu): The menu which holds all tab options for the given tab. Automatically updates when switching between tabs. The TabFrame class from Utilities.py has methods for automatically creating the tabframe.
        notebook (ttk.Notebook): The tab notebook which holds all tabs. DO NOT TOUCH. Takes up the entire window, and is the only widget that is a child of the tk.Tk window.
    """
    def __init__(self, __filepath__: str) -> None:
        """
        Initialisation of the PUtilities window, executed when first creating the class.

        Args:
            __filepath__ (str): The root filepath of the program - directory where the main.pyw file is stored. Use os.path.abspath(os.path.dirname(__file__)) when working in the root directory for this path.
        
        Returns: None
        """
        super().__init__()
        self.__version__ = PConstants.PUTILITIES_VERSION
        self.title(f"PUtilties Version {self.__version__}")
        self.geometry("850x600")
        self.filepath = __filepath__

    def _createMenu(self) -> None:
        """
        Internal function for creating the menubar and adding menus to that menubar. When adding a tab to the testing menu, use 'self.testingMenu.add_command(label="Name of Tab", command=lambda: self.newTab(tabs.YourTabName(self))). Called after the other internal function _CreateWidgets() in the Start() method.

        Returns: None
        """
        self.menubar = tk.Menu(self, tearoff=0)
        self.config(menu=self.menubar)

        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.fileMenu, label="File")
        self.newMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label="New", menu=self.newMenu)
        self.newMenu.add_command(label="New Text Document", command=lambda: self.newTab(tabs.TextEditor(self)))
        self.newMenu.add_command(label="New Lesson", command=lambda: self.newTab(tabs.LessonEditor(self)))
        self.openMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label="Open", menu=self.openMenu)
        self.openMenu.add_command(label="Open Home Tab", command=lambda: self.newTab(tabs.HomeScreen(self)))
        self.openMenu.add_command(label="Open File Explorer", command=lambda: self.newTab(tabs.FileExplorer(self)))
        self.openMenu.add_command(label="Open Text Documents", command=lambda: self.newTabAndOpen(tabs.TextEditor(self)))
        self.openMenu.add_command(label="Open Image(s)", command=lambda: self.newTab(tabs.ImageViewer(self)))
        self.openMenu.add_command(label="Open Error Log", command=lambda: self.newTab(tabs.ErrorLogViewer(self)))
        self.saveMenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label="Save", menu=self.saveMenu)
        self.saveMenu.add_command(label="Save", command=self.save)
        self.saveMenu.add_command(label="Save As", command=self.saveAs)
        self.exportMenu = tk.Menu(self.saveMenu, tearoff=0)
        self.fileMenu.add_cascade(label="Export", menu=self.exportMenu)
        self.fileMenu.add_separator()

        self.utilities_menu = tk.Menu(self, tearoff=0)
        self.menubar.add_cascade(label="Utilities", menu=self.utilities_menu)
        self.utilities_menu.add_command(label="Command Line", command=lambda: self.newTab(tabs.CommandLine(self)))
        self.utilities_menu.add_command(label="Linux Terminal", command=lambda: self.newTab(tabs.LinuxTerminal(self)))
        self.utilities_menu.add_command(label="Password Generator", command=lambda: self.newTab(tabs.PasswordGenerator(self)))
        self.utilities_menu.add_command(label="Simple Calculator", command=lambda: self.newTab(tabs.Calculator(self)))
        self.utilities_menu.add_command(label="Unit Converter", command=lambda: self.newTab(tabs.UnitConverter(self)))
        self.utilities_menu.add_command(label="Right Triangle Calculator", command=lambda: self.newTab(tabs.RightTriangleCalculator(self)))
        self.utilities_menu.add_command(label="Projectile Motion Calculator", command=lambda: self.newTab(tabs.ProjectileMotionCalculator(self)))
        self.utilities_menu.add_command(label="CPS Tester", command=lambda: self.newTab(tabs.CpsTester(self)))
        self.utilities_menu.add_command(label="All Tabs...", command=lambda: self.newTab(TabSelector(self)))

        self.moreMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_cascade(label="More", menu=self.moreMenu)
        self.moreMenu.add_command(label="Configurate PUtilties", command=self.openSettingsDialogue)
        self.testingMenu = tk.Menu(self.moreMenu, tearoff=0)
        self.moreMenu.add_cascade(label="Testing", menu=self.testingMenu)

        # Add TESTING Tabs here. Use a lambda expression as shown below as the command.:
        self.testingMenu.add_command(label="Open Example Tab", command=lambda: self.newTab(tabs.ExampleTab(self)))

        #self.menubar.add_separator()
        self.tabOptionsMenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tab Options", menu=self.tabOptionsMenu)
        self.fileMenu.add_command(label="Exit Program", command=self.destroy)
        self.menubar.add_command(label="Close Current Tab", command=self.closeCurrentTab)
        try:
            self.newTab(tabs.HomeScreen(self))
        except Exception as e:
            messagebox.showerror("Error", "Error in creation of Homepage tab. Check error log.")
            ERROR_LOG.log(f"[window] Error in creating Home tab. Error type: {str(e)}")
            self.notebook.forget(self.notebook.select())
    
    def _createWidgets(self) -> None:
        """
        Internal function for creating the tab widget (ttk.Notebook). Not recommended to modify. Also includes bindings for save, save as, open, etc. Called in the Start() method of the window before the _CreateMenu() method.
        """
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self._onTabChange)

        self.bind("<Control-s>", self.save)
        self.bind("<Control-Shift-s>", self.saveAs)
        self.bind("<Control-o>", self.open)
        self.bind("<Control-w>", self.closeCurrentTab)
        self.bind("<Control-n>", self.new)
        self.bind("<Shift-Left>", self.switchToPreviousTab)
        self.bind("<Shift-Right>", self.switchToNextTab)
        self.bind("<Control-t>", lambda event: self.newTab(tabs.HomeScreen(self)))
        self.bind("<Control-q>", lambda event: self.newTab(tabs.CommandLine(self)))

    def start(self) -> None:
        """
        Start the program. Calls the internal functions _CreateWidgets() and _CreateMenu(), and starts the mainloop of the window.

        Returns: None
        """
        self._createWidgets()
        self._createMenu()
        self.mainloop()
    
    def getCurrentTab(self) -> TabFrame:
        """
        Gets the current tab in the form of its object (tabframe). This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        return self.notebook.nametowidget(self.notebook.select())
    
    def getFinalTab(self) -> TabFrame:
        """
        Gets the final tab in the form of its object (tabframe). This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        return self.notebook.nametowidget(self.notebook.tabs()[:-1])
    
    def getTabAtIndex(self, index: int = -1) -> typing.Any:
        """
        Gets the tab at a certain index in the form of its object (tabframe). This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        index %= len(self.notebook.tabs())
        return self.notebook.nametowidget(self.notebook.tabs()[index])
    
    def switchToFinalTab(self) -> None:
        """
        Switches to the final tab. Can be called from outside the Window class.

        Returns: None
        """
        self.notebook.select(self.notebook.tabs()[-1])
    
    def switchToTabAtIndex(self, index: int = -1) -> None:
        """
        Switches to a tab at a certain index. Can be called from outside the Window class.

        Args:
            index (int): The index of the tab in the current tabs you are wishing to switch to. If that index does not exist, will use the modulus operator to always get a valid index.
        
        Returns: None
        """
        index %= len(self.notebook.tabs())
        self.notebook.select(self.notebook.tabs()[index])
    
    def switchToNextTab(self, event=None) -> None:
        """
        Switch to the next tab. If at final tab, then switches back to the first tab. Also called using the keyboard shortcut Shift+Right. Do not touch the event arg.

        Returns: None
        """
        index = self.notebook.index("current")
        self.switchToTabAtIndex(index + 1)
    
    def switchToPreviousTab(self, event=None) -> None:
        """
        Switch to the previous tab. If at starting tab, then loops back around to the last tab. Also called using the keyboard shortcut Shift+Left. Do not touch the event arg.

        Returns: None
        """
        self.switchToTabAtIndex(self.notebook.index("current") - 1)
    
    def getTabList(self) -> list:
        """
        Returns the tab list using self.notebook.tabs(). Only meant to be used in the other methods surrounding tabs.

        Returns: list -> A list of the tab identifiers in the Window.notebook.
        """
        return self.notebook.tabs()
    
    def _closeCurrentTab(self) -> None:
        """
        Internal function. Close the current tab open in the tab notebook. Also calls the onTabClose() method of the TabFrame.

        Returns: None
        """
        self.getCurrentTab().onTabClose()
        self.notebook.forget(self.notebook.select())

    def closeCurrentTab(self, event=None) -> None:
        """
        Closes the current tab. If the current tab is the only tab, closes the tab and opens the home tab. Also calls the onTabClose() method of the TabFrame, and is called using the keyboard shortcut Control+w

        Returns: None
        """
        if len(self.getTabList()) > 1:
            self._closeCurrentTab()
        else:
            self._closeCurrentTab()
            self.newTab(tabs.HomeScreen(self))
    
    def newTab(self, tabframe: TabFrame, name: str = "New Tab") -> None:
        """
        Creates a new tab using the tabs class and the name of the tab. Then switches to that final tab.
        Generally, the following lambda expression is used when adding to a given menu:
            command=lambda: self.newTab(tabs.YourTabName(self))
        
        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into. Pass your class initialised with the master of the window (self). Calls the _onTabCreation() method of the tab you are adding.
            name (str): The name of the tab. Generally, this does not need to be set when defining the TabFrame.tabname property in the TabFrame.init() method.
        
        Returns: None
        """
        self.notebook.add(tabframe, text=name)
        self.switchToFinalTab()
        self.getCurrentTab()._onTabCreation()
    
    def newTabAndOpen(self, tabframe: TabFrame, name: str = "New Tab") -> None:
        """
        Creates a new tab with newTab and calls the open dialogue for that tab. Usually used when adding a command to the open menu under the file menu.

        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into. Pass your class initialised with the master of the window (self). Calls the _onTabCreation() method of the tab you are adding.
            name (str): The name of the tab. Generally, this does not need to be set when defining the TabFrame.tabname property in the TabFrame.init() method.
        
        Returns: None
        """
        self.newTab(tabframe=tabframe, name=name)
        self.getCurrentTab().open()
    
    def newTabAndAutoload(self, tabframe: TabFrame, filepath: str, name: str = "New Tab") -> None:
        """
        Creates a new tab with newTab and calls the autoload method for that tab. Usually used only from the file explorer.

        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into. Pass your class initialised with the master of the window (self). Calls the _onTabCreation() method of the tab you are adding.
            filepath (str): The filepath of the file to autoload. Be noted that the file must be dealt with in the tab for any errors.
            name (str): The name of the tab. Generally, this does not need to be set when defining the TabFrame.tabname property in the TabFrame.init() method.
        
        Returns: None
        """
        self.newTab(tabframe=tabframe, name=name)
        self.getCurrentTab().autoload(filepath)
    
    def changeCurrentTabName(self, newName: str) -> None:
        """
        Change the current tab's name. Intended to be called from both in and outside the Window class. Also called when modifying the tabname attribute of the TabFrame class, so that the tab is renamed instantly.

        Args:
            newName (str): The new name that you want the tab to be called.
        
        Returns: None
        """
        if len(newName) > 27:
            newName = newName[:27] + "..."
        if not self.notebook.select():
            print("no tab selected")
            return
        self.notebook.tab(self.notebook.select(), text=newName)
    
    def _onTabChange(self, event=None) -> None:
        """
        Internal function called when the tab is changed. Calls the methods clearTabOptions(), clearExportMenu(), and currentTab._onTabOpen().

        Returns: None
        """
        self.clearTabOptions()
        self.clearExportMenu()
        self.getCurrentTab()._onTabOpen()
    
    def clearTabOptions(self) -> None:
        """
        Clears the tab options menu. Called automatically when the tab is changed, before the new tab options are added.

        Returns: None
        """
        self.tabOptionsMenu.delete(0, "end")
    
    def save(self, event=None) -> None:
        """
        Calls the current tab's save() method. Also called with the keyboard shortcut Control+s.

        Returns: None
        """
        self.getCurrentTab().save()
    
    def saveAs(self, event=None) -> None:
        """
        Calls the current tab's saveAs() method. Also called with the keyboard shortcut Control+Shift+s.

        Returns: None
        """
        self.getCurrentTab().saveAs()
    
    def open(self, event=None) -> None:
        """
        Calls the current tab's open() method. Also called with the keyboard shortcut Control+o.

        Returns: None
        """
        self.getCurrentTab().open()
    
    def new(self, event=None) -> None:
        """
        Calls the current tab's new() method. Also called with the keyboard shortcut Control+n.

        Returns: None
        """
        self.getCurrentTab().new()
    
    def clearExportMenu(self) -> None:
        """
        Clears the export menu when the tab is changed, preparing it for adding new items to the export menu.

        Returns: None
        """
        self.exportMenu.delete(0, "end")
    
    def openSettingsDialogue(self) -> None:
        """
        Open the settings dialogue. Will create a new window for the dialogue, and runs in parallel.

        Returns: None
        """
        dialogue = tabs.SettingsDialogue()
        dialogue.mainloop()
    
    def open_file_in_specific_tab(self, filepath: str) -> None:
        """
        Open a given filepath in its available tab.

        Returns: None
        """
        if not PFileHandler.filepath_exists(filepath): return
        if filepath.endswith(".json"):
            self.newTabAndAutoload(tabs.LessonEditor(self), filepath)
        elif filepath.endswith(".png") or filepath.endswith(".gif"):
            self.newTabAndAutoload(tabs.ImageViewer(self), filepath)
        else:
            self.newTabAndAutoload(tabs.TextEditor(self), filepath)
        CONFIGURATION.add_recent_file(filepath)

if __name__ == "__main__":
    program = Window("J:/!2025 Year 10A/!Warning - This Folder is Messy!/Python/PUtilities School Edition")
    program.start()
