#:kivy 1.0.6

__all__ = ('Gauge',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'

import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder

from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label

class Gauge(Widget):
    '''
    Gauge class

    '''
    maxvalue = NumericProperty(100)
    value = NumericProperty(0)
    size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
    size_text = NumericProperty(10)
    size_desc = NumericProperty(15)
    text_desc = StringProperty("")
    file_gauge = StringProperty("Datas/cadran.png")
    file_needle = StringProperty("Datas/needle.png")
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False, 
            do_scale=False,
            do_translation=False
            )

        _img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, 
            self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
            )

        _img_needle = Image(source=self.file_needle, size=(self.size_gauge, 
            self.size_gauge))

        self._glab = Label(font_size=self.size_text, markup=True,font_name="Datas/7_Segment.ttf",color=[1,0,0,1])
        self._glabdesc = Label(font_size=self.size_desc, markup=True,text=self.text_desc)

        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)
        
        self.add_widget(self._gauge)
        self.add_widget(self._needle)
        self.add_widget(self._glab)
        self.add_widget(self._glabdesc)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)
        
    def _update(self, *args):
        '''
        Update gauge and needle positions after sizing or positioning.

        '''
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._glab.center_x = self._gauge.center_x
        self._glab.center_y = self._gauge.center_y + (self.size_gauge/4)
        self._glabdesc.center_x = self._gauge.center_x
        self._glabdesc.center_y = self._gauge.center_y - (self.size_gauge/8)
        

    def _turn(self, *args):
        '''
        Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.
        '''
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = 90 - (self.value * 180.0/self.maxvalue) # (50 * self.unit) 
        self._glab.text = "[b]{0:.2f}[/b]".format(self.value)
        if(self.value < self.maxvalue/3):
            self._glab.color = [0,1,0,1]
        elif(self.value > self.maxvalue/3)&(self.value<2*self.maxvalue/3):
            self._glab.color = [1,.64,0,1]
        elif(self.value > 2*self.maxvalue/3):
            self._glab.color = [1,0,0,1]