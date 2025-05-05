from classes.Utilities import *
import classes._unitconversions as convert

class UnitConverterTab(ttk.Frame):
    
    def __init__(self, master=None, unitType: str = "Length"):
        super().__init__(master)
              
        self.unitType = unitType
        self.unitConversions = {"not implemented": 1}
        self.conversionType = "table"
        self.unitOptions = []
        
        self.headerLabel = ttk.Label(self, text=f"Convert {self.unitType}", font=("Arial", 16))
        self.headerLabel.grid(row=0, column=0, columnspan=3)
        self.loadUnitConversions()
        
        self.fromLabel = ttk.Label(self, text="From:")
        self.fromLabel.grid(row=1, column=0, padx=5)
        self.fromEntry = ttk.Entry(self, width=40)
        self.fromEntry.grid(row=1, column=1, padx=5)
        self.fromDropDown = ttk.Combobox(self, values=self.unitOptions)
        self.fromDropDown.set(self.unitOptions[0])
        self.fromDropDown.grid(row=1, column=2, padx=5)
        
        self.toLabel = ttk.Label(self, text="To:")
        self.toLabel.grid(row=2, column=0, padx=5)
        self.toDropDown = ttk.Combobox(self, values=self.unitOptions)
        self.toDropDown.set(self.unitOptions[0])
        self.toDropDown.grid(row=2, column=1, padx=5, columnspan=2, sticky="w")
        
        self.resultLabel = ttk.Label(self, text="Result:")
        self.resultLabel.grid(row=3, column=0, padx=5)
        self.resultEntry = ttk.Entry(self, width=40)
        self.resultEntry.grid(row=3, column=1, columnspan=1, padx=5, sticky="w")
        
        self.convertButton = ttk.Button(self, text="Convert!", command=self.convert)
        self.convertButton.grid(row=3, column=2, columnspan=1, sticky="w")
    
    def loadUnitConversions(self) -> None:
        if self.unitType == "Length":
            self.unitConversions = convert.lengthConversions
            self.conversionType = "table" # possible table or lambda
        elif self.unitType == "Area":
            self.unitConversions = convert.areaConversions
            self.conversionType = "table"
        elif self.unitType == "Volume":
            self.unitConversions = convert.volumeConversions
            self.conversionType = "table"
        elif self.unitType == "Speed":
            self.unitConversions = convert.speedConversions
            self.conversionType = "table"
        elif self.unitType == "Time":
            self.unitConversions = convert.timeConversions
            self.conversionType = "table"
        elif self.unitType == "Energy":
            self.unitConversions = convert.energyConversions
            self.conversionType = "table"
        elif self.unitType == "Angle":
            self.unitConversions = convert.angleConversions
            self.conversionType = "lambda"
        elif self.unitType == "Information":
            self.unitConversions = convert.informationConversions
            self.conversionType = "table"
        elif self.unitType == "Temperature":
            self.unitConversions = convert.temperatureConversions
            self.conversionType = "lambda"
        elif self.unitType == "Power":
            self.unitConversions = convert.powerConversions
            self.conversionType = "table"
        elif self.unitType == "Force":
            self.unitConversions = convert.forceConversions
            self.conversionType = "table"
        elif self.unitType == "Frequency":
            self.unitConversions = convert.frequencyConversions
            self.conversionType = "table"
        elif self.unitType == "Torque":
            self.unitConversions = convert.torqueConversions
            self.conversionType = "table"

        self.unitOptions = list(self.unitConversions.keys())
    
    def convert(self) -> None:
        self.fromValue = float(self.fromEntry.get())
        self.result = None
        self.fromUnit = self.fromDropDown.get()
        self.toUnit = self.toDropDown.get()
        
        if self.conversionType == "table":
            self.baseUnitValue = self.fromValue / self.unitConversions[self.fromUnit]
            self.result = self.baseUnitValue * self.unitConversions[self.toUnit]
        else:
            self.baseUnitValue = self.unitConversions[self.fromUnit][0](self.fromValue)
            self.result = self.unitConversions[self.toUnit][1](self.baseUnitValue)
        
        self.resultEntry.delete(0, tk.END)
        self.result = f"{self.result:.3f}" if self.master.master.roundTo3dp.get() else self.result
        resultString = f"{self.result} {self.toUnit}" if bool(self.master.master.includeUnits.get()) else str(self.result)
        self.resultEntry.insert(0, resultString)

class UnitConverter(TabFrame):
    _name = "Unit Converter"
    _description = "Convert between units of speed, length, time, and more."
    _icon = "unit converter icon.png"

    def init(self):
        self.tabname = "Unit Converter"
        self.typesOfUnits = ttk.Notebook(self, width=700)
        self.typesOfUnits.pack(side="top", anchor="n", expand=1, fill="both")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Length"), text="Length")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Area"), text="Area")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Volume"), text="Volume")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Angle"), text="Angle")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Speed"), text="Speed")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Time"), text="Time")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Energy"), text="Energy")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Temperature"), text="Temperature")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Information"), text="Information")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Power"), text="Power")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Force"), text="Force")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Frequency"), text="Frequency")
        self.typesOfUnits.add(child=UnitConverterTab(self.typesOfUnits, "Torque"), text="Torque")
    
    def createTabCommands(self):
        self.roundTo3dp: tk.BooleanVar = tk.BooleanVar(self, value=True)
        self.addTabCheckbox(name="Round to 3.d.p", variable=self.roundTo3dp)
        self.includeUnits: tk.BooleanVar = tk.BooleanVar(self, value=False)
        self.addTabCheckbox(name="Include Units", variable=self.includeUnits)