"""
PUtilties TabFrame and other Utilities used in the developement process. It is recommended to use the import line 'from classes.Utilities import *' to import all functions and classes from this module.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import typing, os, sys, math, time, random, datetime, pathlib, json, pickle, configparser, abc

LOWERCASE = list("abcdefghijklmnopqrstuvwxyz")
UPPERCASE = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS = list("0123456789")

class TabFrame(ttk.Frame, abc.ABC):
    """
    Frame able to be added as a tab to the PUtilties Window. ALL UTILITIES SHOULD INHERIT FROM THIS CLASS.

    Attributes:
        window (Window): A reference to the main window that this tab is added to. Used to call important methods from the Window to do with tab naming, commands, etc.
        description (str): A description of the tab (property).
        _defaultTabName (str): The default name of the tab. In general, should not be touched, as it usually never used.
        _tabname (str): The internal attribute for the name of the tab. When developing a tab, only use the tabname property of the TabFrame class, as it provides additional functionality, automatically renaming the tab when it is set.
    
    When creating a class inheriting from the TabFrame, the following boilerplate code should be used:
        from classes.Utilities import *

        class YourTabName(TabFrame):
            def init(self):
                self.tabname = "Your Tab Name" # Set the tab name
                Create your widgets here.
            
            def createTabCommands(self):
                Create your tab commands here using the addTabCommand(), addTabCheckbox(), addExportCommand() methods.
    """
    # Static class members - see methods with the @classmethod descriptor
    _icon: str = "default tab icon.png"
    _name: str = "Unnamed Tab"
    _description: str = "No description available."

    def __init__(self, window: tk.Tk) -> None:
        """
        Initialisation of the TabFrame class. Used only in the Window() class when adding a new tab.

        Args:
            window (Window): The main window of the program. The TabFrame then stores a reference to this window so that main window commands can be called from the TabFrame.
        
        Returns: None
        """
        super().__init__(master=window.notebook)
        self.window: WindowInterface = window
        self._tabname = self._name
    
    def _onTabCreation(self) -> None:
        """
        Internal method, called on the tabs creation. Then in turn calls the methods init() and createTabCommands().

        Returns: None
        """
        self.init()
        self.createTabCommands()

    def _onTabOpen(self) -> None:
        """
        Internal method called when the THIS tab is switched to. Only exists to call createTabCommands() method of this TabFrame.

        Returns: None
        """
        self.createTabCommands()
    
    @abc.abstractmethod
    def init(self) -> None:
        """Use this method as the one used for initialisation of the tab. Runs only when the tab is first created. Designed to be the place widgets are defined, as well as any important attributes to the class.
        Override simply by defining the method in your custom tab.
        
        Returns: None"""
        #self.createTabCommands()
        ...
    
    def onTabClose(self) -> None:
        """
        Executes when the tab is closed. Is left blank by default, but can be overwritten if specific functionality is needed.

        Returns: None
        """
        ...
    
    def createTabCommands(self) -> None:
        """
        Create the tabs commands. Executes under initialisation as well as when switching back to the tab.
        Override this method if your tab needs tab commands.

        Returns: None
        """
        ...
    
    def open(self) -> None:
        """
        Blank method for opening a file. Override by re-defining this method in your tab class. Called broadly in the Window class.

        Returns: None
        """
        ...
    
    def save(self) -> None:
        """
        Blank method for saving a file. Override by re-defining this method in your tab class. Called broadly in the Window class.

        Returns: None
        """
        ...
    
    def saveAs(self) -> None:
        """
        Blank method for saving a file with a new filename. Override by re-defining this method in your tab class. Called broadly in the Window class.

        Returns: None
        """
        ...
    
    def new(self) -> None:
        """
        Blank method for opening a new file. Override by re-defining this method in your tab class. Called broadly in the Window class.

        Returns: None
        """
        ...
    
    def clearTabFunctions(self) -> None:
        """
        Clears the current tab functions. Simply calls the Window.clearTabFunctions() method.

        Returns: None
        """
        self.window.clearTabFunctions()
    
    def addTabFunction(self, name: str = "", function: typing.Callable = None) -> None:
        """
        Add a tab function to the tab functions menu. Designed to be called in your tab classes createTabFunctions() method.

        Args:
            name (str): The name of the tab function you are adding.
            function (Callable): The function (usually a method of your class) which, when clicked on, this tab function calls.

        Returns: None
        """
        self.window.tabOptionsMenu.add_command(label=name, command=function)
    
    def addTabCheckbox(self, name: str = "", variable: tk.BooleanVar = None) -> None:
        """
        Add a tab checkbox to the tab functions menu. Designed to be called in your tabs createTabFunctions() method.

        Args:
            name (str): The name of the tab checkbox you are adding.
            variable (tk.BooleanVar): The tkinter boolean variable which the checkbox updates. Call the .get() method on this variable to get the true/false result.
        
        Returns: None
        """
        self.window.tabOptionsMenu.add_checkbutton(label=name, variable=variable)
    
    def close(self) -> None:
        """
        Close the current tab. Called using the keyboard shortcut Control+w.

        Returns: None
        """
        self.window.closeCurrentTab()
    
    def renameTab(self, newName: str) -> None:
        """
        Rename the current tab. Generally, use the property tabname instead to quickly rename the tab in one line.

        Args:
            newName (str): The new name of the tab.
        
        Returns: None
        """
        self._tabname = newName
        self.window.changeCurrentTabName(newName)
    
    @property
    def tabname(self) -> str:
        """Get the current tabname.
        
        Returns: str"""
        return self._tabname

    @tabname.setter
    def tabname(self, newName: str) -> None:
        """
        Set the current tab's name, automatically renaming the tab in the Window.notebook.

        Args:
            newName (str): The new name of the tab.
        
        Returns: None
        """
        if not isinstance(newName, str):
            return
        self.renameTab(newName)
    
    def getPhotoimage(self, imageNameOrPathFromAssets: str) -> tk.PhotoImage:
        """
        Get a photo image from its name in the assets folder. Intended to be used to add images to labels.

        Args:
            imageNameOrPathFromAssets (str): The image name or image path from the assets folder. e.g. "default-image.jpg".
        
        Returns: tk.PhotoImage
        """
        path = self.window.filepath + f"/assets/{imageNameOrPathFromAssets}"
        return tk.PhotoImage(file=path)
    
    def quitProgram(self) -> None:
        """
        Quit the entire PUtilities program. Calls Window.destroy() and sys.exit().
        """
        self.window.destroy()
        sys.exit()
    
    def addExportCommand(self, label: str, command: typing.Callable) -> None:
        """
        Add a command to the export menu. Designed to be called from your tab's createTabCommands() method.

        Args:
            label (str): The name of the export command.
            command (Callable): The function (usually a method of your tab) that is called when selected in the menu.
        
        Returns: None
        """
        self.window.exportMenu.add_command(label=label, command=command)
    
    def clearExportCommands(self) -> None:
        """
        Clear all export commands. Is automatically called when switching tabs.

        Returns: None
        """
        self.window.clearExportMenu()
    
    def autoload(self, filepath: str) -> None:
        """Blank method for loading a filepath without using any dialogue.
        
        Arguments:
            filepath (str): The full filepath to the file attempting to be opened.
        
        Returns: None"""
        ...
    
    @classmethod
    def get_description(cls) -> str:
        """The description of the PUtilities tab."""
        return cls._description

    def set_description(cls, new: str | list[str]) -> None:
        """Set the tab's description."""
        if isinstance(new, str): cls._description = new; return
        elif isinstance(new, list): cls._description = "\n".join(new); return
    
    @property
    def root_filepath(self) -> str:
        """Get the root filepath."""
        return PConstants.ROOT_FILEPATH
    
    @classmethod
    def get_icon_path(cls) -> str:
        """Get the icon path of the class ready to be turned into a PhotoImage."""
        return PFileHandler.TAB_ICONS_FILEPATH + "/" + cls._icon
    
    @classmethod
    def set_icon(cls, icon_filename: str = "default tab icon.png") -> None:
        """Set the icon of your tab based on it's FILENAME in the assets/tab icons directory."""
        new = PFileHandler.TAB_ICONS_FILEPATH + "/" + icon_filename
        if not PFileHandler.filepath_exists(new): icon_filename = "default tab icon.png"
        cls._icon = icon_filename
    
    @classmethod
    def get_name(cls) -> str:
        """Get the name of the tab."""
        return cls._name

    @classmethod
    def set_name(cls, new_name: str) -> None:
        """Set the name of the tab the user sees."""
        cls._name = new_name
        
