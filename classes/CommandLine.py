from classes.Utilities import *
import inspect, http.client, json
from urllib.parse import urlparse

class funcs:
    """Use @hidden as a docstring for any functions not wanting to be displayed in the help menu."""
    def help(**kwargs) -> None:
        """Print help for PUtilities command line functions."""
        return
    
    def clear(**kwargs) -> None:
        """Clear the terminal."""
        return
    
    def exit(**kwargs) -> None:
        """Exit the PUtilities Command Line tab."""
        return
    
    def exitall(**kwargs) -> None:
        """Exit the entire program."""
        return

    def echo(text: str, **kwargs) -> str:
        """Print the input back to the terminal."""
        return text
    
    def calc(text: str, **kwargs) -> float:
        """Simple text-based calculator."""
        return toFloat(text)

    def solvepoints(x1: float, y1: float, x2: float, y2: float, **kwargs) -> dict:
        """Solve two coordinates."""
        rise, run = y2-y1, x2-x1
        gradient, distance = rise/run, (rise**2 + run**2)**0.5
        midpoint = f"({(x1+x2)/2}, {(y1+y2)/2})"
        yIntercept = y1 - x1*gradient
        xIntecept = -yIntercept/gradient
        equation = f"y = {gradient}x + {yIntercept}"
        return {"Rise": rise, "Run": run, "Gradient": gradient, "Distance between points": distance, "Midpoint": midpoint, "y-Intercept": yIntercept, "x-Intercept": xIntecept, "Equation of line": equation}

    def quadratic(a: float, b: float, c: float, **kwargs) -> dict:
        """Solve a quadratic equation of the form ax^2 + bx + c = 0."""
        midpoint = (-b) / (2*a)
        determinate = (b**2 - 4*a*c)**0.5 / (2*a)
        return {"Solution 1": midpoint + determinate, "Solution 2": midpoint - determinate, "Midpoint": midpoint, "Determinate": determinate}
    
    def rt(opposite: float, adjacent: float, hypotenuse: float, theta: float, phi: float, **kwargs) -> dict:
        """Solve a right-angled triangle. If value is not known, enter 0."""
        triangle = right_triangle(hypotenuse=hypotenuse, opposite=opposite, adjacent=adjacent, theta=theta, phi=phi, radians=False)
        triangle.solve_triangle()
        return triangle.dictionary

    def projectile(initialVelocity: float, initialAngleFromHorizontal: float, initialHeight: float, **kwargs) -> dict:
        """Calculate projectile motion using an initial velocity, initial angle from horizontal, and initial height."""
        ux = initialVelocity * math.cos(math.radians(initialAngleFromHorizontal))
        uy = initialVelocity * math.sin(math.radians(initialAngleFromHorizontal))
        time = (2*uy) / 9.8 if not initialHeight else max(get_quadratic_solutions(-9.8/2, uy, initialHeight))
        sx = ux*time
        maxHeight = (uy**2) / 19.6 + initialHeight
        vImpactY = uy - 9.8*time
        vImpact = f"{(ux**2 + vImpactY**2)**0.5} E {math.atan(vImpactY/ux)} S"
        s = f"{(sx**2 + initialHeight**2)} E {math.atan(initialHeight/sx)} S"
        return {"Initial x-velocity": ux, "Initial y-velocity": uy, "Time of flight": time, "Horizontal range": sx, "Maximum height": maxHeight, "Impact y-velocity": vImpactY, "Impact velocity": vImpact, "Total displacement": s}
    
    def cat(**kwargs) -> str:
        """Print out a selected file."""
        filepath = filedialog.askopenfilename(title="Open File", filetypes=[("Text File", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            return "Not file selected."
        with open(filepath, "r") as f:
            return f.read()
    
    def randint(minimum: int, maximum: int, **kwargs) -> int:
        """Generate a random integer."""
        return random.randint(minimum, maximum)
    
    def randreal(**kwargs) -> float:
        """Generate a random number between 0 and 1."""
        return random.random()
    
    def lcm(num1: int, num2: int, **kwargs) -> int:
        """Get the lowest common multiple of two integers."""
        return math.lcm(num1, num2)
    
    def gcd(num1: int, num2: int, **kwargs) -> int:
        """Get the greatest common divisor of two numbers."""
        return math.gcd(num1, num2)
    
    def sin(angle: float, **kwargs) -> float:
        """Get the sin of an angle."""
        return math.sin(math.radians(angle))
    
    def cos(angle: float, **kwargs) -> float:
        """Get the cos of an angle."""
        return math.cos(math.radians(angle))
    
    def tan(angle: float, **kwargs) -> float:
        """Get the tan of an angle."""
        return math.tan(math.radians(angle))
    
    def asin(ratio: float, **kwargs) -> float:
        """Get the asin of a ratio."""
        return math.degrees(math.asin(ratio))
    
    def acos(ratio: float, **kwargs) -> float:
        """Get the acos of a ratio."""
        return math.degrees(math.acos(ratio))
    
    def atan(ratio: float, **kwargs) -> float:
        """Get the atan of a ratio."""
        return math.degrees(math.atan(ratio))
    
    def degrees(angleInRadians: float, **kwargs) -> float:
        """Convert radians into degrees."""
        return math.degrees(angleInRadians)
    
    def radians(angleInDegrees: float, **kwargs) -> float:
        """Convert degrees into radians."""
        return math.radians(angleInDegrees)
    
    def triples(seed1: int, seed2: int, number: int, **kwargs) -> dict:
        """Generate pythagorean triples."""
        triples = dict()
        for i in range(number):
            a = seed1**2 - seed2**2
            b = 2 * seed1 * seed2
            c = seed1**2 + seed2**2
            triples[f"({i+1})"] = (abs(a), abs(b), abs(c))
            seed2 += 1
        return triples
    
    def currentperiod(**kwargs) -> str:
        """Print the current period."""
        hour = datetime.datetime.now().hour + datetime.datetime.now().minute / 60
        if hour < (8 + 55/60):
            return "Before school"
        elif hour < (10 + 5/60):
            return "Period 1"
        elif hour < (10 + 45/60):
            return "Recess 1"
        elif hour < (11 + 55/60):
            return "Period 2"
        elif hour < (13 + 5/60):
            return "Period 3"
        elif hour < (13 + 35/60):
            return "Recess 2"
        elif hour < (14 + 45/60):
            return "Period 4"
        else:
            return "After school"
    
    def password(length: int, includeNums: bool, includeBrackets: bool, includeSpecialChars: bool, **kwargs) -> None:
        """Generate a password."""
        chars = list("abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if includeNums:
            chars += list("1234567890")
        if includeBrackets:
            chars += list("()[]{}<>")
        if includeSpecialChars:
            chars += list("`~!@#$%^&*-_=+\\|;:'\",./?")
        result = ""
        for i in range(length):
            result += random.choice(chars)
        return result
    
    def dictionary(word: str, **kwargs) -> str:
        """@hidden"""
        result = ""
        word = input("Enter the word to look up: ")
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        # Parse the URL to get the host and path
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path

        try:
            # Create a connection to the host
            conn = http.client.HTTPSConnection(host)
            
            # Set up the headers
            headers = {'User-Agent': 'Mozilla/5.0'}

            # Make a GET request
            conn.request("GET", path, headers=headers)
            
            # Get the response
            response = conn.getresponse()
            
            if response.status == 200:
                # Parse the JSON data
                data = json.loads(response.read().decode())
                
                if isinstance(data, list) and len(data) > 0:
                    meanings = data[0].get("meanings", [])
                    if meanings:
                        result += "\nMeanings:\n"
                        for meaning in meanings:
                            part_of_speech = meaning.get("partOfSpeech", "N/A")
                            definitions = meaning.get("definitions", [])
                            result += f"\nPart of Speech: {part_of_speech}\n"
                            for definition in definitions:
                                result += f"Definition: {definition.get('definition', 'N/A')}\n"
                                result += f"Example: {definition.get('example', 'N/A')}\n"
                                result += f"Synonyms: {', '.join(definition.get('synonyms', []))}\n"
                                result += f"Antonyms: {', '.join(definition.get('antonyms', []))}\n"
                    else:
                        result = "No meanings found for the word."
                else:
                    result = "No data found for the word."
            else:
                result = f"Error: Received status code {response.status}"
            
            conn.close()
        
        except Exception as e:
            result = f"Error: {e}"
        
        return result

    def timetable(**kwargs) -> dict:
        """Print today's timetable."""
        timetable = CONFIGURATION.timetable
        if not timetable:
            return "Timetable not found."
        day = datetime.datetime.now().strftime("%A")
        if not day in timetable.keys():
            return "Day not found in timetable."
        result, i = dict(), 0
        while i < len(timetable[day]):
            result[f"Period {i+1}"] = timetable[day][i]
            i += 1
        return result

    def isprime(number: int, **kwargs) -> bool:
        """Check if an integer is prime."""
        if number < 2:
            return "Number must be greater than 1."
        for i in range(2, round(number**0.5) + 1):
            if number % i == 0:
                return False
        return True
    
    def divisors(number: int, **kwargs) -> str:
        """Get the divisors of an integer."""
        if number < 2:
            return "Number must be greater than 1."
        divisors = []
        for i in range(1, round(number/2) + 1):
            if number % i == 0:
                divisors.append(str(i))
        divisors.append(str(number))
        return ", ".join(divisors)
    
    def factorise(number: int, **kwargs):
        """Get the prime factorisation of a number."""
        if number <= 1:
            return "Number must be greater than 1"
        factors = []
        # Check for factors of 2
        count = 0
        while number % 2 == 0:
            number //= 2
            count += 1
        if count > 0:
            factors.append(f"2^{count}" if count > 1 else "2")
        
        # Check for odd factors from 3 upwards
        for i in range(3, int(number**0.5) + 1, 2):
            count = 0
            while number % i == 0:
                number //= i
                count += 1
            if count > 0:
                factors.append(f"{i}^{count}" if count > 1 else str(i))
        
        # If there's anything left, it must be a prime factor
        if number > 1:
            factors.append(str(number))
        
        # Join the factors with " x "
        return " x ".join(factors)
    
    def symbol(name: str, **kwargs) -> str:
        """Print a mathematics or other symbol to be copied. Includes lambda, proportional."""
        match name.lower().strip():
            case "lambda":
                return "∆"
            case "proportional":
                return "∝"
            case _:
                return "Could not find symbol."
    
    def kinetic(mass: float, velocity: float, **kwargs) -> float:
        """Get the kinetic energy of an object using the formula E_k = 1/2 m v^2."""
        return 0.5 * mass * velocity**2
    
    def potential(mass: float, height: float, **kwargs) -> float:
        """Get the potential energy of an object under earth's gravity. Uses Ep = mgh."""
        return mass * height * 9.81
    
    def lachem(equation: str, **kwargs) -> str:
        """Write chemical equation quickly to convert into the LaTeX format."""
        class Tokenizer:
            plus = "+"
            arrow = ">"

            def __init__(self, string: str) -> None:
                self.tokenize(string)

            def cleanup_string(self, string: str) -> None:
                result = ""
                for i in string:
                    if i in LOWERCASE + UPPERCASE + DIGITS + ["+", ">"]:
                        result += i
                return result

            def tokenize(self, string: str) -> None:
                string = self.cleanup_string(string)
                split = string.split(self.plus)
                temp, i = [], 0
                while i < len(split):
                    if i > 0: temp.append(self.plus)
                    temp.append(split[i])
                    i += 1
                self.tokens = []
                for i in temp:
                    if self.arrow in i:
                        split = i.split(self.arrow)
                        self.tokens.append(split[0])
                        self.tokens.append(self.arrow)
                        self.tokens.append(split[1])
                    else:
                        self.tokens.append(i)

            def latexify(self) -> None:
                result = ""
                for token in self.tokens:
                    if token == self.plus:
                        result += " + "
                    elif token == self.arrow:
                        result += " \\longrightarrow "
                    else:
                        t, i = list(token), 0
                        coefficient = ""
                        while t[0] in DIGITS:
                            coefficient += t[0]
                            t.pop(0)
                        result += coefficient
                        i = 0
                        while i < len(t):
                            if t[i] in UPPERCASE + LOWERCASE:
                                element = ""
                                while i < len(t) and t[i] in UPPERCASE + LOWERCASE:
                                    element += t[i]
                                    i += 1
                                result += "\\mathrm{" + element + "}"
                            else:
                                sub = ""
                                while i < len(t) and t[i] not in UPPERCASE + LOWERCASE:
                                    sub += t[i]
                                    i += 1
                                result += "_{" + sub + "}"
                return result
        return Tokenizer(equation).latexify()

class CommandLine(TabFrame):
    _name = "Command Line"
    _description = "A command line interface in PUtilities."
    _icon = "command line icon.png"

    def init(self):
        self.tabname = "PUtilities Command Line"
        self.textbox = ScrollableTextBox(self, state=tk.DISABLED)
        self.textbox.pack(fill="both", expand=1)
        self.inputFrame = ttk.Frame(self)
        self.inputFrame.pack(fill="x")
        self.label = ttk.Label(self.inputFrame, text=f"{CONFIGURATION.terminal_prompt} ")
        self.label.pack(side="left", anchor="w")
        self.entry = ttk.Entry(self.inputFrame, width=100)
        self.entry.pack(side="left", fill="x", expand=1)
        self.entry.bind("<Return>", self.execute)
        self.createFunclist()
        self.prompt = CONFIGURATION.terminal_prompt
        self.initTextbox()
    
    def initTextbox(self) -> None:
        self.textbox.text_widget.config(state=tk.NORMAL)
        self.textbox.clear()
        self.textbox.text_widget.config(state=tk.DISABLED)
        self.write("PUtilities Terminal")
        self.write("Type 'help' for more details.\n")
        self.write(f"{self.prompt} ", end="")

    def write(self, text: str = "", end: str = "\n") -> None:
        self.textbox.text_widget.config(state=tk.NORMAL)
        self.textbox.insertAtEnd(text+end)
        self.textbox.scrollToBottom()
        self.textbox.text_widget.config(state=tk.DISABLED)

    def printHelp(self) -> None:
        self.write("PUtilties Command Line is designed to quickly execute commands. These commands include:")
        for item in self.funcslist.keys():
            if self.funcslist[item]["doc"] == "@hidden": continue
            self.write(f">> {item} ", end="")
            for argument in self.funcslist[item]["args"]:
                self.write(f"({argument['name']}) ", end="")
            self.write(f": {self.funcslist[item]['doc']}")

    def execute(self, event=None) -> None:
        rightToPrint = True
        if self.entry.get():
            self.write(f"{self.entry.get()}")
        else:
            return
        string = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        command = string.split()[0]
        match command.lower():
            case "help":
                self.printHelp()
            case "clear":
                rightToPrint = False
                self.initTextbox()
            case "exit":
                self.close()
            case "exitall":
                self.quitProgram()
            case _:
                try:
                    self.checkAndRun(string)
                except Exception as e:
                    message = "There was an error in running the command. Error type: " + str(e)
                    self.write(message)
                    ERROR_LOG.log("[terminal]" + message)
        if rightToPrint:
            self.write()
            self.write(f"{self.prompt} ", end="")
    
    def createFunclist(self) -> None:
        self.funcslist = dict()

        # Use __dict__ to get methods in the correct order as defined in the class
        method_names = [name for name, obj in vars(funcs).items() 
                        if (inspect.isfunction(obj) or inspect.ismethod(obj)) and not name.startswith("__")]

        # Loop through the method names in the order they appear in the class
        for name in method_names:
            obj = getattr(funcs, name)
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                doc = obj.__doc__
                signature = inspect.signature(obj)
                args = []
                for param in signature.parameters.values():
                    nameOfArg = param.name
                    if nameOfArg == "kwargs":
                        continue
                    argType = param.annotation if param.annotation is not inspect.Parameter.empty else str
                    args.append({"name": nameOfArg, "type": argType})
                self.funcslist[name] = {"obj": obj, "doc": doc, "args": args}
    
    def checkAndRun(self, string: str) -> None:
        command = string.split()[0]
        function = None
        for func in self.funcslist.keys():
            if command.lower() == func:
                function = self.funcslist[func]
        if not function:
            self.write(f"Function '{command}' not found. Type 'help' for a list of functions.")
            ERROR_LOG.log(f"[terminal] Function '{command}' not found. Type 'help' for a list of functions.")
            return
        args = string.split()
        args.pop(0)       
        if len(args) < len(function["args"]):
            self.write(f"Incorrect number of arguments passed into function '{command}'. Refer to the help menu for a list of possible arguments for each function.")
            ERROR_LOG.log(f"[terminal] Incorrect number of arguments passed into function '{command}'. Refer to the help menu for a list of possible arguments for each function.")
            return
        while len(args) != len(function["args"]):
            args[-2] = f"{args[-2]} {args[-1]}"
            args.pop(-1)
        i = 0
        while i < len(args):
            target = function["args"][i]["type"]
            if target == float:
                args[i] = toFloat(args[i])
            elif target == int:
                args[i] = toInt(args[i])
            elif target == bool:
                args[i] = False if args[i].lower() in ["no", "false", "0", "n", "not", "0.0"] else True
            i += 1
        args = tuple(args)
        try:
            kwargs = {"tab": self}
            result = function["obj"].__call__(*args, **kwargs)
        except Exception as e:
            self.write(f"There was an error in function '{command}'. Error type: {str(e)}. Please try again.")
            ERROR_LOG.log(f"[terminal] There was an error in function '{command}'. Error type: {str(e)}. Please try again.")
            return
        
        if isinstance(result, (int, float, complex)):
            self.write(f"Result = {smartRound(result)}")
        elif isinstance(result, dict):
            for item in result.keys():
                if isinstance(result[item], float):
                    result[item] = smartRound(result[item])
                self.write(f"{item}: {result[item]}")
        elif result is None:
            self.write()
        else:
            self.write(str(result))
