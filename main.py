from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.config import Config
from logic import dec_to_bin
import logic

from iamlaizy import reload_me
reload_me('calculator.kv')

# Setting size to resizable
Config.set('graphics', 'resizable', 1)
## Config.set('graphics', 'width', '400')
## Config.set('graphics', 'height', '400')
 
 
# Creating Layout class
class CalcGridLayout(GridLayout):

    # Function called when equals is pressed
    def calculate(self, calculation):
        if calculation:
            try:
                # Solve formula and display it in entry
                # which is pointed at by display
                text = str(eval(calculation))
            except Exception:
                self.ids.deci.text = "Error"
                return

            self.ids.deci.text = text
            for base in logic.ope:
                logic.base = base
                res = dec_to_bin(text)
                out = getattr(self.ids, logic.ope[base].__name__)
                out.text = res


# Creating App class
class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

  
# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()