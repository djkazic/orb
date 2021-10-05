from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from io import StringIO
import sys

from data_manager import data_man


class StatusLine(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(StatusLine, self).__init__(*args, **kwargs)

        @mainthread
        def delayed():
            self.ids.line_input.bind(output=self.ids.line_output.setter("output"))

        delayed()


class StatusLineInput(TextInput):

    output = StringProperty("")

    def got_input(self, text):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            eval(text)
        except:
            print("Error")
        sys.stdout = old_stdout
        message = mystdout.getvalue()
        self.output = message.strip()


class StatusLineOutput(TextInput):
    output = StringProperty("")
