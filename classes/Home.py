from classes.Utilities import *
from classes.Calculator import Calculator
from classes.TextEditor import TextEditor
from classes.UnitConverter import UnitConverter
from classes.ImageViewer import ImageViewer
from classes.CommandLine import CommandLine
from classes.FileExplorer import FileExplorer

class TimetableFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.timetable = CONFIGURATION.timetable.get(datetime.datetime.now().strftime("%A"), "Sunday")
        self.labelOne = ttk.Label(self, text=f"Period 1: {self.timetable[0]}", font=("Arial", 12))
        self.labelOne.grid(row=1, column=0, sticky="w")
        self.labelTwo = ttk.Label(self, text=f"Period 2: {self.timetable[1]}", font=("Arial", 12))
        self.labelTwo.grid(row=2, column=0, sticky="w")
        self.labelThree = ttk.Label(self, text=f"Period 3: {self.timetable[2]}", font=("Arial", 12))
        self.labelThree.grid(row=3, column=0, sticky="w")
        self.labelFour = ttk.Label(self, text=f"Period 4: {self.timetable[3]}", font=("Arial", 12))
        self.labelFour.grid(row=4, column=0, sticky="w")

class HomeScreen(TabFrame):
    _name = "Home Tab"
    _description = "PUtilities home tab and quick references."
    _icon = "home tab icon.png"
    
    def init(self):
        self.tabname = "Home"
        self.createWidgets()
        self.tick()
    
    def tick(self) -> None:
        self.info.config( text=f"{CONFIGURATION.username} - {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')}")
        self.update_recent_files()
        self.after(5000, self.tick)
    
    def createWidgets(self) -> None:
        self.header = ttk.Label(self, text="PUtilities School Edition", font=("Arial", 24))
        self.header.pack()
        self.info = ttk.Label(self, text=f"{CONFIGURATION.username} - {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')}")
        self.info.pack()
        self.frame = ttk.Frame(self)
        self.frame.pack(fill="both", anchor="n")
        self.calculatorButtonImage = self.getPhotoimage("calculator-icon_34473.png")
        self.calculatorButton = ttk.Button(self.frame, text="Open Simple Calculator", compound="top", image=self.calculatorButtonImage, command=lambda: self.window.newTab(Calculator(self.window)))
        self.calculatorButton.grid(row=0, column=0, padx=5, pady=5)
        self.textEditorButtonImage = self.getPhotoimage("text-document-icon.png")
        self.textEditorButton = ttk.Button(self.frame, text="Open Text Editor", compound="top", image=self.textEditorButtonImage, command=lambda: self.window.newTab(TextEditor(self.window)))
        self.textEditorButton.grid(row=0, column=1, padx=5, pady=5)
        self.unitConverterButtonImage = self.getPhotoimage("converter-icon.png")
        self.unitConverterButton = ttk.Button(self.frame, text="Open Unit Converter", compound="top", image=self.unitConverterButtonImage, command=lambda: self.window.newTab(UnitConverter(self.window)))
        self.unitConverterButton.grid(row=0, column=2, padx=5, pady=5)
        self.imageViewerButtonImage = self.getPhotoimage("image-viewer-icon.png")
        self.imageViewerButton = ttk.Button(self.frame, text="Open Image(s)", compound="top", image=self.imageViewerButtonImage, command=lambda: self.window.newTabAndOpen(ImageViewer(self.window)))
        self.imageViewerButton.grid(row=1, column=0, padx=5, pady=5)
        self.terminalButtonImage = self.getPhotoimage("terminal-shell-icon.png")
        self.terminalButton = ttk.Button(self.frame, text="Open Command Line", compound="top", image=self.terminalButtonImage, command=lambda: self.window.newTab(CommandLine(self.window)))
        self.terminalButton.grid(row=1, column=1, padx=5, pady=5)
        self.configButtonImage = self.getPhotoimage("config-icon.png")
        self.configButton = ttk.Button(self.frame, text="Configurate PUtilities", compound="top", image=self.configButtonImage, command=self.window.openSettingsDialogue)
        self.configButton.grid(row=1, column=2, padx=5, pady=5)
        self.fileExplorerButtonImage = self.getPhotoimage("fancy-folder-icon.png")
        self.fileExplorerButton = ttk.Button(self.frame, text="Open File Explorer", compound="top", image=self.fileExplorerButtonImage, command=lambda: self.window.newTab(FileExplorer(self.window)))
        self.fileExplorerButton.grid(row=0, column=3, padx=5, pady=5)

        self.timetableFrame = ttk.Frame(self.frame, border=2, borderwidth=2, relief="groove", width=150)
        self.timetableFrame.grid(row=0, column=4, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.timetableHeader = ttk.Label(self.timetableFrame, text="On Today", font=("Arial Bold", 14))
        self.timetableHeader.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.timetable = TimetableFrame(self.timetableFrame)
        self.timetable.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.recent_files_header = ttk.Label(self.timetableFrame, text="Recent Files", font=("Arial Bold", 14))
        self.recent_files_header.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.recent_files = tk.Listbox(self.timetableFrame)
        self.recent_files.grid(row=3, column=0, sticky="nsew", padx=5, pady=2)
        self.update_recent_files()
        self.recent_files.bind("<Double-1>", self.on_recent_file_selection)
    
    def update_recent_files(self) -> None:
        self.recent_files.delete(0, tk.END)
        for item in CONFIGURATION.recent_files:
            self.recent_files.insert(tk.END, PFileHandler.get_filename_with_extension(item))
    
    def on_recent_file_selection(self, event=None) -> None:
        try:
            selected_index = self.recent_files.curselection()[0]
            selected_index = int(selected_index)
        except:
            return
        selected: str = CONFIGURATION.recent_files[selected_index]
        self.window.open_file_in_specific_tab(selected)
    
    def open(self) -> None:
        filetypes = [("Text Document", "*.txt"), ("Lesson", "*.json"), ("All Files", "*.*")]
        openpath = filedialog.askopenfilename(title="Open File", filetypes=filetypes, defaultextension=".txt")
        if not openpath: return
        self.window.open_file_in_specific_tab(openpath)
