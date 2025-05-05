from classes.Utilities import *

class Calculator(TabFrame):
    _name = "Simple Calculator"
    _description = "A simple calculator with basic operations."
    _icon = "calculator icon.png"

    def init(self, master=None) -> None:
        self.tabname = "Simple Calculator"
        self.last_result = None  # Store the result of the last calculation
        
        self.entry = ttk.Entry(self, width=30, font=("Consolas", 20), state="normal")  # Change state to normal initially
        self.entry.grid(row=0, column=0, columnspan=5)
        self.entry.bind("<Return>", self.calculate)
        
        # Number and Operator Buttons
        self.button7 = ttk.Button(self, text="7", padding=(5, 20), command=lambda: self.add("7"))
        self.button7.grid(row=1, column=0)
        self.button8 = ttk.Button(self, text="8", padding=(5, 20), command=lambda: self.add("8"))
        self.button8.grid(row=1, column=1)
        self.button9 = ttk.Button(self, text="9", padding=(5, 20), command=lambda: self.add("9"))
        self.button9.grid(row=1, column=2)
        
        self.button4 = ttk.Button(self, text="4", padding=(5, 20), command=lambda: self.add("4"))
        self.button4.grid(row=2, column=0)
        self.button5 = ttk.Button(self, text="5", padding=(5, 20), command=lambda: self.add("5"))
        self.button5.grid(row=2, column=1)
        self.button6 = ttk.Button(self, text="6", padding=(5, 20), command=lambda: self.add("6"))
        self.button6.grid(row=2, column=2)
        
        self.button1 = ttk.Button(self, text="1", padding=(5, 20), command=lambda: self.add("1"))
        self.button1.grid(row=3, column=0)
        self.button2 = ttk.Button(self, text="2", padding=(5, 20), command=lambda: self.add("2"))
        self.button2.grid(row=3, column=1)
        self.button3 = ttk.Button(self, text="3", padding=(5, 20), command=lambda: self.add("3"))
        self.button3.grid(row=3, column=2)
        
        self.delButton = ttk.Button(self, text="DEL", padding=(5, 20), command=self.delete)
        self.delButton.grid(row=1, column=3)
        self.clrButton = ttk.Button(self, text="CLR", padding=(5, 20), command=self.clear)
        self.clrButton.grid(row=1, column=4)
        
        self.plusButton = ttk.Button(self, text="+", padding=(5, 20), command=lambda: self.add("+"))
        self.plusButton.grid(row=2, column=3)
        self.minusButton = ttk.Button(self, text="-", padding=(5, 20), command=lambda: self.add("-"))
        self.minusButton.grid(row=2, column=4)
        
        self.multiplyButton = ttk.Button(self, text="x", padding=(5, 20), command=lambda: self.add("x"))
        self.multiplyButton.grid(row=3, column=3)
        self.divideButton = ttk.Button(self, text="/", padding=(5, 20), command=lambda: self.add("/"))
        self.divideButton.grid(row=3, column=4)
        
        self.zeroButton = ttk.Button(self, text="0", padding=(5, 20), command=lambda: self.add("0"))
        self.zeroButton.grid(row=4, column=0)
        self.decimalPointButton = ttk.Button(self, text=".", padding=(5, 20), command=lambda: self.add("."))
        self.decimalPointButton.grid(row=4, column=1)
        
        self.exponentialButton = ttk.Button(self, text="x^[]", padding=(5, 20), command=lambda: self.add("^"))
        self.exponentialButton.grid(row=4, column=2)
        self.ansButton = ttk.Button(self, text="Ans", padding=(5, 20), command=lambda: self.add_last_result())
        self.ansButton.grid(row=4, column=3)
        self.equalsButton = ttk.Button(self, text="==", padding=(5, 20), command=self.calculate)
        self.equalsButton.grid(row=4, column=4)
    
    def createTabCommands(self):
        self.round = tk.BooleanVar(self, True)
        self.addTabCheckbox("Round to 3 Decimal Places", self.round)
        
    def clear(self) -> None:
        self.entry.delete(0, tk.END)
    
    def delete(self) -> None:
        text: str = self.entry.get()[:-1]
        self.clear()
        self.entry.insert(tk.END, text)
    
    def add(self, char: str) -> None:
        self.entry.insert(tk.END, char)
    
    def add_last_result(self) -> None:
        if self.last_result is not None:
            self.add(str(self.last_result))  # Add the last result to the current expression
    
    def calculate(self, event=None) -> None:
        expression = self.entry.get()
        expression = expression.replace('x', '*').replace('^', '**')
        
        try:
            result = round(eval(expression), 3) if self.round.get() else eval(expression)
            self.last_result = result  # Store the result of the calculation
            self.clear()
            self.entry.insert(tk.END, str(result))  # Display the result in the entry widget
        
        except Exception as e:
            self.clear()
            self.entry.insert(tk.END, "Error")  # Show error message for invalid expression