def get_filename_of_filepath(filepath: str) -> str:
    """Returns the filename of a filepath."""
    return pathlib.Path(filepath).name

def get_raw_filepath(filepath: str) -> str:
    """Returns the pure filepath of a filepath."""
    return os.path.dirname(os.path.abspath(filepath))

class ScrollableTextBox(tk.Frame):
    def __init__(self, master=None, **kwargs):
        """
        A scrollable text box widget.

        Parameters:
        master: Parent widget
        kwargs: Additional configuration options for the Text widget
        """
        super().__init__(master)

        # Create the Text widget
        self.text_widget = tk.Text(self, wrap="word", **kwargs)
        self.text_widget.pack(side="left", fill="both", expand=True)

        # Create the vertical Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Link the Text widget and the Scrollbar
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    def insert(self, *args):
        """Insert text into the Text widget."""
        self.text_widget.insert(*args)

    def delete(self, *args):
        """Delete text from the Text widget."""
        self.text_widget.delete(*args)

    def get(self, *args):
        """Get text from the Text widget."""
        return self.text_widget.get(*args)

    def clear(self):
        """Clear all text from the Text widget."""
        self.text_widget.delete("1.0", "end")

    def getAll(self):
        """Retrieve all text from the Text widget."""
        return self.text_widget.get("1.0", "end-1c")

    def insertAtStart(self, text: str):
        self.text_widget.insert("1.0", text)
    
    def insertAtEnd(self, text: str) -> None:
        """Insert text at the end of the textbox."""
        self.text_widget.insert(tk.END, text)
    
    def scrollToBottom(self):
        """Scroll the text box to the bottom."""
        self.text_widget.yview(tk.END)

def toFloat(object: str | typing.Any) -> float:
    """Convert an object (mostly a string) to a floating-point number."""
    _floatCharacters = list("0123456789.")
    _floatOperators = list("+-*x/()^%")
    supportedChars = _floatCharacters + _floatOperators
    string = list(object.lower())
    try:
        i = 0
        while i < len(string):
            if not string[i] in supportedChars:
                string.pop(i)
                i -= 1
            if string[i] == "x":
                string[i] = "*"
            if string[i] == "^":
                string[i] = "**"
            i += 1
        string = "".join(string)
        result = eval(string)
        return result
    except:
        return 0.0

def toInt(object: str | typing.Any) -> int:
    """Convert an object (mostly a string) to an integer."""
    return round(toFloat(object))

class right_triangle:
    """An object for expressing a right triangle. Includes various functions for calculating right triangles. 
    As this is an object and not a set of functions, it requires input variables to function properly."""
    def __init__(self, hypotenuse: float | None = None, opposite: float | None = None, adjacent: float | None = None, theta: float | None = None, phi: float | None = None, radians: bool = False) -> None:
        try:
            self.hypotenuse = float(hypotenuse)
        except:
            self.hypotenuse = 0
        try:
            self.opposite = float(opposite)
        except:
            self.opposite = 0
        try:
            self.adjacent = float(adjacent)
        except:
            self.adjacent = 0
        self.radians = bool(radians)
        self.update_quarter_revolution()
        try:
            self.theta = float(theta) % self.quarter_revolution
        except:
            self.theta = 0
        try:
            self.phi = float(phi) % self.quarter_revolution
        except:
            self.phi = 0
        self.init_dictionary()
        self.height = None
        self.area = None
        self.perimeter = None

    def update_quarter_revolution(self) -> None:
        if self.radians:
            self.quarter_revolution = math.pi / 2
            self.full_revolution = 2 * math.pi
        else:
            self.quarter_revolution = 90
            self.full_revolution = 360
    
    def toggle_radians_degrees(self) -> None:
        if self.radians:
            self.radians = False
        else:
            self.radians = True

    def toggle_angle_units(self) -> None:
        self.toggle_radians_degrees()
        if self.radians:
            self.theta = math.radians(self.theta)
            self.phi = math.radians(self.phi)
        else:
            self.theta = math.degrees(self.theta)
            self.phi = math.degrees(self.phi)

    def init_dictionary(self) -> None:
        self.dictionary = {"Hypotenuse": self.hypotenuse,
        "Opposite": self.opposite,
        "Adjacent": self.adjacent,
        "Theta": self.theta,
        "Phi": self.phi,
        "Radians?": self.radians}

    def update_dictionary(self) -> None:
        self.init_dictionary()
        self.dictionary["Area"] = self.area
        self.dictionary["Perimeter"] = self.perimeter
        self.dictionary["Height"] = self.height
        self.dictionary["Semi Perimeter"] = self.perimeter / 2
        self.dictionary["Inradius"] = self.area / self.dictionary["Semi Perimeter"]
        self.dictionary["Circumradius"] = self.hypotenuse / 2

    def print_triangle_information(self) -> None:
        for item in self.dictionary.keys():
            print(str(item) + " = " + str(self.dictionary[item]))

    def solve_triangle(self) -> None:
        if not self.radians:
            self.toggle_angle_units()
            back_to_degrees = True
        else:
            back_to_degrees = False
        self.update_quarter_revolution()
        if self.opposite and self.adjacent:
            self.hypotenuse = (self.opposite**2 + self.adjacent**2)**0.5
            self.theta = math.asin(self.opposite / self.hypotenuse)
            self.phi = self.quarter_revolution - self.theta
        elif self.hypotenuse and self.opposite:
            self.adjacent = (self.hypotenuse**2 - self.opposite**2)**0.5
            self.theta = math.asin(self.opposite / self.hypotenuse)
            self.phi = self.quarter_revolution - self.theta
        elif self.hypotenuse and self.adjacent:
            self.opposite = (self.hypotenuse**2 - self.adjacent**2)**0.5
            self.theta = math.asin(self.opposite / self.hypotenuse)
            self.phi = self.quarter_revolution - self.theta
        elif self.hypotenuse and self.theta:
            self.opposite = math.sin(self.theta) * self.hypotenuse
            self.adjacent = (self.hypotenuse**2 - self.opposite**2)**0.5
            self.phi = self.quarter_revolution - self.theta
        elif self.hypotenuse and self.phi:
            self.adjacent = math.sin(self.phi) * self.hypotenuse
            self.opposite = (self.hypotenuse**2 - self.adjacent**2)**0.5
            self.theta = self.quarter_revolution - self.phi
        elif self.opposite and self.theta:
            self.hypotenuse = self.opposite / math.sin(self.theta)
            self.adjacent = (self.hypotenuse**2 - self.opposite**2)**0.5
            self.phi = self.quarter_revolution - self.theta
        elif self.opposite and self.phi:
            self.hypotenuse = self.opposite / math.cos(self.phi)
            self.adjacent = (self.hypotenuse**2 - self.opposite**2)**0.5
            self.theta = self.quarter_revolution - self.phi
        elif self.adjacent and self.theta:
            self.hypotenuse = self.adjacent / math.cos(self.theta)
            self.opposite = (self.hypotenuse**2 - self.adjacent**2)**0.5
            self.phi = self.quarter_revolution - self.theta
        elif self.adjacent and self.phi:
            self.hypotenuse = self.adjacent / math.sin(self.phi)
            self.opposite = (self.hypotenuse**2 - self.adjacent**2)**0.5
            self.theta = self.quarter_revolution - self.phi
        if back_to_degrees:
            self.toggle_angle_units()
        if self.adjacent and self.opposite:
            self.area = self.adjacent * self.opposite / 2
            if self.hypotenuse:
                self.height = self.opposite * self.adjacent / self.hypotenuse
                self.perimeter = self.opposite + self.adjacent + self.hypotenuse
        self.update_dictionary()

