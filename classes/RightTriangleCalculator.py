from classes.Utilities import *

class RightTriangleCalculator(TabFrame):
    _name = "Right Triangle Calculator"
    _description = "Calculate the angles and sides of a right triangle."
    _icon = "right triangle icon.png"

    def init(self):
        self.tabname = "Right Triangle Calculator"
        self.header = ttk.Label(self, text="Right Triangle Calculator", font=("Arial", 24))
        self.header.grid(row=0, column=0, columnspan=3, sticky="n")
        self.diagramImage = self.getPhotoimage("right-triangle-diagram-bordered.png")
        self.diagram = ttk.Label(self, image=self.diagramImage)
        self.diagram.grid(row=1, column=0, columnspan=2, pady=2, sticky="w")

        self.hypotenuseLabel = ttk.Label(self, text="Enter Hypotenuse:")
        self.hypotenuseLabel.grid(row=2, column=0, padx=5, pady=0, sticky="w")
        self.hypotenuseEntry = ttk.Entry(self, width=45)
        self.hypotenuseEntry.grid(row=2, column=1, padx=5, pady=0, sticky="w")

        self.oppositeLabel = ttk.Label(self, text="Enter Opposite:")
        self.oppositeLabel.grid(row=3, column=0, padx=5, pady=0, sticky="w")
        self.oppositeEntry = ttk.Entry(self, width=45)
        self.oppositeEntry.grid(row=3, column=1, padx=5, pady=0, sticky="w")

        self.adjacentLabel = ttk.Label(self, text="Enter Adjacent:")
        self.adjacentLabel.grid(row=4, column=0, padx=5, pady=0, sticky="w")
        self.adjacentEntry = ttk.Entry(self, width=45)
        self.adjacentEntry.grid(row=4, column=1, padx=5, pady=0, sticky="w")

        self.thetaLabel = ttk.Label(self, text="Enter Theta:")
        self.thetaLabel.grid(row=5, column=0, padx=5, pady=0, sticky="w")
        self.thetaEntry = ttk.Entry(self, width=45)
        self.thetaEntry.grid(row=5, column=1, padx=5, pady=0, sticky="w")

        self.phiLabel = ttk.Label(self, text="Enter Phi:")
        self.phiLabel.grid(row=6, column=0, padx=5, pady=0, sticky="w")
        self.phiEntry = ttk.Entry(self, width=45)
        self.phiEntry.grid(row=6, column=1, padx=5, pady=0, sticky="w")

        self.buttonsFrame = ttk.Frame(self)
        self.buttonsFrame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=2)

        self.clearButton = ttk.Button(self.buttonsFrame, text="Clear", command=self.clearEntries)
        self.clearButton.pack(side="left", anchor="w")
        self.calculateButton = ttk.Button(self.buttonsFrame, text="Calculate!", command=self.calculate)
        self.calculateButton.pack(side="left", anchor="w")

        self.resultbox = ScrollableTextBox(self, width=45)
        self.resultbox.grid(row=1, column=2, rowspan=7, padx=5, sticky="nsew", pady=5)
        self.resultbox.text_widget.config(state="disabled")
        self.prnt("# -- RESULT -- #")
        self.prnt("No result calculated.")
    
    def createTabCommands(self):
        self.addTabFunction("Clear all Entries", self.clearResultBox)
        self.addTabFunction("Calculate!", self.calculate)
        self.addExportCommand("Export as Text File", self.export)
    
    def clearResultBox(self) -> None:
        self.resultbox.text_widget.config(state="normal")
        self.resultbox.clear()
        self.resultbox.insertAtEnd("# -- RESULT -- #\n")
        self.resultbox.text_widget.config(state="disabled")
    
    def prnt(self, text: str, end: str = "\n") -> None:
        self.resultbox.text_widget.config(state="normal")
        self.resultbox.insertAtEnd(text + end)
        self.resultbox.text_widget.config(state="disabled")
    
    def clearEntries(self) -> None:
        self.hypotenuseEntry.delete(0, tk.END)
        self.oppositeEntry.delete(0, tk.END)
        self.adjacentEntry.delete(0, tk.END)
        self.thetaEntry.delete(0, tk.END)
        self.phiEntry.delete(0, tk.END)
        self.clearResultBox()
        self.prnt("No result calculated.")
    
    def calculate(self) -> None:
        hypotenuse = toFloat(self.hypotenuseEntry.get())
        opposite = toFloat(self.oppositeEntry.get())
        adjacent = toFloat(self.adjacentEntry.get())
        theta = toFloat(self.thetaEntry.get())
        phi = toFloat(self.phiEntry.get())
        if not hypotenuse and not opposite and not adjacent and not theta and not phi:
            self.clearResultBox()
            self.prnt("Not enough information to solve the triangle.")
            return
        triangle = right_triangle(hypotenuse, opposite, adjacent, theta, phi, False)
        triangle.solve_triangle()
        
        self.clearResultBox()
        for key, value in triangle.dictionary.items():
            if isinstance(value, float):
                value = smartRound(value)
            self.prnt(f"{key} = {value}")
    
    def export(self) -> None:
        savepath = filedialog.asksaveasfilename(title="Export Result as Text Document", defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if not savepath or not os.path.exists(os.path.dirname(savepath)):
            return
        hypotenuse = toFloat(self.hypotenuseEntry.get())
        opposite = toFloat(self.oppositeEntry.get())
        adjacent = toFloat(self.adjacentEntry.get())
        theta = toFloat(self.thetaEntry.get())
        phi = toFloat(self.phiEntry.get())
        if not hypotenuse and not opposite and not adjacent and not theta and not phi:
            return
        triangle = right_triangle(hypotenuse, opposite, adjacent, theta, phi, False)
        triangle.solve_triangle()
        result = "# -- Right Triangle Calculator -- #\n"
        for key, value in triangle.dictionary.items():
            result += f"{key} = {value}\n"
        with open(savepath, "w") as f:
            f.write(result)