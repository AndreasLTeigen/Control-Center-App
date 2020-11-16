import subprocess
import kivy
kivy.require('1.0.6') # replace with your current kivy version !'

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore

class Alarm:
    def __init__(self, set_clock_screen, pos_hint_y, alarm_nr):
        self.set_clock_screen = set_clock_screen

        self.size_hint_y = 0.1
        self.pos_hint_y = pos_hint_y
        self.hour = 0
        self.minute = 0
        self.activated = False
        self.alarm_nr = alarm_nr

        self.time_label= Label(text=self.getPrintTime(self.hour)+':'+self.getPrintTime(self.minute), 
            font_size='30sp', size_hint=(0.2,self.size_hint_y), pos_hint={'x': 0.2, 'y': self.pos_hint_y})
        self.activation_toggle= ToggleButton(text='On', group='state', size_hint=(0.1,self.size_hint_y), 
            pos_hint={'x': 0.6, 'y': self.pos_hint_y})
        self.set_button= Button(text='Set', size_hint=(0.1,self.size_hint_y), pos_hint={'x': 0.7, 'y': self.pos_hint_y})
            
        self.set_clock_screen.add_widget(self.time_label)
        self.set_clock_screen.add_widget(self.activation_toggle)
        self.set_clock_screen.add_widget(self.set_button)

        self.set_button.bind(on_press = self.set)
        self.activation_toggle.bind(on_press = self.toggleEvent)

        self.load()


    def toggleEvent(self, event):
        # TODO: Add command "ctrl+c here"
        if self.activation_toggle.state == 'down':
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        print('Alarm Activated!')
    
    def deactivate(self):
        print('Alarm Deactivated')

    def set(self, event):
        self.hour = self.set_clock_screen.hour_counter
        self.minute = self.set_clock_screen.minute_counter
        self.time_label.text = self.getPrintTime(self.hour)+':'+self.getPrintTime(self.minute)
        self.set_clock_screen.store.put('alarm'+str(self.alarm_nr), hour=self.hour, minute=self.minute)

    def load(self):
        if self.set_clock_screen.store.exists('alarm'+str(self.alarm_nr)):
            self.hour = self.set_clock_screen.store.get('alarm'+str(self.alarm_nr))['hour']
            self.minute = self.set_clock_screen.store.get('alarm'+str(self.alarm_nr))['minute']
            self.time_label.text = self.getPrintTime(self.hour)+':'+self.getPrintTime(self.minute)
        else:
            print('Not here')
    
    def getPrintTime(self, value):
        if len(str(value)) == 1:
            value = str(0) + str(value)
        return str(value)


class SetClockScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(SetClockScreen, self).__init__(**kwargs)
        self.store = JsonStore('alarm_log.json')
        self.cols = 5
        self.alarm_list = []

        self.hour_counter = 0
        self.minute_counter = 0

        self.hour_increase_button= Button(text='UP', size_hint=(0.2,0.1), pos_hint={'x': 0.2, 'y': 0.75})
        self.hour_decrease_button= Button(text='DOWN', size_hint=(0.2,0.1), pos_hint={'x': 0.2, 'y': 0.55})
        self.minute_increase_button= Button(text='UP', size_hint=(0.2,0.1), pos_hint={'x': 0.6, 'y': 0.75})
        self.minute_decrease_button= Button(text='DOWN', size_hint=(0.2,0.1), pos_hint={'x': 0.6, 'y': 0.55})
        #self.add_alarm_button= Button(text='Add alarm', size_hint= (0.6,0.1), pos_hint={'x': 0.2, 'y': 0.43})
        self.hour_counter_label= Label(text=str(0)+str(self.hour_counter), font_size='40sp', size_hint=(0.2,0.1), pos_hint={'x': 0.2, 'y': 0.65})
        self.minute_counter_label= Label(text=str(0)+str(self.minute_counter), font_size='40sp', size_hint=(0.2,0.1), pos_hint={'x': 0.6, 'y': 0.65})
        self.divider_label= Label(text=':', font_size='40sp', size_hint=(0.2,0.1), pos_hint={'x': 0.4, 'y': 0.65})
        self.title_label= Label(text="Chromecast Alarm", font_size='30sp', size_hint=(0.6,0.1), pos_hint={'x': 0.2, 'y': 0.9})

        for i in range(4):
            self.addAlarm(i)

        self.add_widget(self.hour_increase_button)
        self.add_widget(self.hour_decrease_button)
        self.add_widget(self.minute_increase_button)
        self.add_widget(self.minute_decrease_button)
        #self.add_widget(self.add_alarm_button)
        self.add_widget(self.hour_counter_label)
        self.add_widget(self.minute_counter_label)
        self.add_widget(self.divider_label)
        self.add_widget(self.title_label)

        self.hour_increase_button.bind(on_press = self.increaseHourCounter)
        self.hour_decrease_button.bind(on_press = self.decreaseHourCounter)
        self.minute_increase_button.bind(on_press = self.increaseMinuteCounter)
        self.minute_decrease_button.bind(on_press = self.decreaseMinuteCounter)
        #self.add_alarm_button.bind(on_press = self.addAlarm)

    def addAlarm(self, i):
        pos_hint_y = 0.43 - len(self.alarm_list)*0.12
        new_alarm = Alarm(self, pos_hint_y, i)
        self.alarm_list.append(new_alarm)

    def changeHourCounter(self, change_value):
        self.hour_counter += change_value
        update_string = str(self.hour_counter)
        if len(update_string) == 1:
            update_string = str(0) + str(update_string)
        self.hour_counter_label.text =update_string
    
    def increaseHourCounter(self,event):
        increase_interval = 1
        if self.hour_counter + increase_interval >= 24:
            self.hour_counter = -increase_interval
        self.changeHourCounter(increase_interval)

    def decreaseHourCounter(self,event):
        decrease_interval = -1
        if self.hour_counter + decrease_interval < 0:
            self.hour_counter = 24
        self.changeHourCounter(decrease_interval)


    def changeMinuteCounter(self, change_value):
        self.minute_counter += change_value
        update_string = str(self.minute_counter)
        if len(update_string) == 1:
            update_string = str(0) + str(update_string)
        self.minute_counter_label.text =update_string
    
    def increaseMinuteCounter(self,event):
        increase_interval = 5
        if self.minute_counter + increase_interval >= 60:
            self.minute_counter = -increase_interval
        self.changeMinuteCounter(increase_interval)

    def decreaseMinuteCounter(self,event):
        decrease_interval = -5
        if self.minute_counter + decrease_interval < 0:
            self.minute_counter = 60
        self.changeMinuteCounter(decrease_interval)

class MyApp(App):

    def build(self):
        return SetClockScreen()

if __name__ == '__main__':
    MyApp().run()