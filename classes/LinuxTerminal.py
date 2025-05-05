import shutil
from classes.Utilities import *
import inspect
from textwrap import dedent

class _keywordArguments(typing.NamedTuple):
    tab: TabFrame
    current_working_directory: str

class _FunctionDescription(typing.NamedTuple):
    name: str
    obj: typing.Callable
    doc: str
    args: list[dict[str: str | type]]
    flags: list[str]
    type_of_function: typing.Literal["general", "bash", "utility"]
    description: str
    shortened_description: str

class _terminal_funcs:
    def __example_func(arg1: str, arg2: int, f: bool, p: bool, kwargs) -> str:
        """@type: utils # Possible 'bash', 'utility', 'general'
        This is an example function, with arguments and flags.

        Arguments:
            arg1 (str): The first argument.
            arg2 (int): The second argument.
        
        Flags:
            f: The first flag.
            p: The second flag.
        """

    def help(kwargs: _keywordArguments) -> str:
        """@type: general
        Print a general help message for using the PUtilities Linux Terminal Emulator.

        Arguments:
            (None)
        
        Flags:
            (None)
        """
        terminal = kwargs.tab
        terminal.print_("# PUtilities Linux Terminal Emulator Help")
        terminal.print_("PUtilities Linux Terminal Emulator incorporates many different functions found in traditional bash scripting, as well as custom functions designed to increase productivity from within PUtilities. These include:\n")
        general_funcs: list[_FunctionDescription] = []
        bash_funcs: list[_FunctionDescription] = []
        util_funcs: list[_FunctionDescription] = []
        for name, description in terminal.funcslist.items():
            if description.type_of_function == "general": general_funcs.append(description)
            elif description.type_of_function == "bash": bash_funcs.append(description)
            elif description.type_of_function == "utility": util_funcs.append(description)
        
        terminal.print_("## General Functions")
        for description in general_funcs:
            arguments = "" if not description.args else " " + " ".join(f"({item['name']}: {item['type']})" for item in description.args)
            terminal.print_(f"{description.name}{arguments}: {description.shortened_description}")
        terminal.print_("")

        terminal.print_("## Bash Functions")
        for description in bash_funcs:
            arguments = "" if not description.args else " " + " ".join(f"({item['name']}: {item['type']})" for item in description.args)
            terminal.print_(f"{description.name}{arguments}: {description.shortened_description}")
        terminal.print_("")

        terminal.print_("## Utility Functions")
        for description in util_funcs:
            arguments = "" if not description.args else " " + " ".join(f"({item['name']}: {item['type']})" for item in description.args)
            terminal.print_(f"{description.name}{arguments}: {description.shortened_description}")
        terminal.print_("")

    def man(name: str, kwargs: _keywordArguments) -> str:
        """@type: general
        Print out the details and description of a given function.

        Arguments:
            name (str): The name of the function to print the details on.
        
        Flags:
            (None)
        """
        terminal = kwargs.tab
        terminal.print_(f"# Information on Function '{name}'")
        description = None
        for item in terminal.funcslist.keys():
            if item == name:
                description: _FunctionDescription = terminal.funcslist[item]
        if not description: return f"Could not find function '{name}' in function list. Refer to help menu for a list of available functions."
        return description.description + "\n"

    def echo(text: str, u: bool = False, kwargs: _keywordArguments=None) -> str:
        """
        @type: bash
        Print back the inputted text to the terminal.

        Arguments:
            text (str): The text to print to the terminal.
        
        Flags:
            u: Print the text in uppercase.
        """
        if u: return text.upper()
        return text
    
    def cd(new_path: str, s: bool = False, kwargs: _keywordArguments = None) -> str:
        """@type: bash
        Change the current working directory.

        Arguments:
            new path (str): The new path to switch to, either as a subdirectory from the current working directory, or a completely seperate directory.
        
        Flags:
            s: Whether to strictly only use a completely new directory.
        """
        terminal, current_dir = kwargs.tab, kwargs.current_working_directory
        if new_path == "..":
            terminal.change_working_directory(os.path.dirname(current_dir))
        elif not s:
            if os.path.isdir(os.path.join(current_dir, new_path)):
                terminal.change_working_directory(os.path.join(current_dir, new_path))
            elif os.path.isdir(new_path):
                terminal.change_working_directory(new_path)
            else: return f"Directory '{new_path}' not found."
        elif os.path.isdir(new_path):
            terminal.change_working_directory(new_path)
        else: return f"Directory '{new_path}' not found."
    
    def pwd(kwargs: _keywordArguments = None) -> None:
        """@type: bash
        Print the current working directory.

        Arguments:
            (None)
        
        Flags:
            (None)
        """
        return kwargs.current_working_directory

    def ls(l: bool = False, a: bool = False, d: bool = False, f: bool = False, kwargs: _keywordArguments = None) -> str:
        """@type: bash
        List all files and directories within the current working directory.

        Arguments:
            (None)
        
        Flags:
            l: Print in list form instead of tab form.
            a: Print files and directories together in alphabetical order.
            d: Print directories only.
            f: Print files only.
        """
        directories, files = [], []
        all_items = os.listdir(kwargs.current_working_directory)
        for item in all_items:
            item_path = os.path.join(kwargs.current_working_directory, item)
            if os.path.isdir(item_path): directories.append(item)
            elif os.path.isfile(item_path): files.append(item)
        
        if a:
            return "    ".join(all_items) if not l else "\n".join(all_items)
        elif d:
            return "    ".join(directories) if not l else "\n".join(directories)
        elif f:
            return "    ".join(files) if not l else "\n".join(files)
        else:
            one = "    ".join(directories) if not l else "\n".join(directories)
            two = "    ".join(files) if not l else "\n".join(files)
            return one + "\n" + two
    
    def touch(filename: str, kwargs: _keywordArguments = None) -> None:
        """@type: bash
        Create a new file in the current working directory.

        Arguments:
            filename (str): The filename of the file to create.
        
        Flags:
            (None)
        """
        current_working_directory = kwargs.current_working_directory
        if PFileHandler.filepath_exists(os.path.join(current_working_directory, filename)):
            return f"File '{filename}' already exists."
        with open(os.path.join(current_working_directory, filename), "w") as f:
            f.write("")
    
    def rm(filename: str, kwargs: _keywordArguments = None) -> None:
        """@type: bash
        Delete a given file with its filename.

        Arguments:
            filename: The filename of the file to delete in the current working directory.
        
        Flags:
            (None)
        """
        if not PFileHandler.filepath_exists(os.path.join(kwargs.current_working_directory, filename)):
            return f"File '{filename}' not found."
        os.remove(os.path.join(kwargs.current_working_directory, filename))
    
    def rmdir(dirname: str, kwargs: _keywordArguments) -> None:
        """@type: bash
        Remove a directory from the current working directory.

        Arguments:
            dirname (str): The name of the directory to remove.
        
        Flags:
            (None)
        """
        if not os.path.exists(os.path.join(kwargs.current_working_directory, dirname)): return f"Could not find directory '{dirname}' to remove."
        shutil.rmtree(os.path.join(kwargs.current_working_directory, dirname))
    
    def mkdir(dirname: str, kwargs: _keywordArguments) -> None:
        """@type: bash
        Create a subdirectory in the current working directory.
        
        Arguments:
            dirname (str): The name of the directory to be created.
        
        Flags:
            (None)"""
        os.mkdir(os.path.join(kwargs.current_working_directory, dirname))
    
    def putils(filename: str, kwargs: _keywordArguments) -> None:
        """@type: utility
        Open a file with it's given PUtilities tab. Not recommended for large files.
        
        Arguments:
            filename (str): The filename in the current working directory to open.
        
        Flags:
            (None)"""
        if not PFileHandler.filepath_exists(os.path.join(kwargs.current_working_directory, filename)): return f"File '{filename}' not found to open."
        kwargs.tab.window.open_file_in_specific_tab(os.path.join(kwargs.current_working_directory, filename))
    
    def cat(filename: str, kwargs: _keywordArguments) -> None:
        """@type: bash
        Print out a file within the current working directory.
        
        Arguments:
            filename (str): The filename of the file to print out in the current working directory.
        
        Flags:
            (None)"""
        if not PFileHandler.filepath_exists(os.path.join(kwargs.current_working_directory, filename)):
            print(f"File '{filename}' not found.")
        with open(os.path.join(kwargs.current_working_directory, filename), "r") as f:
            kwargs.tab.print_(f.read())
    
    def clear(kwargs: _keywordArguments) -> None:
        """@type: utility
        Clear the terminal.
        
        Arguments:
            (None)
        
        Flags:
            (None)"""
        kwargs.tab.clearAll()

