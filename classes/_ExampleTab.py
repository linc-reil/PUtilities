"""PUtilities tabs can be made quickly and easily!
See here an example tab with tab functions and widgets!

While testing the tab, add it to the testingMenu in the Window. Make sure to add it to _imports to ensure
you can access it in the Window class."""

from classes.Utilities import * # Import the utilities, including the TabFrame and external imports.

class ExampleTab(TabFrame): # Create the example tab class.
    _name = "Example Tab"
    _description = "An example tab showcasing the developement of tabs in PUtilities."
    _icon = "example tab icon.png"

    def init(self) -> None: # Runs the first time the tab is opened.
        self.tabname = "Example" # Set the tab's name.
        self.counter = 0 # Define variables here!
        self.label = ttk.Label(self, text="Example Tab!") # Create widgets just like in any other frame.
        self.label.pack() # Same method to back widgets.
        self.button = ttk.Button(self, text="Click Me!", command=self.addcount) # Buttons can be connected to
        self.button.pack() # Other functions in the class.

    def createTabCommands(self): # Must-define method for creating tab commands!
        self.addTabFunction("Reset Button", self.resetcount)
    
    def addcount(self) -> None: # Define any methods you need to use in the class!
        self.counter += 1 # Access variables defined in initialisation!
        self.button.config(text=f"Button has been clicked {self.counter} time(s).")
    
    def resetcount(self) -> None: # This method runs off the tab options menu!
        self.counter = 0
        self.button.config(text="Click Me!")