def get_quadratic_solutions(a: float, b: float, c: float) -> tuple[float, float]:
    """Get solutions to a quadratic equation."""
    midpoint = -b / (2*a)
    determinate = ((b**2 - 4*a*c)**0.5) / (2*a)
    return(midpoint+determinate, midpoint-determinate)

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, scrollableWithMouse: bool = True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrollableWithMouse = scrollableWithMouse
        # Create a canvas to contain the content
        self.canvas = tk.Canvas(self)
        
        # Create a scrollbar linked to the canvas
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create a frame inside the canvas to hold the content
        self._frame = tk.Frame(self.canvas)
        
        # Create a window on the canvas to place the scrollable_frame
        self.canvas.create_window((0, 0), window=self._frame, anchor="nw")
        
        # Bind the configure event to update the scrollregion
        self._frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
    
    @property
    def frame(self) -> tk.Frame:
        return self._frame

    @frame.setter
    def frame(self, new: tk.Frame) -> None:
        self.canvas.delete("all")
        self._frame = new
        self.canvas.create_window((0, 0), window=self._frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self._frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.yview_moveto(0)
        self.canvas.yview_scroll(-1, "units")
        self.canvas.yview_scroll(1, "units")
    
    def on_mouse_wheel(self, event):
        # On Windows and macOS, the event.delta is positive for scrolling up and negative for scrolling down
        # On Linux, we check for button 4 (up) or button 5 (down)

        if event.delta:  # Windows/macOS (use event.delta to determine the scroll direction)
            delta = event.delta
        elif event.num == 4:  # Linux (button 4 means scrolling up)
            delta = 120
        elif event.num == 5:  # Linux (button 5 means scrolling down)
            delta = -120
        else:
            delta = 0
        
        # Scroll the canvas based on the wheel movement (delta value)
        if self.scrollableWithMouse:
            self.canvas.yview_scroll(int(-delta / 120), "units")

def smartRound(number: float | int) -> int | float:
    """Round a number to a certain number of decimal places in the config file. If none, then will not round."""
    if not isinstance(number, (float, int)): return number

    numDecimalPlaces = CONFIGURATION.rounding
    if isinstance(number, int) or numDecimalPlaces is None:
        return number
    return round(number, numDecimalPlaces)

def _getRootFilepath() -> str:
    """Get the root filepath of the program."""
    return os.path.abspath(os.path.dirname(__file__))[:-8]

def _filename_advanced(filepath: str) -> str:
    # Get the filename with extension
    filename_with_extension = os.path.basename(filepath)
    # Split the filename from its extension and return the name without extension
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    return filename_without_extension

TYPE_STRING_OR_NONE = str | None
TYPE_INT_NONE = int | None

def _filepath_exists(filepath: str, *args, **kwargs) -> bool:
    """
    Check whether a filepath exists.

    Arguments:
        filepath (str): The filepath to check.
    
    Returns: bool
    """
    if not isinstance(filepath, str): return False
    return os.path.exists(filepath)

def get_date() -> str:
    """
    Get the current date in the format "dd/mm/yyyy".

    This method returns the current date as a string formatted as "dd/mm/yyyy" 
    using the current local date and time.

    Parameters:
        None

    Returns:
        str: The current date as a string in the format "dd/mm/yyyy".
    """
    return datetime.datetime.now().strftime("%d/%m/%Y")

def get_hour_minute() -> str:
    """
    Get the current time in the format "hh:mm".

    This method returns the current time as a string formatted as "hh:mm" 
    using the current local time.

    Parameters:
        None

    Returns:
        str: The current time as a string in the format "hh:mm".
    """
    return datetime.datetime.now().strftime("%H:%M")

class _FileFactory:
    """Factory for creating, loading and modifying files. Use FileFactory().method() to call a method."""
    def __init__(self, filepath: TYPE_STRING_OR_NONE = None, *args, **kwargs) -> None:
        """Initialise file factory.
        
        Arguments:
            filepath (TYPE_STRING_OR_NONE): The working directory of the file factory."""
        self._filepath = filepath
    
    @property
    def filepath(self) -> str:
        return self._filepath
    
    @filepath.setter
    def filepath(self, new: str) -> None:
        if not _filepath_exists(os.path.dirname(new)): raise ValueError(f"Could not find directory of {new}.")
        self. _filepath = new
    
    def write_to_file(self, data: str, *args, filepath: TYPE_STRING_OR_NONE = None, mode: typing.Literal["w", "a"] = "w", throw_error: bool = True) -> None:
        """
        Write data to a file. If FileFactory.filepath is set, then filepath does not need to be included.

        Arguments:
            data (str): The data to write to the file.
            filepath (str): The filepath to write the file to. Does not need to be included if a filepath was set upon the FileFactory's creation.
            mode (str): The mode of writing to the file ("w" for write and "a" for append).
            throw_error (bool): Whether or not to throw an error if the file is not found or writing in unsuccessful.
        
        Returns: None"""
        if not self._filepath and (not filepath):
            if throw_error: raise ValueError("No filepath specified in write_to_file() method of FileFactory.")
            else: return
        if not filepath: filepath = self._filepath
        with open(filepath, mode) as file:
            file.write(data)
    
    def load_file(self, *args, filepath: TYPE_STRING_OR_NONE = None, throw_error: bool = True) -> str:
        """
        Load a file.

        Arguments:
            filepath (TYPE_STRING_OR_NONE): The filepath to load a file from. If unspecified, will default to the filepath defined on initialisation.
            throw_error (bool): Whether or not to throw an error.
        
        Returns: str
        """
        if not self._filepath and (not filepath or not os.path.exists(filepath)):
            if throw_error: raise ValueError("Filepath not specified or does not exist in load_file() method of FileFactory class.")
            else: return ""
        if not self._filepath or not os.path.exists(self._filepath):
            if throw_error: raise ValueError("Filepath not detected or not found in load_file() method of FileFactory class.")
            else: return ""
        if not filepath: filepath = self._filepath
        with open(filepath, "r") as file:
            return file.read()
    
    def write_to_json_file(self, data: dict, *args, filepath: TYPE_STRING_OR_NONE = None, throw_error: bool = True, indent: TYPE_INT_NONE = 4, **kwargs) -> None:
        """
        Write data in the form of a dictionary to a file.

        Arguments:
            data (dict): The data to save.
            filepath (TYPE_STRINGOR_NONE): The filepath of the json file. If none, will default to the filepath created upon initialisation.
            throw_error (bool): Whether or not to throw an error if unsuccessful.
        
        Returns: None
        """
        if (not filepath) and not self._filepath:
            if throw_error: raise ValueError("Filepath not specified in the write_to_json_file() method of the FileFactory class.")
            else: return
        if not (filepath): filepath = self._filepath
        with open(filepath, "w") as file:
            json.dump(data, file, indent=indent)
    
    def load_json_file(self, *args, filepath: TYPE_STRING_OR_NONE = None, throw_error: bool = True) -> dict:
        """
        Load a json file with a given filepath or the default filepath.

        Arguments:
            filepath (TYPE_STRING_OR_NONE): The filepath to load. If None, defaults to filepath defined upon initialisation of the FileFactory class.
            throw_error (bool): Whether or not to throw an error if something goes wrong.
        
        Returns: dict
        """
        if not _filepath_exists(self._filepath) and not _filepath_exists(filepath):
            if throw_error: raise ValueError("No filepath defined in the load_json_file() method of the FileFactory class.")
            else: return dict()
        if not _filepath_exists(filepath): filepath = self._filepath
        with open(filepath, "r") as file:
            return json.load(file)
    
    def load_ini_file(self, *args, filepath: TYPE_STRING_OR_NONE = None, throw_error: bool = True) -> dict:
        """
        Load an ini file (standard configuration file).

        Arguments:
            filepath (TYPE_STRING_OR_NONE): The filepath to load the .ini file from.
            throw_error (bool): Whether or not to throw an error if unsuccessful.
        
        Returns: dict
        """
        config = configparser.ConfigParser()
        
        # Check if the file exists
        if not _filepath_exists(filepath) and not _filepath_exists(self._filepath):
            if throw_error:
                raise FileNotFoundError(f"The file at {filepath} does not exist.")
            else:
                return None
        if not _filepath_exists(filepath): filepath = self._filepath
        
        try:
            # Read the .ini file
            config.read(filepath)
            
            # Check if the file was loaded successfully
            if not config.sections():
                if throw_error:
                    raise ValueError(f"The file at {filepath} does not contain any sections.")
                else:
                    return None

            config_dict = {}
            # Loop through each section and its options
            for section in config.sections():
                # Add each section to the dictionary, creating a dictionary of key-value pairs
                config_dict[section] = {option: config.get(section, option) for option in config.options(section)}
            return config_dict

        except Exception as e:
            if throw_error:
                raise RuntimeError(f"An error occurred while reading the file: {str(e)}")
            else:
                return None
    
    def create_file(self, *args, filepath: TYPE_STRING_OR_NONE = None, throw_error: bool = True, **kwargs) -> None:
        """
        Create a file at the specified filepath.

        Arguments:
            filepath (str or None): The filepath to create the file at. If None or invalid, uses the default file path.
            throw_error (bool): Whether or not to throw an error if file creation fails.

        Returns:
            None
        """ 
        if not filepath or not _filepath_exists(os.path.dirname(filepath)): filepath = self._filepath
        self.write_to_file("", filepath=filepath, throw_error=throw_error)
    
    def delete_file(self, throws_error: bool = True) -> None:
        """
        Delete the file at the specified filepath.

        Arguments:
            throws_error (bool): Whether or not to throw an error if the file deletion fails.

        Returns:
            None
        """
        try:
            os.remove(self._filepath)
        except:
            if throws_error: raise FileExistsError("The file specified in the delete_file() method of the FileFactory class.")
            else: return
    
    def create_file_reader(self, filepath: str, *args, **kwargs) -> typing.Callable:
        """
        Create a function that reads the contents of a file.

        Arguments:
            filepath (str): The path to the file to be read.
            *args: Additional arguments to be passed to the read function.
            **kwargs: Additional keyword arguments to be passed to the read function.

        Returns:
            typing.Callable: A function that reads the contents of the file.
        """
        def read() -> str:
            with open(filepath, "r") as f:
                return f.read()
        return read
    
    def create_file_writer(self, filepath: str, mode: typing.Literal["w", "a"] = "w", *args, **kwargs) -> typing.Callable:
        """
        Create a function that writes data to a file.

        Arguments:
            filepath (str): The path to the file to be written to.
            mode (typing.Literal["w", "a"]): The mode to use when opening the file ("w" for write, "a" for append).
            *args: Additional arguments to be passed to the write function.
            **kwargs: Additional keyword arguments to be passed to the write function.

        Returns:
            typing.Callable: A function that writes data to the file.
        """
        def write(data: str) -> None:
            with open(filepath, mode) as file:
                file.write(data)
        return write
    
    def create_json_reader(self, filepath: str, *args, **kwargs) -> typing.Callable:
        """
        Create a function that reads a JSON file and returns its contents as a dictionary.

        Arguments:
            filepath (str): The path to the JSON file to be read.
            *args: Additional arguments to be passed to the read_json function.
            **kwargs: Additional keyword arguments to be passed to the read_json function.

        Returns:
            typing.Callable: A function that reads the contents of the JSON file and returns a dictionary.
        """
        def read_json() -> dict:
            with open(filepath, "r") as f:
                return json.load(f)
        return read_json

    def create_json_writer(self, filepath: str, *args, **kwargs) -> typing.Callable:
        """
        Create a function that writes a dictionary to a JSON file.

        Arguments:
            filepath (str): The path to the JSON file to be written.
            *args: Additional arguments to be passed to the write_json function.
            **kwargs: Additional keyword arguments to be passed to the write_json function.

        Returns:
            typing.Callable: A function that writes a dictionary to a JSON file.
        """
        def write_json(data: dict, indent: int = 4) -> None:
            with open(filepath, "w") as file:
                json.dump(data, file, indent=indent)
        return write_json
    
    def create_ini_reader(self, filepath: str, *args, **kwargs) -> typing.Callable:
        """
        Create a function that reads an INI file and returns its contents as a dictionary.

        Arguments:
            filepath (str): The path to the INI file to be read.
            *args: Additional arguments to be passed to the read_ini function.
            **kwargs: Additional keyword arguments to be passed to the read_ini function.

        Returns:
            typing.Callable: A function that reads the contents of the INI file and returns a dictionary.
        """
        def read_ini() -> dict:
            parser = configparser.ConfigParser()
            parser.read(filepath)
            config_dict = {}
            # Loop through each section and its options
            for section in parser.sections():
                # Add each section to the dictionary, creating a dictionary of key-value pairs
                config_dict[section] = {option: parser.get(section, option) for option in parser.options(section)}
            return config_dict
        return read_ini
    
    class FileManager:
        """
        A class that provides file management operations, including reading, writing, and reading/writing bytes.
        """

        def __init__(self, filepath: str) -> None:
            """
            Initialize the FileManager with the specified filepath.

            Arguments:
                filepath (str): The path to the file to be managed.
            """
            self.filepath = filepath

        def read(self) -> str:
            """
            Read the contents of the file.

            Returns:
                str: The contents of the file.
            """
            with open(self.filepath, "r") as f:
                return f.read()

        def write(self, data: str, mode: typing.Literal["w", "a"] = "w", *args, **kwargs) -> None:
            """
            Write data to the file.

            Arguments:
                data (str): The data to be written to the file.
                mode (typing.Literal["w", "a"]): The mode to use when opening the file ("w" for write, "a" for append).
            """
            with open(self.filepath, mode) as file:
                file.write(data)

        def read_bytes(self, num_bytes: typing.Optional[int] = None) -> bytes:
            """
            Read the contents of the file in bytes.

            Arguments:
                num_bytes (typing.Optional[int]): The number of bytes to read. If None, the entire file will be read.

            Returns:
                bytes: The contents of the file in bytes.
            """
            with open(self.filepath, "rb") as file:
                if num_bytes:
                    return file.read(num_bytes)
                else:
                    return file.read()

        def write_bytes(self, data: bytes, mode: typing.Literal["w", "a"]) -> None:
            """
            Write bytes to the file.

            Arguments:
                data (bytes): The bytes to be written to the file.
                mode (typing.Literal["w", "a"]): The mode to use when opening the file ("w" for write, "a" for append).
            """
            with open(self.filepath, mode + "b") as file:
                file.write(data)

    def create_file_manager(self, filepath: str, *args, **kwargs) -> FileManager:
        """
        Create a FileManager instance for the specified filepath.

        Arguments:
            filepath (str): The path to the file to be managed.

        Returns:
            FileManager: A FileManager instance for the specified filepath.
        """
        return self.FileManager(filepath)
    
    class JsonFileManager:
        """
        A class that provides file management operations specifically for JSON files.
        """

        def __init__(self, filepath: str):
            """
            Initialize the JsonFileManager with the specified filepath.

            Arguments:
                filepath (str): The path to the JSON file to be managed.
            """
            self.filepath = filepath

        def read(self) -> dict:
            """
            Read the contents of the JSON file and return it as a dictionary.

            Returns:
                dict: The contents of the JSON file as a dictionary.
            """
            with open(self.filepath, "r") as f:
                return json.load(f)

        def write(self, data: dict, indent: int = 4) -> None:
            """
            Write a dictionary to the JSON file.

            Arguments:
                data (dict): The dictionary to be written to the JSON file.
                indent (int): The number of spaces to use for indentation when writing the JSON file.
            """
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=indent)
    
    def create_json_file_manager(self, filepath: str, *args, **kwargs) -> JsonFileManager:
        """
        Create a JsonFileManager instance for the specified filepath.

        Arguments:
            filepath (str): The path to the JSON file to be managed.

        Returns:
            JsonFileManager: A JsonFileManager instance for the specified filepath.
        """
        return self.JsonFileManager(filepath)

