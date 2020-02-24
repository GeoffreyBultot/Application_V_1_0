#:kivy 1.0.6

__all__ = ('Automatic',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'
import time
import kivy

kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Canvas

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from Gauge import Gauge


class AutomaticScreen(Screen):
    i = 0
    j = 0
    def __init__(self, app, **kwargs):
        super(AutomaticScreen, self).__init__(**kwargs)

        layout = FloatLayout()
        self.add_widget(layout)

        self.app = app

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1) # green; colors range from 0-1 instead of 0-255
            #self.rect = Rectangle(size=(1024,600),source='Datas/background.jpg')
            self.rect2 = Rectangle(size=(75,50), pos=(800-75,0),rgb=(1,1,1),source='Datas/irisib.png')
        #layout.add_widget(Label(text=str('Hello')))
        #layout.add_widget(Button(text='Button!'))

        box_Gauges = GridLayout(rows=1,cols=6,col_default_width=130, col_force_default=True,row_default_height=150, row_force_default=True, pos = (10,-20))
        gaugesize = 125
        fontSize = 20

        self.gaugeU_Motor = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="U Motor",size_desc=15)
        self.gaugeI_Motor = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="I Motor",size_desc=15)
        self.gaugeU_Brake = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="U Brake",size_desc=15)
        self.gaugeI_brake = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="I Brake",size_desc=15)
        self.gauge_Speed  = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="Speed",size_desc=15)
        self.gauge_Couple = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="Couple",size_desc=15)
        
        box_Gauges.add_widget(self.gaugeU_Motor)
        box_Gauges.add_widget(self.gaugeI_Motor)
        box_Gauges.add_widget(self.gaugeU_Brake)
        box_Gauges.add_widget(self.gaugeI_brake)
        box_Gauges.add_widget(self.gauge_Speed)
        box_Gauges.add_widget(self.gauge_Couple)
        layout.add_widget(box_Gauges)


        print(self.width)




    def update(self, dt):
        i = self.app.labtooTestBench.TMTC_COM.testNumber
        if(self.i<100):
            self.gaugeU_Motor.value = (i/1.5)
            self.gaugeU_Brake.value = (i/2)
            self.gauge_Speed.value = i
            self.gaugeI_Motor.value = (100-i)/2
            self.gaugeI_brake.value = (100-1.5*i)
            self.gauge_Couple.value = (75-i)
        else:
            self.i=0
            