class LinuxTerminal(TabFrame):
    _name = "Linux Terminal"
    _description = "A linux terminal emulator with access to file commands."
    _icon = "linux terminal icon.png"

    def init(self):
        self.tabname = "Linux Terminal"
        self.previous_command = ""
        self.textbox = ScrollableTextBox(self, state=tk.DISABLED)
        self.textbox.pack(expand=1, fill="both")
        self.entry = ttk.Entry(self)
        self.entry.pack(expand=1, fill="x")
        self.entry.bind("<Return>", self.execute)
        self.entry.bind("<Up>", self.add_previous_command)
        self.filepath = PFileHandler.ROOT_FILEPATH
        self.print_(f"PUtilities Linux Terminal Emulator.\nType 'help' for more details.\n\n")
        self.print_entry_prompt()
        self.create_funcslist()
    
    def clearAll(self) -> None:
        self.textbox.text_widget.config(state="normal")
        self.textbox.clear()
        self.print_("PUtilities Linux Terminal Emulator.\nType 'help' for more details.\n\n")

    def add_previous_command(self, event=None) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.previous_command)
    
    def print_entry_prompt(self) -> None:
        self.print_(f"@PUtilities ~ $ ", end="")
    
    def change_working_directory(self, new_directory: str) -> None:
        self.filepath = new_directory
    
    def print_(self, text: str = "", end: str = "\n") -> None:
        self.textbox.text_widget.config(state=tk.NORMAL)
        self.textbox.insertAtEnd(text+end)
        self.textbox.scrollToBottom()
        self.textbox.text_widget.config(state=tk.DISABLED)
    
    def create_funcslist(self) -> None:
        method_names = [name for name, obj in vars(_terminal_funcs).items() if (inspect.isfunction(obj) or inspect.ismethod(obj)) and not name.startswith("__")]
        self.funcslist: dict[str: _FunctionDescription] = dict()
        for name in method_names:
            obj = getattr(_terminal_funcs, name)
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                doc = dedent(inspect.getdoc(obj).strip())
                signature = inspect.signature(obj)
                args = []
                flags = []
                for param in signature.parameters.values():
                    nameOfArg = param.name
                    if nameOfArg == "kwargs":
                        continue
                    elif len(nameOfArg) == 1:
                        flags.append(nameOfArg)
                        continue
                    argType = param.annotation if param.annotation is not inspect.Parameter.empty else str
                    args.append({"name": nameOfArg, "type": argType})
                self.funcslist[name] = _FunctionDescription(name, obj, doc, args, flags, doc.splitlines()[0][7:].strip().lower(), "\n".join(doc.splitlines()[1:]).strip(), doc.splitlines()[1].strip())

    def execute(self, event=None) -> None:
        raw_string = self.entry.get()
        self.previous_command = raw_string
        self.print_(raw_string)
        self.entry.delete(0, tk.END)
        
        split_string = raw_string.strip().split()
        if not split_string: self.print_entry_prompt(); return
        
        command = split_string[0].lower()
        split_string.pop(0)
        args, flags = [], []
        for text in split_string:
            if text.startswith("-"):
                flags += list(text[1:])
            else:
                args.append(text)
        flags = set(flags)
        function = None
        for func in self.funcslist.keys():
            if func == command:
                function: _FunctionDescription = self.funcslist[func]
        if not function:
            self.print_(f"Function '{command}' not found. Type 'help' for a list of commands."); return
        if len(args) < len(function.args):
            self.print_(f"Incorrect number of arguments passed into function '{command}'."); return
        while len(args) != len(function.args):
            args[-2] = f"{args[-2]} {args[-1]}"
            args.pop(-1)
        i = 0
        while i < len(args):
            target = function.args[i]["type"]
            if target == float:
                args[i] = toFloat(args[i])
            elif target == int:
                args[i] = toInt(args[i])
            elif target == bool:
                args[i] = False if args[i].lower() in ["no", "false", "0", "n", "not", "0.0"] else True
            i += 1
        args = tuple(args)
        new_flags = []
        for flag in function.flags:
            if flag in flags:
                new_flags.append(flags)
        kwargs = _keywordArguments(self, self.filepath)
        new_flags = tuple(new_flags)
        try:
            result = function.obj.__call__(*args, *new_flags, kwargs=kwargs)
        except Exception as e:
            self.print_(f"Error in running function '{command}'. Error type: {str(e)}. Please try again."); return

        if isinstance(result, (int, float, complex)):
            self.print_(f"Result = {smartRound(result)}")
        elif isinstance(result, dict):
            for item in result.keys():
                if isinstance(result[item], float):
                    result[item] = smartRound(result[item])
                self.print_(f"{item}: {result[item]}")
        elif result is None:
            self.print_(end="")
        else:
            self.print_(str(result))

        self.print_entry_prompt()