class ConfigGetterFactory:
    """
    A class responsible for managing the configuration file and providing access 
    to specific configuration settings.

    This class loads configuration data from a JSON file, allows updating of the configuration, 
    and provides access to various configuration properties such as username, rounding, 
    angle units, and more. It also provides a method to reset the configuration to its default values.

    Attributes:
        filepath (str): The file path to the configuration JSON file.
        config (dict): The configuration data loaded from the JSON file.
        _manager (utils.FileFactory): An instance of a file manager for reading and writing the JSON file.
        valid_keys (tuple[str]): The valid keys for the config file.
    """

    def __init__(self, filepath: str) -> None:
        """
        Initialize the ConfigGetterFactory with the given file path.

        This method initializes the class by setting the file path and loading 
        the configuration from the specified JSON file using a file manager.

        Parameters:
            filepath (str): The file path to the configuration JSON file.

        Returns:
            None
        """
        self.filepath = filepath
        self._manager = _FileFactory().create_json_file_manager(self.filepath)
        self.config = self._manager.read()
        self.valid_keys = (
        "username",
        "rounding",
        "angle_unit",
        "show_error_windows",
        "default_tab",
        "terminalprompt",
        "subjects",
        "timetable",
        "recent_files",
        "cps_highscore"
        )
        self.defaults = {"username": "Default User", "rounding": 3, "angle_unit": "Degrees",
            "show_error_windows": True, "default_tab": "Home Tab", "terminalprompt": "PUtilities $",
            "subjects": ["No Subject Selected"],
            "timetable": {"Monday": ["No Subject Selected", "No Subject Selected", "No Subject Selected", "No Subject Selected"],
                "Tuesday": ["No Subject Selected", "No Subject Selected", "No Subject Selected", "No Subject Selected"],
                "Wednesday": ["No Subject Selected", "No Subject Selected", "No Subject Selected", "No Subject Selected"],
                "Thursday": ["No Subject Selected", "No Subject Selected", "No Subject Selected", "No Subject Selected"],
                "Friday": ["No Subject Selected", "No Subject Selected", "No Subject Selected", "No Subject Selected"],
                "Saturday": ["No Subject (weekend)", "No Subject (weekend)", "No Subject (weekend)"],
                "Sunday": ["No Subject (weekend)", "No Subject (weekend)", "No Subject (weekend)"]},
            "recent_files": [],
            "cps_highscore": 0}
    
    def write(self, config_data: dict[str, typing.Any], safe_mode: bool = True) -> None:
        """
        Write the provided configuration data to the JSON file.

        This method writes the configuration data to the file, ensuring that only 
        valid keys are included in the configuration when in safe mode.

        Parameters:
            config_data (dict): A dictionary of configuration data to be written.
            safe_mode (bool): A flag to enable safe mode, which restricts the valid keys.

        Returns:
            None
        """
        if safe_mode:
            for key in config_data.keys():
                if not key in self.valid_keys: return
            for key in self.valid_keys:
                if not key in config_data.keys(): return
        self._manager.write(config_data)
    
    def update_config(self) -> None:
        """
        Update the in-memory configuration by reloading it from the file.

        This method fetches the latest configuration data from the file and updates 
        the `config` attribute.

        Parameters:
            None

        Returns:
            None
        """
        self.config = self._manager.read()

    def get_all(self) -> None:
        """
        Retrieve all the configuration data.

        This method updates the in-memory configuration and returns the entire configuration data.

        Parameters:
            None

        Returns:
            dict: The full configuration data.
        """
        self.update_config()
        return self.config
    
    def get_key(self, key: str) -> typing.Any:
        """
        Retrieve a specific configuration value by its key.

        This method updates the in-memory configuration and returns the value 
        associated with the specified key. If not found, then looks to the default values.

        Parameters:
            key (str): The key for which the value is to be retrieved.

        Returns:
            typing.Any: The value associated with the key, or None if the key is not found.
        """
        self.update_config()
        return self.config.get(key, self.defaults.get(key, None))
    
    @property
    def username(self) -> str:
        """
        Retrieve the username from the configuration.

        This property updates the in-memory configuration and returns the username 
        stored in the configuration, or "Default User" if not set.

        Parameters:
            None

        Returns:
            str: The username from the configuration.
        """
        self.update_config()
        return self.get_key("username")
    
    @property
    def rounding(self) -> int | None:
        """
        Retrieve the rounding value from the configuration.

        This property updates the in-memory configuration and returns the rounding 
        value stored in the configuration, or 3 if not set.

        Parameters:
            None

        Returns:
            int | None: The rounding value from the configuration.
        """
        self.update_config()
        return self.get_key("rounding")
    
    @property
    def angle_unit(self) -> typing.Literal["Degrees", "Radians"]:
        """
        Retrieve the angle unit from the configuration.

        This property updates the in-memory configuration and returns the angle 
        unit (either "Degrees" or "Radians") from the configuration, or "Degrees" if not set.

        Parameters:
            None

        Returns:
            str: The angle unit from the configuration.
        """
        self.update_config()
        return self.get_key("angle_unit")
    
    @property
    def show_error_windows(self) -> bool:
        """
        Retrieve the show_error_windows setting from the configuration.

        This property updates the in-memory configuration and returns whether 
        error windows should be shown, or True if not set.

        Parameters:
            None

        Returns:
            bool: The show_error_windows setting from the configuration.
        """
        self.update_config()
        return self.get_key("show_error_windows")
    
    @property
    def default_tab(self) -> typing.Literal["Home Tab", "Text Editor", "Terminal", "Simple Calculator", "Lesson Editor", "File Explorer"]:
        """
        Retrieve the default tab setting from the configuration.

        This property updates the in-memory configuration and returns the default 
        tab to open, or "Home Tab" if not set.

        Parameters:
            None

        Returns:
            str: The default tab setting from the configuration.
        """
        self.update_config()
        return self.get_key("default_tab")
    
    @property
    def terminal_prompt(self) -> str:
        """
        Retrieve the terminal prompt from the configuration.

        This property updates the in-memory configuration and returns the terminal 
        prompt string, or "PUtilities $" if not set.

        Parameters:
            None

        Returns:
            str: The terminal prompt string from the configuration.
        """
        self.update_config()
        return self.get_key("terminalprompt")
    
    @property
    def subject_list(self) -> list[str]:
        """
        Retrieve the list of subjects from the configuration.

        This property updates the in-memory configuration and returns the list of 
        subjects, or ["No Subject Selected"] if not set.

        Parameters:
            None

        Returns:
            list[str]: The list of subjects from the configuration.
        """
        self.update_config()
        return self.get_key("subjects")
    
    @property
    def timetable(self) -> dict[str, list]:
        """
        Retrieve the timetable from the configuration.

        This property updates the in-memory configuration and returns the timetable 
        data, or a default timetable if not set.

        Parameters:
            None

        Returns:
            dict: The timetable data from the configuration.
        """
        self.update_config()
        return self.get_key("timetable")

    @property
    def recent_files(self) -> list[str]:
        """
        Retrieve the list of recently accessed files.

        This property fetches the list of recently accessed files from the configuration 
        and returns it as a list of strings. The configuration is updated before accessing the data.

        Returns:
            list[str]: A list of strings representing the paths of recently accessed files.
        """
        self.update_config()
        return self.get_key("recent_files")

    def add_recent_file(self, latest: str) -> None:
        """
        Add a recent file to the recent files list.

        This setter method adds a new file to the beginning of the recent files list, ensuring 
        that the list does not exceed a specified maximum length (10). The configuration is updated 
        and written back after the modification.

        Parameters:
            latest (str): The path of the file to add to the list of recently accessed files.

        Returns:
            None
        """
        file_list = self.recent_files
        if latest in file_list: file_list.remove(latest)
        file_list.insert(0, latest)
        if len(file_list) > 10:
            file_list.pop(-1)
        self.config["recent_files"] = file_list
        self.write(self.config)
    
    @property
    def cps_highscore(self) -> None:
        """Get the highscore for the CpsTester tab."""
        return self.get_key("cps_highscore")

    @cps_highscore.setter
    def cps_highscore(self, new: int) -> None:
        """Set the highscore of the CpsTester tab."""
        self._write_value("cps_highscore", new)
    
    def reset_to_defaults(self, make_sure: bool = True) -> None:
        """
        Reset the configuration to its default values.

        This method resets the configuration data to predefined default values, 
        optionally asking the user for confirmation before proceeding.

        Parameters:
            make_sure (bool): A flag that asks for confirmation before resetting the configuration.

        Returns:
            None
        """
        if not make_sure or messagebox.askokcancel("Confirm Operation", "Will reset configuration to defaults. Confirm?"):
            self._manager.write(self.defaults, 4)
    
    def _write_value(self, key: str, value: typing.Any) -> None:
        """
        Write a specific key's value. Do not use outside the ConfigGetterFactory.

        Parameters:
            key (str): The key to write to.
            value (Any): What value to write
        
        Returns:
            None
        """
        if not key in self.valid_keys: return
        self.config[key] = value
        self._manager.write(self.config)

