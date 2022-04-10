from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.base import ExceptionHandler, ExceptionManager
from logic import FromDec, ToDec
import logic
import re
import sys

FROZEN = getattr(sys, "frozen", False)
if not FROZEN:
    from traceback import format_exception
    from iamlaizy import reload_me
    reload_me('calculator.kv')
from kivymd.app import MDApp



# Setting size to resizable
Config.set('graphics', 'resizable', 1)
excepthook=None

color_green = (0, 1, 0, 1)
color_write = (1, 1, 1, 1)
# Creating Layout class
class CalcGridLayout(GridLayout):
    from_base=10

    def __init__(self, *args, **kwargs):
        global excepthook
        excepthook=self.on_exception
        super().__init__(*args, **kwargs)

    def replace_with_dec(self, calcu:str):
        start = 0
        deci_calcu = ''
        numbers = re.finditer(r'\+|\-|\*|\\', calcu)
        for match in numbers:
            num: str = calcu[start: match.start()]

            num = ToDec(num).do(self.from_base)
            deci_calcu+=num
            deci_calcu+=match.group()

            start=match.start()+1
        # convert leftovers
        deci_calcu+=ToDec(calcu[start:len(calcu)]).do(self.from_base)
        
        return deci_calcu


    # Function called when equals is pressed
    def calculate(self, calculation:str):
        if not calculation:
            return
        if self.from_base!=10:
            calculation=self.replace_with_dec(calculation)
        
        # Solve formula and display it in entry
        # which is pointed at by display
        text = str(eval(calculation))
        self.ids.deci.text = ToDec.fold_nega(float(text))

        res = FromDec(text)
        for base, type_conv in logic.ope.items():
            out = getattr(self.ids, type_conv.__name__)
            out.text = res.do(base)

    def select(self, base, order=[10, 2, 8, 16][::-1]):
        idx=order.index(base)
        self.from_base = base

        for pos, btn in enumerate(self.children[-2].children):
            if pos==idx:
                btn.color=color_green
            else:
                btn.color=color_write

    def on_exception(self):
        # full_tb=format_exception(etype, value, tb)
        
        self.ids.deci.text = "Error"
        self.ids.bin.text = ''
        self.ids.oct.text = ''
        self.ids.hex.text = ''

# Creating App class
class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"
        return CalcGridLayout()


class E(ExceptionHandler):
    def handle_exception(self, inst):
        if not FROZEN:
            return ExceptionManager.RAISE
        
        excepthook()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())

# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()
