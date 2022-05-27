from kivy.base import ExceptionHandler, ExceptionManager
from kivy.config import Config
import sys
from kivy.utils import get_color_from_hex
from kivy.lang import Builder


FROZEN = getattr(sys, "frozen", False)
if not FROZEN:
    from traceback import format_exception
    from iamlaizy import reload_me

    hiden_dependencies =['kvs', 'custom']
    reload_me(*hiden_dependencies,  filter_extc=['.kv'])

from kivymd.app import MDApp
from script.conversion import CalcGridLayout


# Setting size to resizable
Config.set('graphics', 'resizable', 1)
excepthook=None

# Creating App class
class CalculatorApp(MDApp):
    color_scheme = {
        "background": get_color_from_hex('#282F37'),# 91% black
        "blue": '#263347',
        'green': '#03C03C',
        'white': [1, 1, 1, 1]
    }
    app_name = 'Dummy Calculator'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"

        # return CalcGridLayout()
        return Builder.load_file('kvs/app.kv')
        #TODO: make a load function
        # return Builder.load_file('kvs/app.kv')


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