CONFIGURATION = ConfigGetterFactory(_getRootFilepath() + "/config/config.json")

class ErrorLogFactory:
    """
    A class responsible for managing the error log file, including logging error messages
    and resetting the log to start a new session.

    This class provides methods for logging error messages to a specified log file and for 
    resetting the log with session details. It writes error messages to the file in an 
    append mode and also supports initializing the log file with session information.

    Attributes:
        filepath (str): The file path to the error log file.
        manager (utils.FileFactory): A file manager responsible for writing to the log file.
    """

    def __init__(self, filepath: str):
        """
        Initialize the ErrorLogFactory with the given file path.

        This method sets up the file path for the error log and creates a file manager 
        to manage writing to the log file.

        Parameters:
            filepath (str): The file path where the error log will be stored.

        Returns:
            None
        """
        self.filepath = filepath
        self.manager = _FileFactory().create_file_manager(filepath)
    
    def reset(self) -> None:
        """
        Reset the error log, adding session details at the start.

        This method clears the current log and writes session information such as 
        the date and time the session started. It initializes the error log with 
        a header and session details.

        Parameters:
            None

        Returns:
            None
        """
        self.manager.write(f"# PUtilities Error Log\n\n## Session Details\nDate: {get_date()}\nTime: {get_hour_minute()}\n\n## Error Log\n")
    
    def log(self, message: str, end: str = "\n") -> None:
        """
        Log an error message to the log file.

        This method appends an error message to the error log file. If the `end` 
        argument is specified, it will be used to control how the message ends 
        (default is a newline).

        Parameters:
            message (str): The error message to log.
            end (str, optional): The string to append to the message (default is a newline).

        Returns:
            None
        """
        self.manager.write(message + end, "a")
    
    def log_tab_error(self, tab_name: str, error_message: str) -> None:
        """
        Log an error from a given tab, in the format:
        [TabName] Error message.

        Arguments:
            tab_name (str): The name of the tab the error is from.
            error_message (str): The error message.
        
        Returns:
            None
        """
        self.log(f"[{tab_name}] {error_message}")

