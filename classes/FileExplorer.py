from classes.Utilities import *
from shutil import rmtree
from classes.TextEditor import TextEditor
from classes.LessonEditor import LessonEditor
from classes.ImageViewer import ImageViewer

class NewFileDialogue(tk.Toplevel):
    def __init__(self, master=None) -> None:
        super().__init__(master=master)
        self.title("Create New File")
        self.geometry("400x200")

        self.header = ttk.Label(self, text="New File", font=("Arial", 14))
        self.header.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="nw")
        self.filenameLabel = ttk.Label(self, text="Name:")
        self.filenameLabel.grid(row=1, column=0, padx=5, pady=2, sticky="nw")
        self.filenameEntry = ttk.Entry(self, width=35)
        self.filenameEntry.grid(row=1, column=1, padx=5, pady=2, sticky="nw")

        self.file_type_options = ["Text Document (.txt)", "Lesson (.json)", "Other Format (.*)"]
        self.selected_file_type = tk.StringVar(self, self.file_type_options[0])
        self.file_type_label = ttk.Label(self, text="Type:")
        self.file_type_label.grid(row=2, column=0, padx=5, pady=2, sticky="nw")
        self.file_type_selector = ttk.Combobox(self, textvariable=self.selected_file_type, values=self.file_type_options)
        self.file_type_selector.grid(row=2, column=1, padx=5, pady=2, sticky="nw")

        self.buttonsFrame = ttk.Frame(self)
        self.buttonsFrame.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        self.cancelButton = ttk.Button(self.buttonsFrame, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side="left", anchor="w", padx=5, pady=2)
        self.acceptButton = ttk.Button(self.buttonsFrame, text="Confirm", command=self.accept)
        self.acceptButton.pack(side="left", anchor="w", padx=5, pady=2)

        self.wait_window(self)
    
    def cancel(self) -> None:
        self.result = None
        self.destroy()
    
    def accept(self) -> dict[str: str]:
        """Returns a dictionary of the form: {
        "name": string,
        "type": string (possible 'lesson', 'text', or 'other')}"""
        index = self.file_type_options.index(self.selected_file_type.get())
        if index == 0: type_ = "text"
        elif index == 1: type_ = "lesson"
        else: type_ = "other"
        self.result = {"name": self.filenameEntry.get().strip(), "type": type_}
        self.destroy()

class NewFolderDialogue(tk.Toplevel):
    def __init__(self, master=None) -> None:
        super().__init__(master=master)
        self.title("Create New Folder")
        self.geometry("400x200")

        self.header = ttk.Label(self, text="Create New Folder", font=("Arial", 16))
        self.header.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="nw")
        self.filenameLabel = ttk.Label(self, text="Folder name")
        self.filenameLabel.grid(row=1, column=0, padx=5, pady=2, sticky="nw")
        self.filenameEntry = ttk.Entry(self, width=35)
        self.filenameEntry.grid(row=1, column=1, padx=5, pady=2, sticky="nw")
        self.buttonsFrame = ttk.Frame(self)
        self.buttonsFrame.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        self.cancelButton = ttk.Button(self.buttonsFrame, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side="left", anchor="w", padx=5, pady=2)
        self.acceptButton = ttk.Button(self.buttonsFrame, text="Confirm", command=self.accept)
        self.acceptButton.pack(side="left", anchor="w", padx=5, pady=2)

        self.wait_window(self)
    
    def cancel(self) -> None:
        self.result = None
        self.destroy()
    
    def accept(self) -> None:
        self.result = self.filenameEntry.get().strip()
        self.destroy()

