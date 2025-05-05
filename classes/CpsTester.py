"""
CPS Tester (tab)
A CPS (clicks per second) tester tab. Includes:
- 3, 5, 10 second tests
- Personal best score
"""

from classes.Utilities import *

class CpsTester(TabFrame):
    _name = "CPS Tester"
    _description = "A CPS tester game / utility. Try to beat your personal best!"
    _icon = "cps tester icon.png"

    def init(self) -> None:
        self.tabname = "CPS Tester"
        self.description = """A CPS (clicks per second) tester tab. Includes:
- 3, 5, 10 second tests
- Personal best score"""
        self.create_widgets()

    def create_widgets(self) -> None:
        self.cps = 0
        self.can_click = True
        self.test_clicks = 0
        self.in_test = False

        self.clicker = tk.Button(self, text="Click to Start!", width=20, height=5, font=("Arial", 20), command=self.tester_clicked, bg=PConstants.orange, background=PConstants.orange)
        self.clicker.pack(side="top", anchor="center", padx=20, pady=30)

        self.test_options = ["1 Second", "2 Second", "3 Second", "5 Second", "10 Second", "20 Second", "30 Second", "60 Second"]
        self.test_type = tk.StringVar(self, "5 Second")
        self.test_options_selector = ttk.Combobox(self, textvariable=self.test_type, values=self.test_options, width=12)
        self.test_options_selector.pack(side="left", anchor="n")
        
        self.highscore_label = ttk.Label(self, text=f"Highscore: {CONFIGURATION.cps_highscore}")
        self.highscore_label.pack(side="left", anchor="n")

    def tester_clicked(self) -> None:
        if not self.can_click: return
        if self.in_test:
            self.test_clicks += 1
            self.clicker.config(text=f"{self.test_clicks}")
        else:
            self.in_test = True
            self.test_clicks = 0
            self.clicker.config(text="0")
            test_seconds = self.get_test_time()
            self.after(test_seconds * 1000, self.end_test)
    
    def get_test_time(self) -> int:
        match self.test_type.get():
            case "1 Second": return 1
            case "2 Second": return 2
            case "3 Second": return 3
            case "5 Second": return 5
            case "10 Second": return 10
            case "20 Second": return 20
            case "30 Second": return 30
            case "60 Second": return 60
            case _: return 5

    def end_test(self) -> None:
        test_seconds = self.get_test_time()
        self.cps = self.test_clicks / test_seconds
        self.cps = round(self.cps, 3)
        self.in_test = False
        self.test_clicks = 0
        if self.cps > CONFIGURATION.cps_highscore:
            CONFIGURATION.cps_highscore = self.cps
            self.highscore_label.config(text=f"Highscore: {CONFIGURATION.cps_highscore}")
        self.clicker.config(text=f"{self.cps} cps")
        self.can_click = False
        self.after(2000, self.scc)
    
    def scc(self) -> None:
        self.can_click = True
        self.clicker.config(text="Click to Start!")
    
    def createTabCommands(self):
        self.addTabFunction("Reset High Score", self.reset_highscore)
    
    def reset_highscore(self) -> None:
        if messagebox.askyesno("Confirm", "Reset CPS test high score?"):
            CONFIGURATION.cps_highscore = 0
            self.highscore_label.config(text=f"Highscore: {CONFIGURATION.cps_highscore}")