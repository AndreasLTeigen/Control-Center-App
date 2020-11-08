import kivy
kivy.require('1.0.6') # replace with your current kivy version !'

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

class SetClockScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(SetClockScreen, self).__init__(**kwargs)
        self.cols = 5
        hello1_button= Button(text='Hello 1', size_hint=(0.2,0.2), pos_hint={'x': 0.5, 'y': 0.5})
        self.add_widget(hello1_button)

class MyApp(App):

    def build(self):
        return SetClockScreen()


if __name__ == '__main__':
    MyApp().run()