class FileExplorer(TabFrame):
    """
    File Explorer tab using OS.path utilities to quickly navigate through filepaths and open files in PUtilities.
    """
    _name = "File Explorer"
    _description = "A file explorer to open and navigate files."
    _icon = "file explorer icon.png"

    def init(self):
        self.tabname = "File Explorer"
        self.currentfilepath = "D:"
        
        self.buttonsFrame = ttk.Frame(self, height=10)
        self.buttonsFrame.pack(anchor="w")

        self.navigateButtonImage = self.getPhotoimage("folder-icon-76px.png")
        self.navigateButton = ttk.Button(self.buttonsFrame, text="Navigate", compound="top", image=self.navigateButtonImage, command=self.navigate)
        self.navigateButton.pack(side="left", anchor="w")
        self.newFileButtonImage = self.getPhotoimage("new-file-icon-76px.png")
        self.newFileButton = ttk.Button(self.buttonsFrame, text="New File", compound="top", image=self.newFileButtonImage, command=self.new)
        self.newFileButton.pack(side="left", anchor="w")
        self.newFolderButtonImage = self.getPhotoimage("new-folder-icon-76px.png")
        self.newFolderButton = ttk.Button(self.buttonsFrame, text="New Folder", compound="top", image=self.newFolderButtonImage, command=self.newFolder)
        self.newFolderButton.pack(side="left", anchor="w")
        self.deleteButtonImage = self.getPhotoimage("delete-icon-76px.png")
        self.deleteButton = ttk.Button(self.buttonsFrame, text="Delete", compound="top", image=self.deleteButtonImage, command=self.deleteItem)
        self.deleteButton.pack(side="left", anchor="w")

        self.fileTree = ttk.Treeview(self, columns=("Size", "Type"))
        self.fileTree.pack(fill="both", expand=1, anchor="n")

        self.fileTree.heading("#0", text="Name", anchor="w")
        self.fileTree.heading("Size", text="Size", anchor="w")
        self.fileTree.heading("Type", text="Type", anchor="w")

        self.fileTree.column("#0", stretch=True)
        self.fileTree.column("Size", stretch=False, width=200)
        self.fileTree.column("Type", stretch=False, width=200)

        self.fileTree.bind("<Double-1>", self.onTreeItemDoubleClick)
        self.loadCurrentFilepath()

    def loadCurrentFilepath(self) -> None:
        try:
            for item in self.fileTree.get_children():
                self.fileTree.delete(item)
            self.fileTree.insert("", "end", text="..", values=("", "Directory"), open=True, iid="..")

            files, directories = [], []

            for _filename in os.listdir(self.currentfilepath):
                full_path = os.path.join(self.currentfilepath, _filename)
                if os.path.isdir(full_path):
                    directories.append(full_path)
                elif os.path.isfile(full_path):
                    files.append(full_path)
            
            for directory in directories:
                size, type_ = "n/a", "Directory"
                self.fileTree.insert("", "end", text=get_filename_of_filepath(directory), values=(size, type_), iid=directory)
            for file in files:
                size, type_ = f"{os.path.getsize(file)} bytes", "File"
                self.fileTree.insert("", "end", text=get_filename_of_filepath(file), values=(size, type_), iid=file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load filepath {self.currentfilepath}. Error type: {str(e)}")
            self.currentfilepath = os.path.dirname(self.currentfilepath)
    
    def onTreeItemDoubleClick(self, event=None) -> None:
        selectedItem = self.fileTree.focus()
        item_path = selectedItem

        if item_path == "..":
            self.currentfilepath = os.path.dirname(self.currentfilepath)
            self.loadCurrentFilepath()

        # If the item is a directory, navigate to it
        elif os.path.isdir(item_path):
            self.currentfilepath = item_path
            self.loadCurrentFilepath()
        else: self.window.open_file_in_specific_tab(item_path)
    
    def navigate(self) -> None:
        newpath = filedialog.askdirectory(title="Open Folder")
        if not newpath or not os.path.isdir(newpath):
            return
        self.currentfilepath = newpath
        self.loadCurrentFilepath()
    
    def new(self) -> None:
        dialogue = NewFileDialogue(self)
        if not dialogue.result: return
        match dialogue.result["type"]:
            case "text":
                with open(self.currentfilepath + "/" + dialogue.result.get("name") + ".txt", "w") as f: f.write("")
            case "lesson":
                with open(self.currentfilepath + f"/{dialogue.result.get('name')}.json", "w") as f:
                    data = {"title": "",
                    "metadata": {
                        "subtitle": "",
                        "date": "17/03/2025",
                        "subject": "",
                        "unit": "",
                        "term": "",
                        "week": ""},
                    "know": "",
                    "understand": "",
                    "demonstrate": "",
                    "notes": ""}
                    json.dump(data, f, indent=4)
            case _:
                with open(f"{self.currentfilepath}/{dialogue.result.get('name')}", "w") as f: f.write("")
        self.loadCurrentFilepath()

    def newFolder(self) -> None:
        dialogue = NewFolderDialogue(self)
        if not dialogue.result:
            return
        os.mkdir(self.currentfilepath + f"/{dialogue.result}")
        self.loadCurrentFilepath()
    
    def deleteItem(self) -> None:
        selected = self.fileTree.focus()
        item_path = selected
        if selected == "..": return
        if not item_path: return
        if os.path.isfile(item_path):
            confirmation = messagebox.askokcancel("Confirm", f"Will delete file '{item_path}'. Confirm?")
            if not confirmation: return
            os.remove(item_path)
        elif os.path.isdir(item_path):
            confirmation = messagebox.askokcancel("Confirm", f"Will delete folder '{item_path}' and all of it's contents. Confirm?")
            if not confirmation: return
            rmtree(item_path)
        self.loadCurrentFilepath()
