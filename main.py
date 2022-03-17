from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.properties import NumericProperty
from logic import Convert
import logic

from iamlaizy import reload_me
reload_me('calculator.kv')

# Setting size to resizable
Config.set('graphics', 'resizable', 1)

color_green = (0, 1, 0, 1)
color_write = (1, 1, 1, 1)
# Creating Layout class
class CalcGridLayout(GridLayout):

    # Function called when equals is pressed
    def calculate(self, calculation):
        if not calculation:
            return 
        
        try:
            # Solve formula and display it in entry
            # which is pointed at by display
            text = str(eval(calculation))
        except Exception:
            
            self.ids.deci.text = "Error"
            self.ids.bin.text = ''
            self.ids.oct.text = ''
            self.ids.hex.text = ''
            return

        self.ids.deci.text = text
        
        res = Convert(text)
        for base, type_conv in logic.ope.items():
            out = getattr(self.ids, type_conv.__name__)
            out.text = res.do(base)

    def select(self, base, order=[10, 2, 8, 16][::-1]):
        idx=order.index(base)
        for pos, btn in enumerate(self.children[-2].children):
            if pos==idx:
                btn.color=color_green
            else:
                btn.color=color_write

# Creating App class
class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

  
# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()