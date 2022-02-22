from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from logic import Convert
import logic

# from iamlaizy import reload_me
# reload_me('calculator.kv')

# Setting size to resizable
Config.set('graphics', 'resizable', 1)
 
 
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
                self.ids.bin.text = ''
                self.ids.oct.text = ''
                self.ids.hex.text = ''
                return

            self.ids.deci.text = text
            
            res = Convert(text)
            for base, type_conv in logic.ope.items():
                out = getattr(self.ids, type_conv.__name__)
                out.text = res.do(base)


# Creating App class
class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

  
# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()