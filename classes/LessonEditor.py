from classes.Utilities import *

class LessonEditor(TabFrame):
    _name = "Lesson Editor"
    _description = "Create and edit lessons, take notes, and more!"
    _icon = "lesson editor icon.png"

    def init(self):
        self.tabname = "Lesson Editor"
        self.filepath = None
        self.createWidgets()
    
    def createWidgets(self) -> None:
        self.titleLabel = ttk.Label(self, text="Title")
        self.titleLabel.pack(anchor="w")
        self.titleEntry = ttk.Entry(self, font=("Arial", 16), width=60)
        self.titleEntry.pack(padx=5, anchor="w")
        self.metadataLabel = ttk.Label(self, text="Lesson Info")
        self.metadataLabel.pack(anchor="w")
        self.metadataFrame = ttk.Frame(self)
        self.metadataFrame.pack(fill="x", padx=5)

        self.subtitleLabel = ttk.Label(self.metadataFrame, text="Subtitle")
        self.subtitleLabel.grid(row=0, column=0, padx=5, sticky="w")
        self.subtitleEntry = ttk.Entry(self.metadataFrame, width=40)
        self.subtitleEntry.grid(row=0, column=1, padx=5, sticky="ew")

        self.dateLabel = ttk.Label(self.metadataFrame, text="Date")
        self.dateLabel.grid(row=1, column=0, padx=5, sticky="w")
        self.dateEntry = ttk.Entry(self.metadataFrame, width=40)
        self.dateEntry.grid(row=1, column=1, padx=5, sticky="ew")

        self.subjectLabel = ttk.Label(self.metadataFrame, text="Subject")
        self.subjectLabel.grid(row=2, column=0, padx=5, sticky="w")
        self.subjectEntry = ttk.Entry(self.metadataFrame, width=40)
        self.subjectEntry.grid(row=2, column=1, padx=5, sticky="ew")

        self.unitLabel = ttk.Label(self.metadataFrame, text="Unit")
        self.unitLabel.grid(row=0, column=2, padx=5, sticky="w")
        self.unitEntry = ttk.Entry(self.metadataFrame, width=40)
        self.unitEntry.grid(row=0, column=3, padx=5, sticky="ew")

        self.termLabel = ttk.Label(self.metadataFrame, text="Term")
        self.termLabel.grid(row=1, column=2, padx=5, sticky="w")
        self.termEntry = ttk.Entry(self.metadataFrame, width=40)
        self.termEntry.grid(row=1, column=3, padx=5, sticky="ew")

        self.weekLabel = ttk.Label(self.metadataFrame, text="Week")
        self.weekLabel.grid(row=2, column=2, padx=5, sticky="w")
        self.weekEntry = ttk.Entry(self.metadataFrame, width=40)
        self.weekEntry.grid(row=2, column=3, padx=5, sticky="ew")

        self.kudsFrame = ttk.Frame(self)
        self.kudsFrame.pack(fill="x")
        self.knowLabel = ttk.Label(self.kudsFrame, text="Know")
        self.knowLabel.grid(row=0, column=0, sticky="w")
        self.knowEntry = ScrollableTextBox(self.kudsFrame, width=30, height=3)
        self.knowEntry.grid(row=1, column=0, sticky="ew")

        self.understandLabel = ttk.Label(self.kudsFrame, text="Understand")
        self.understandLabel.grid(row=0, column=1, sticky="w")
        self.understandEntry = ScrollableTextBox(self.kudsFrame, width=30, height=3)
        self.understandEntry.grid(row=1, column=1, sticky="ew")

        self.demonstrateLabel = ttk.Label(self.kudsFrame, text="Demonstrate")
        self.demonstrateLabel.grid(row=0, column=2, sticky="w")
        self.demonstrateEntry = ScrollableTextBox(self.kudsFrame, width=30, height=3)
        self.demonstrateEntry.grid(row=1, column=2, sticky="ew")

        self.notesLabel = ttk.Label(self, text="Main Notes")
        self.notesLabel.pack(anchor="w")
        self.notesEntry = ScrollableTextBox(self)
        self.notesEntry.pack(expand=1, fill="both")

        self.dateEntry.insert(tk.END, datetime.datetime.now().strftime("%d/%m/%Y"))
    
    def createTabCommands(self):
        self.addTabFunction("Clear text", self.clearData)
        self.addTabFunction("Fill out date", lambda: self.dateEntry.insert(tk.END, datetime.datetime.now().strftime("%d/%m/%Y")))
        self.addExportCommand("Export as Text Document", self.exportAsTextDocument)
        self.addExportCommand("Export to Clipboard", self.exportToClipboard)
    
    def getDict(self) -> None:
        return {
            "title": self.titleEntry.get().strip(),
            "metadata": {
                "subtitle": self.subtitleEntry.get().strip(),
                "date": self.dateEntry.get().strip(),
                "subject": self.subjectEntry.get().strip(),
                "unit": self.unitEntry.get().strip(),
                "term": self.termEntry.get().strip(),
                "week": self.weekEntry.get().strip()},
            "know": self.knowEntry.getAll().strip(),
            "understand": self.understandEntry.getAll().strip(),
            "demonstrate": self.demonstrateEntry.getAll().strip(),
            "notes": self.notesEntry.getAll().strip()}

    def save(self) -> None:
        if not self.filepath:
            self.saveAs()
            return
        with open(self.filepath, "w") as f:
            json.dump(self.getDict(), f, indent=4)
        CONFIGURATION.add_recent_file(self.filepath)
    
    def saveAs(self):
        if self.filepath:
            self.save()
        savepath = filedialog.asksaveasfilename(title="Save Lesson File", filetypes=[("Lesson File", "*.json")], defaultextension=".json")
        if not savepath or not os.path.exists(os.path.dirname(savepath)):
            return
        with open(savepath, "w") as f:
            json.dump(self.getDict(), f, indent=4)
        self.filepath = savepath
        self.tabname = get_filename_of_filepath(self.filepath)[:-5]
        CONFIGURATION.add_recent_file(self.filepath)
    
    def open(self):
        if self.filepath:
            self.save()
        loadpath = filedialog.askopenfilename(title="Load Lesson File", filetypes=[("Lesson File", "*.json")])
        if not loadpath or not os.path.exists(loadpath) or not loadpath.endswith(".json"):
            return
        with open(loadpath, "r") as f:
            data = json.load(f)
        self.parseData(data)
        self.filepath = loadpath
        self.tabname = get_filename_of_filepath(self.filepath)[:-5]
        CONFIGURATION.add_recent_file(self.filepath)
    
    def clearData(self) -> None:
        self.titleEntry.delete(0, tk.END)
        self.subjectEntry.delete(0, tk.END)
        self.dateEntry.delete(0, tk.END)
        self.subjectEntry.delete(0, tk.END)
        self.unitEntry.delete(0, tk.END)
        self.termEntry.delete(0, tk.END)
        self.weekEntry.delete(0, tk.END)

        self.knowEntry.clear()
        self.understandEntry.clear()
        self.demonstrateEntry.clear()
        self.notesEntry.clear()

    def parseData(self, data: dict) -> None:
        self.clearData()
        self.titleEntry.insert(tk.END, data.get("title", ""))
        self.subtitleEntry.insert(tk.END, data.get("metadata", dict()).get("subtitle", ""))
        self.dateEntry.insert(tk.END, data.get("metadata", dict()).get("date", ""))
        self.subjectEntry.insert(tk.END, data.get("metadata", dict()).get("subject", ""))
        self.unitEntry.insert(tk.END, data.get("metadata", dict()).get("unit", ""))
        self.termEntry.insert(tk.END, data.get("metadata", dict()).get("term", ""))
        self.weekEntry.insert(tk.END, data.get("metadata", dict()).get("week", ""))
        self.knowEntry.insertAtEnd(data.get("know", ""))
        self.understandEntry.insertAtEnd(data.get("understand"))
        self.demonstrateEntry.insertAtEnd(data.get("demonstrate"))
        self.notesEntry.insertAtEnd(data.get("notes"))
    
    def exportAsTextDocument(self) -> None:
        """Export the lesson as a .txt file."""
        data = self.getDict()
        savepath = filedialog.asksaveasfilename(title="Export Lesson as Text Document", filetypes=[("Text Document", "*.txt")], defaultextension=".txt")
        if not savepath or not os.path.exists(os.path.dirname(savepath)):
            return
        text = f"{data['title']}\n{data['metadata']['date']} - {data['metadata']['subtitle']}\n\nKUDs\nKnow: {data['know']}\nUnderstand: {data['understand']}\nDemonstrate: {data['demonstrate']}\n\n{data['notes']}"
        with open(savepath, "w") as f:
            f.write(text)
    
    def exportToClipboard(self) -> None:
        """Export the lesson as if it where to a .txt file, but instead copy to clipboard."""
        data = self.getDict()
        text = f"{data['title']}\n{data['metadata']['date']} - {data['metadata']['subtitle']}\n\nKUDs\nKnow: {data['know']}\nUnderstand: {data['understand']}\nDemonstrate: {data['demonstrate']}\n\n{data['notes']}"
        self.clipboard_append(text)
    
    def autoload(self, filepath):
        if self.filepath: self.save()
        if not filepath or not os.path.isfile(filepath): return
        with open(filepath, "r") as f:
            data = json.load(f)
        self.parseData(data)
        self.tabname = PFileHandler.get_filename_without_extension(filepath)
        self.filepath = filepath
        CONFIGURATION.add_recent_file(self.filepath)
        