ERROR_LOG = ErrorLogFactory(_getRootFilepath() + "/config/errorlog.md")

class PFileHandler:
    """
    PUtilities File Handler Utility
    Used for creating, modifying, and reading files within the PUtilities Ecosystem.
    Static class, meaning that no instance of the class needs to be created. Instead, simply type PFileHandler.method()
    """

    ROOT_FILEPATH = _getRootFilepath()
    ASSETS_FILEPATH = ROOT_FILEPATH + "/assets"
    TAB_ICONS_FILEPATH = ASSETS_FILEPATH + "/tab icons"
    CONFIG_FILEPATH = ROOT_FILEPATH + "/config"
    CLASSES_FILEPATH = ROOT_FILEPATH + "/classes"

    TYPE_FILEPATH = str | pathlib.Path | os.PathLike | None

    def get_raw_filepath(filepath: TYPE_FILEPATH) -> str:
        """
        Get the raw (direct) filepath of a given filepath.

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to get the raw filepath of.
        
        Returns:
            str
        """
        return get_raw_filepath(filepath)

    def get_filename_with_extension(filepath: TYPE_FILEPATH) -> str:
        """
        Get the filename of a given filepath, including the extension.
        e.g. D:/Documents/helloworld.py --> helloworld.py

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to extract the filename from.
        
        Returns:
            str
        """
        return get_filename_of_filepath(filepath)

    def get_filename_without_extension(filepath: TYPE_FILEPATH) -> str:
        """
        Get the filename of a given filepath, not including the extension.
        e.g. D:/Documents/helloworld.py --> helloworld

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to extract the filename from.
        
        Returns:
            str
        """
        return _filename_advanced(filepath)
    
    def create_file_manager(filepath: TYPE_FILEPATH) -> _FileFactory.JsonFileManager:
        """
        Create a file manager to assign to a variable, with methods to load, save, etc.
        Returns a class representing the file with these methods.

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to assign the file to.

        Returns:
            FileManager
        """
        return _FileFactory.FileManager(filepath=filepath)
    
    def create_json_file_manager(filepath: TYPE_FILEPATH) -> _FileFactory.JsonFileManager:
        """
        Create a json file manager to assign to a variable, with methods to load, save, etc.
        Returns a class representing the json file with these methods.

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to assign the json file to.

        Returns:
            JsonFileManager
        """
        return _FileFactory.JsonFileManager(filepath=filepath)
    
    def filepath_exists(filepath: TYPE_FILEPATH) -> bool:
        """
        Check if a given filepath exists.

        Arguments:
            filepath (TYPE_FILEPATH): The filepath to check.

        Returns:
            bool
        """
        return _filepath_exists(filepath)

    def get_tab_icon(tab_icon_filename: str) -> tk.PhotoImage:
        """
        Get a tab icon with the given tab name. Returns a tk.PhotoImage, and default icon if not found.
        """
        filepath = PFileHandler.TAB_ICONS_FILEPATH + "/" + tab_icon_filename
        if not PFileHandler.filepath_exists(filepath): return tk.PhotoImage(file=PFileHandler.TAB_ICONS_FILEPATH + "/default tab icon.png")
        return tk.PhotoImage(file=filepath)

