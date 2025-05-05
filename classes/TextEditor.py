from classes.Utilities import *

class TextEditor(TabFrame):
    _name = "Text Editor"
    _description = "Edit text documents and other files."
    _icon = "text editor icon.png"

    def init(self):
        self.filepath = None
        self.tabname = "Text Editor"
        self.textbox = ScrollableTextBox(self)
        self.textbox.pack(expand=1, fill="both")
    
    def createTabCommands(self):
        self.addTabFunction("Insert Date", lambda: self.textbox.insertAtEnd(datetime.datetime.now().strftime("%d/%m/%Y")))
        self.addTabFunction("Clear Text", self.textbox.clear)
    
    def save(self) -> None:
        if not self.filepath:
            self.saveAs()
            return
        with open(self.filepath, "w") as f:
            f.write(self.textbox.getAll())
        CONFIGURATION.add_recent_file(self.filepath)
    
    def saveAs(self):
        if self.filepath:
            self.save()
        savepath = filedialog.asksaveasfilename(title="Save Text File", defaultextension=".txt", filetypes=[("Text Document", ("*.txt")), ("All Files", ("*.*"))])
        if not savepath or not os.path.exists(get_raw_filepath(savepath)):
            return
        self.filepath = savepath
        self.tabname = get_filename_of_filepath(savepath)
        self.save()
        CONFIGURATION.add_recent_file(self.filepath)
    
    def open(self) -> None:
        if self.filepath:
            self.save()
        loadpath = filedialog.askopenfilename(title="Open Text Document", filetypes=[("Text Document", "*.txt"), ("Markdown File", "*.md"), ("All Files", "*.*")])
        if not loadpath:
            return
        self.filepath = loadpath
        with open(self.filepath, "r") as f:
            self.textbox.clear()
            self.textbox.insertAtStart(f.read())
        CONFIGURATION.add_recent_file(self.filepath)
    
    def new(self):
        if self.filepath:
            self.save()
        self.textbox.clear()
        self.filepath = None
    
    def autoload(self, filepath):
        if not filepath or not os.path.exists(filepath) or not os.path.isfile(filepath): return
        if self.filepath: self.save()
        with open(filepath, "r") as f:
            self.textbox.clear()
            self.textbox.insertAtEnd(f.read())
        self.tabname = PFileHandler.get_filename_without_extension(filepath)
        self.filepath = filepath
        CONFIGURATION.add_recent_file(self.filepath)