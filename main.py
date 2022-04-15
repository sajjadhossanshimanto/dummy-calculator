from kivy.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from kivy.config import Config
from kivy.base import ExceptionHandler, ExceptionManager
from logic import FromDec, ToDec
from custom.itemlist import ItemConfirm
import logic
import re
import sys
from kivymd.uix.gridlayout import MDGridLayout
from kivy.utils import get_color_from_hex

FROZEN = getattr(sys, "frozen", False)
if not FROZEN:
    from traceback import format_exception
    from iamlaizy import reload_me

    hiden_dependencies =['calculator.kv', 'custom']
    reload_me(*hiden_dependencies)

from kivymd.app import MDApp



# Setting size to resizable
Config.set('graphics', 'resizable', 1)
excepthook=None

# Creating Layout class
class CalcGridLayout(MDGridLayout):
    from_base = 10
    dialog = None
    color_scheme = {
        "background": get_color_from_hex('#282F37'),# 91% black
        "blue": '#263347',
        'green': '#03C03C',
        'white': '#ffffff'
    }

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

    def item_selector(self, obj, *args):
        if not self.dialog:
            return
        
        self.from_base = obj._tag
        self.ids.entry.hint_text = obj.text

        self.dialog.dismiss()

    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Number system",
                type="confirmation",
                items=[
                    ItemConfirm(text="Decimal", _tag=10, select=self.item_selector),
                    ItemConfirm(text="Binary", _tag=2, select=self.item_selector),
                    ItemConfirm(text="Octal", _tag=8, select=self.item_selector),
                    ItemConfirm(text="Hexadecimal", _tag=16, select=self.item_selector),
                ]
            )
        self.dialog.open()


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
