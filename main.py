from kivy.base import ExceptionHandler, ExceptionManager
from kivy.config import Config
import sys
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.config import Config
from kivymd.uix.dialog import MDDialog 

try:
    import android
except ImportError:
    android = None


FROZEN = getattr(sys, "frozen", False) or android
if not FROZEN:
    from traceback import format_exception
    from iamlaizy import reload_me

    hiden_dependencies =['kvs', 'custom']
    reload_me(*hiden_dependencies,  filter_extc=['.kv'])

    H = 700
    W = H * (1080/1920)# 1920/1080 ratio
    Window.size = (W, H)


# Setting size to resizable
Config.set('graphics', 'resizable', 1)


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

        return Builder.load_file('kvs/app.kv')


class E(ExceptionHandler):
    def handle_exception(self, inst):
        if not FROZEN:
            return ExceptionManager.RAISE
        
        circle='\n'#\U00002B24'
        MDDialog(
            title=inst.__class__.__name__,
            text="Oops!" + circle + circle.join(inst.args),
            radius=[20, 7, 20, 7],
        ).open()

        return ExceptionManager.PASS

ExceptionManager.add_handler(E())

# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()