class PConstants:
    """
    Standard constants used in PUtilities.
    """

    # Main
    PUTILITIES_VERSION: str = "1.0.1"
    PUTILITIES_RELEASE_TYPE: str = "dev"

    # Files
    ROOT_FILEPATH: str = PFileHandler.ROOT_FILEPATH
    ASSETS_FILEPATH: str = PFileHandler.ASSETS_FILEPATH
    CONFIG_FILEPATH: str = PFileHandler.CONFIG_FILEPATH
    CLASSES_FILEPATH: str = PFileHandler.CLASSES_FILEPATH

    # Tab Names
    tab_calculator: str = "Calculator"
    tab_command_line: str = "Command Line"
    tab_file_explorer: str = "File Explorer"
    tab_home: str = "Home"
    tab_image_viewer: str = "Image Viewer"
    tab_lesson_editor: str = "Lesson Editor"
    tab_linux_terminal: str = "Linux Terminal"
    tab_right_triangle_calculator: str = "Right Triangle Calculator"
    window_settings_dialogue: str = "Settings Dialogue"
    tab_text_editor: str = "Text Editor"
    tab_unit_converter: str = "Unit Converter"

    # Colours
    light_grey: str = "#E0E0E0"
    orange: str = "#FE9900"
    dark_grey: str = "#2E2E2E"
    grey_black: str = "#1E1E1E"

    # Fonts
    arial_14 = ("Arial", 14)
    arial_16 = ("Arial", 16)
    arial_18 = ("Arial", 18)
    arial_22 = ("Arial", 22)
    arial_24 = ("Arial", 24)
    arial_12 = ("Arial", 12)
    arial_11 = ("Arial", 11)
    arial_10 = ("Arial", 10)
    arial_14 = ("Arial", 14)

    # Utility Constants
    hello_world: str = "Hello, World!"
    unknown_error_message: str = "An unknown error occurred. Consider restarting program."
    error_general: str = "Error!"
    error_fatal: str = "Fatal Error!"
    error_warning: str = "Warning!"
    all_files: tuple[str, tuple[str]] = ("All Files", ("*.*"))
    text_documents: tuple[str, tuple[str]] = ("Text Documents", ("*.txt"))
    lesson_files: tuple[str, tuple[str]] = ("Lesson Files", ("*.json"))
    json_files: tuple[str, tuple[str]] = ("JSON Files", ("*.json"))
    filepath_type: type = PFileHandler.TYPE_FILEPATH

