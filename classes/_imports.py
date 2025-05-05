from classes.Utilities import TabFrame
from classes._ExampleTab import ExampleTab
from classes.Home import HomeScreen
from classes.Calculator import Calculator
from classes.TextEditor import TextEditor
from classes.UnitConverter import UnitConverter
from classes.ImageViewer import ImageViewer
from classes.CommandLine import CommandLine
from classes.LessonEditor import LessonEditor
from classes.SettingsDialogue import SettingsDialogue
from classes.RightTriangleCalculator import RightTriangleCalculator
from classes.FileExplorer import FileExplorer
from classes.LinuxTerminal import LinuxTerminal
from classes.CpsTester import CpsTester
from classes.PasswordGenerator import PasswordGenerator
from classes.ProjectileMotionCalculator import ProjectileMotionCalculator
from classes.ErrorLogViewer import ErrorLogViewer

TABS_LIST: list = [
    HomeScreen, Calculator, TextEditor,
    UnitConverter, ImageViewer, CommandLine, LessonEditor,
    RightTriangleCalculator, FileExplorer, LinuxTerminal,
    CpsTester, PasswordGenerator, ProjectileMotionCalculator,
    
    ErrorLogViewer
]