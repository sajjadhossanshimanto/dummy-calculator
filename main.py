from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.properties import NumericProperty
from logic import FromDec, ToDec
import logic
import re


from iamlaizy import reload_me
reload_me('calculator.kv')

# Setting size to resizable
Config.set('graphics', 'resizable', 1)

color_green = (0, 1, 0, 1)
color_write = (1, 1, 1, 1)
# Creating Layout class
class CalcGridLayout(GridLayout):
    from_base=10

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
        calculation=self.replace_with_dec(calculation)
        
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

# Creating App class
class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

  
# creating object and running it 
calcApp = CalculatorApp()
calcApp.run()