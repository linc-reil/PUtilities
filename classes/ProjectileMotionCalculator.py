"""
Projectile Motion Calculator (tab)
A basic projectile motion calculator using kinematics equations.
"""

from classes.Utilities import *

class ProjectileMotionCalculator(TabFrame):
    _name = "Projectile Motion Calc"
    _description = "Calculate projectile motion using kinematics equations."
    _icon = "projectile calculator icon.png"

    def init(self) -> None:
        self.tabname = "Projectile Motion Calculator"
        self.description = """A basic projectile motion calculator using kinematics equations."""
        self.create_widgets()
    
    def create_widgets(self) -> None:
        self.use_radians = tk.BooleanVar(self, False) if CONFIGURATION.angle_unit == "Degrees" else tk.BooleanVar(self, True)
        self.header = ttk.Label(self, text="Projectile Motion Calculator", font=PConstants.arial_14)
        self.header.grid(row=0, column=0, columnspan=2, sticky="n", padx=5, pady=2)

        self.init_vel_label = ttk.Label(self, text="Initial Velocity:")
        self.init_vel_label.grid(row=1, column=0, sticky=tk.NW, padx=5, pady=2)
        self.init_vel_entry = ttk.Entry(self, width=35)
        self.init_vel_entry.grid(row=1, column=1, sticky=tk.NW, padx=5, pady=2)

        self.angle_label = ttk.Label(self, text="Angle from Horizontal:")
        self.angle_label.grid(row=2, column=0, sticky=tk.NW, padx=5, pady=2)
        self.angle_entry = ttk.Entry(self, width=35)
        self.angle_entry.grid(row=2, column=1, sticky=tk.NW, padx=5, pady=2)

        self.height_label = ttk.Label(self, text="Initial Height:")
        self.height_label.grid(row=3, column=0, sticky=tk.NW, padx=5, pady=2)
        self.height_entry = ttk.Entry(self, width=35)
        self.height_entry.grid(row=3, column=1, sticky=tk.NW, padx=5, pady=2)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=4, column=0, columnspan=2, sticky=tk.NW, padx=5, pady=2)
        self.calculate_button = ttk.Button(self.buttons_frame, text="Calculate!", command=self.calculate)
        self.calculate_button.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=2)
        self.clear_button = ttk.Button(self.buttons_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=2)

        self.result_box = ScrollableTextBox(self, width=50, state=tk.DISABLED)
        self.result_box.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=2)
        self.reset_result_box()
    
    def reset_result_box(self) -> None:
        self.result_box.text_widget.config(state=tk.NORMAL)
        self.result_box.clear()
        self.print_("### RESULTS ###")
    
    def print_(self, text: str, end: str = "\n") -> None:
        self.result_box.text_widget.config(state=tk.NORMAL)
        self.result_box.insert(tk.END, text + end)
        self.result_box.text_widget.config(state=tk.DISABLED)
    
    def print_ans(self, name: str, value: float) -> None:
        self.print_(f"{name} = {smartRound(value)}")
    
    def fix_angle(self, angle: float) -> float:
        if self.use_radians.get(): return angle
        return math.degrees(angle)

    def calculate(self) -> None:
        u = toFloat(self.init_vel_entry.get())
        theta = toFloat(self.angle_entry.get())
        if not self.use_radians.get(): theta = math.radians(theta)
        initialHeight = toFloat(self.height_entry.get())

        theta = math.degrees(theta) if not self.use_radians.get() else theta

        ux = u * math.cos(theta)
        uy = u * math.sin(theta)
        t = (2*uy) / 9.8 if not initialHeight else max(get_quadratic_solutions(-9.8/2, uy, initialHeight))
        sx = ux*t
        maxHeight = (uy**2) / 19.6 + initialHeight
        vImpactY = -uy + 9.8*t
        vImpact = f"{smartRound((ux**2 + vImpactY**2)**0.5)} E {smartRound(self.fix_angle(math.atan2(vImpactY, ux)))} S"
        s = f"{smartRound(sx**2 + initialHeight**2)} E {smartRound(self.fix_angle(math.atan2(initialHeight, sx)))} S"

        self.reset_result_box()
        self.print_ans("Initial velocity", f"{smartRound(u)} E {smartRound(theta)} S")
        self.print_ans("Initial x-velocity", smartRound(ux))
        self.print_ans("Initial y-velocity", smartRound(uy))
        self.print_ans("Time of flight", smartRound(t))
        self.print_ans("Maximum height", smartRound(maxHeight))
        self.print_ans("Horizontal range", smartRound(sx))
        self.print_ans("Y impact velocity", smartRound(vImpactY))
        self.print_ans("Impact velocity", smartRound(vImpact))
        self.print_ans("Total displacement", smartRound(s))
    
    def clear(self) -> None:
        self.reset_result_box()
        PTkUtils.clear_entry(self.init_vel_entry)
        PTkUtils.clear_entry(self.angle_entry)
        PTkUtils.clear_entry(self.height_entry)
    
    def createTabCommands(self):
        self.addTabCheckbox("Use Radians", self.use_radians)
    