class PTkUtils:
    """
    A utility class with general tkinter functions.
    """

    def clear_entry(entry: ttk.Entry | tk.Entry) -> None:
        """
        Clear all text from an entry.
        """
        entry.delete(0, tk.END)
    
    def pack(widget, side: str = tk.TOP, anchor: str = tk.NW, padx: int = 5, pady: int = 2, expand: int = 0, fill: str = tk.NONE) -> None:
        """Quickly pack a widget with default settings."""
        widget.pack(side=side, anchor=anchor, padx=padx, pady=pady)

class WindowInterface(abc.ABC):
    """
    A high level interface for defining what the PUtilties window can do.
    Defines the set methods of the window for type checking.
    """

    @abc.abstractmethod
    def start(self) -> None:
        """
        Start the program. Calls the internal functions _CreateWidgets() and _CreateMenu(), and starts the mainloop of the window.

        Returns: None
        """
        pass

    def getCurrentTab(self) -> TabFrame:
        """
        Gets the current tab in the form of its object (tabframe). This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        pass

    def getFinalTab(self) -> TabFrame:
        """
        Gets the final tab in the form of its object (tabframe). This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        pass
    
    @abc.abstractmethod
    def getTabAtIndex(self, index: int = -1) -> typing.Any:
        """
        Gets the tab at a certain index in the form of its object (tabframe).
        This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        pass

    @abc.abstractmethod
    def switchToFinalTab(self) -> None:
        """
        Switches to the final tab. Can be called from outside the Window class.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToTabAtIndex(self, index: int = -1) -> None:
        """
        Switches to a tab at a certain index. Can be called from outside the Window class.

        Args:
            index (int): The index of the tab in the current tabs you are wishing to switch to.
                         If that index does not exist, will use the modulus operator to always get a valid index.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToNextTab(self, event=None) -> None:
        """
        Switch to the next tab. If at final tab, then switches back to the first tab.
        Also called using the keyboard shortcut Shift+Right. Do not touch the event arg.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToPreviousTab(self, event=None) -> None:
        """
        Switch to the previous tab. If at starting tab, then loops back around to the last tab.
        Also called using the keyboard shortcut Shift+Left. Do not touch the event arg.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def getTabList(self) -> list:
        """
        Returns the tab list. Only meant to be used in the other methods surrounding tabs.

        Returns: list -> A list of the tab identifiers.
        """
        pass

    @abc.abstractmethod
    def getTabAtIndex(self, index: int = -1) -> typing.Any:
        """
        Gets the tab at a certain index in the form of its object (tabframe).
        This object can then be used to call the methods of the tab.

        Returns: TabFrame
        """
        pass

    @abc.abstractmethod
    def switchToFinalTab(self) -> None:
        """
        Switches to the final tab. Can be called from outside the Window class.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToTabAtIndex(self, index: int = -1) -> None:
        """
        Switches to a tab at a certain index. Can be called from outside the Window class.

        Args:
            index (int): The index of the tab in the current tabs you are wishing to switch to.
                         If that index does not exist, will use the modulus operator to always get a valid index.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToNextTab(self, event=None) -> None:
        """
        Switch to the next tab. If at final tab, then switches back to the first tab.
        Also called using the keyboard shortcut Shift+Right. Do not touch the event arg.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def switchToPreviousTab(self, event=None) -> None:
        """
        Switch to the previous tab. If at starting tab, then loops back around to the last tab.
        Also called using the keyboard shortcut Shift+Left. Do not touch the event arg.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def getTabList(self) -> list:
        """
        Returns the tab list. Only meant to be used in the other methods surrounding tabs.

        Returns: list -> A list of the tab identifiers.
        """
        pass

    @abc.abstractmethod
    def newTab(self, tabframe: typing.Any, name: str = "New Tab") -> None:
        """
        Creates a new tab using the tabs class and the name of the tab. Then switches to that final tab.
        Generally, the following lambda expression is used when adding to a given menu:
            command=lambda: self.newTab(tabs.YourTabName(self))

        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into.
                                 Pass your class initialised with the master of the window (self).
                                 Calls the _onTabCreation() method of the tab you are adding.
            name (str): The name of the tab. Generally, this does not need to be set when defining
                        the TabFrame.tabname property in the TabFrame.init() method.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def newTabAndOpen(self, tabframe: typing.Any, name: str = "New Tab") -> None:
        """
        Creates a new tab with newTab and calls the open dialogue for that tab.
        Usually used when adding a command to the open menu under the file menu.

        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into.
                                 Pass your class initialised with the master of the window (self).
                                 Calls the _onTabCreation() method of the tab you are adding.
            name (str): The name of the tab. Generally, this does not need to be set when defining
                        the TabFrame.tabname property in the TabFrame.init() method.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def newTabAndAutoload(self, tabframe: typing.Any, filepath: str, name: str = "New Tab") -> None:
        """
        Creates a new tab with newTab and calls the autoload method for that tab.
        Usually used only from the file explorer.

        Args:
            tabframe (TabFrame): Your TabFrame class that you are opening a new tab into.
                                 Pass your class initialised with the master of the window (self).
                                 Calls the _onTabCreation() method of the tab you are adding.
            filepath (str): The filepath of the file to autoload. Be noted that the file must be
                            dealt with in the tab for any errors.
            name (str): The name of the tab. Generally, this does not need to be set when defining
                        the TabFrame.tabname property in the TabFrame.init() method.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def changeCurrentTabName(self, newName: str) -> None:
        """
        Change the current tab's name. Intended to be called from both in and outside the Window class.
        Also called when modifying the tabname attribute of the TabFrame class, so that the tab is renamed instantly.

        Args:
            newName (str): The new name that you want the tab to be called.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def clearTabOptions(self) -> None:
        """
        Clears the tab options menu. Called automatically when the tab is changed,
        before the new tab options are added.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def save(self, event=None) -> None:
        """
        Calls the current tab's save() method. Also called with the keyboard shortcut Control+s.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def saveAs(self, event=None) -> None:
        """
        Calls the current tab's saveAs() method. Also called with the keyboard shortcut Control+Shift+s.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def open(self, event=None) -> None:
        """
        Calls the current tab's open() method. Also called with the keyboard shortcut Control+o.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def new(self, event=None) -> None:
        """
        Calls the current tab's new() method. Also called with the keyboard shortcut Control+n.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def clearExportMenu(self) -> None:
        """
        Clears the export menu when the tab is changed, preparing it for adding new items to the export menu.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def openSettingsDialogue(self) -> None:
        """
        Open the settings dialogue. Will create a new window for the dialogue, and runs in parallel.

        Returns: None
        """
        pass

    @abc.abstractmethod
    def open_file_in_specific_tab(self, filepath: str) -> None:
        """
        Open a given filepath in its available tab.

        Returns: None
        """
        pass

