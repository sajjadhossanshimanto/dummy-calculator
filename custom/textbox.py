from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)

from kivy.uix.textinput import TextInput
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDIcon
from kivymd.uix.textfield import TextfieldLabel



kv = """
#:import images_path kivymd.images_path


<TextBox>

    canvas.before:
        Clear

        # Active line for fill mode
        Color:
            rgba: self.border_line_color if root.mode == "fill" else (0, 0, 0, 0)
        Rectangle:
            size: self.width, dp(2)
            pos: self.center_x - (self.width / 2), self.y + (dp(16) if root.mode != "fill" else 0)

        # Texture of right Icon.
        Color:
            rgba: self.icon_right_color
        Rectangle:
            texture: self._lbl_icon_right.texture
            size: self._lbl_icon_right.texture_size if self.icon_right else (0, 0)
            pos:
                (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8), \
                (self.center[1] - self._lbl_icon_right.texture_size[1] / 2 + dp(8)) # if root.mode == "fill" else\
                # (self.center[1] - self._lbl_icon_right.texture_size[1] / 2 - dp(4))


        # Hint text.
        Color:
            rgba: self.current_hint_text_color or self.border_line_color
            
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x + dp(15), self.y + self.height - self._hint_y

        # "rectangle" mode
        Color:
            rgba:
                self.border_line_color
        Line:
            width: dp(1) if root.mode == "rectangle" else dp(0.00001)
            points:
                (
                self.x + self._hint_lbl.width + dp(15), self.top - self._hint_lbl.texture_size[1] // 2,
                self.right - dp(5), self.top - self._hint_lbl.texture_size[1] // 2,
                self.right - dp(5), self.y + dp(5),
                self.x + dp(5), self.y + dp(5),
                self.x + dp(5), self.top - self._hint_lbl.texture_size[1] // 2,
                self.x + self._hint_lbl.x + dp(15), self.top - self._hint_lbl.texture_size[1] // 2
                # _line_blank_space_left_point
                )

        Color:
            rgba: self.text_color or root.foreground_color

    # "fill" mode.
    canvas.after:
        Color:
            rgba: root.fill_color if root.mode == "fill" else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height
            radius: root.radius

    font_name: "Roboto"
    bold: False
    padding: 
        # peading for the text
        # left, top, right, buttom
        
        "10dp", \
        "16dp" if root.mode != "fill" else "24dp", \
        "10dp" if root.mode != "fill" and not root.icon_right else ("14dp" if not root.icon_right else self._lbl_icon_right.texture_size[1] + dp(20)), \
        "16dp" if root.mode == "fill" else "10dp"

"""

Builder.load_string(kv)


class TextBox(ThemableBehavior, TextInput):

    mode = OptionProperty("rectangle", options=["rectangle", "fill"])
    """
    Text field mode. Available options are: `'rectangle'`, `'fill'`.
    """


    fill_color = ColorProperty([0, 0, 0, 0])
    """
    The background color of the fill in rgba format when the ``mode`` parameter
    is "fill".
    """


    current_hint_text_color = ColorProperty(None)
    """
    ``hint_text`` text color.
    """

    icon_right = StringProperty()

    icon_right_color = ColorProperty((0, 0, 0, 1))
    """
    Color of right icon in ``rgba`` format.
    """

    press_right_icon = ObjectProperty()

    text_color = ColorProperty(None)
    """
    Text color in ``rgba`` format.
    """

    font_size = NumericProperty("16sp")
    """
    Font size of the text in pixels.
    """

    radius = ListProperty([10, 10, 0, 0])
    """
    The corner radius for a text field in `fill` mode.
    """

    _hint_y = NumericProperty("17dp")
    border_line_color = ColorProperty((0, 0, 0, 0))
    
    
    fill_color = ColorProperty((0, 0, 0, 0))
    _hint_lbl = None
    _lbl_icon_right = None

    def __init__(self, **kwargs):
        self.set_objects_labels()
        super().__init__(**kwargs)
        self.border_line_color = self.theme_cls.primary_color

    def set_objects_labels(self):
        """Creates labels objects for the parameters
        `right_icon`,`hint_text`, etc."""


        # Label object for `hint_text` parameter.
        self._hint_lbl = TextfieldLabel(
            font_style="Subtitle1",
            halign="left",
            valign="middle",
            field=self
        )
        # MDIcon object for the icon on the right.
        self._lbl_icon_right = MDIcon(theme_text_color="Custom")

    def on_icon_right(self, instance, value):
        self._lbl_icon_right.icon = value

    def on_icon_right_color(self, instance, value):
        self._lbl_icon_right.text_color = value

    def on_hint_text(self, instance, value):
        self._hint_lbl.text = value

    def on_touch_down(self, touch):
        if self.icon_right and self.press_right_icon and self.collide_point(*touch.pos):
            # icon position based on the KV code for MDTextField
            icon_x = (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8)
            icon_y = self.center[1] - self._lbl_icon_right.texture_size[1] / 2 + dp(8)

            # not a complete bounding box test, but should be sufficient
            if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                self.press_right_icon()

        return super().on_touch_down(touch)

    def _refresh_hint_text(self):
        pass# prevent hint text
