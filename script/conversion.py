from kivymd.uix.dialog import MDDialog
from script.logic import FromDec, ToDec
from custom.itemlist import ItemConfirm
import script.logic as logic
import re
from kivymd.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file('kvs/main_screen.kv')



# Creating Layout class
class CalcGridLayout(GridLayout):
    from_base = 10
    dialog = None

    def replace_with_dec(self, calcu:str):
        start = 0
        deci_calcu = ''
        numbers = re.finditer(r'\+|\-|\*|\\', calcu)
        for match in numbers:
            num: str = calcu[start: match.start()]
            num = num or '0'

            num = ToDec(num).do(self.from_base)
            deci_calcu+=num# include number
            deci_calcu+=match.group()# include sign

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
        self.ids.deci.text = ToDec.fold_negative(float(text))

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
