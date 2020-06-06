#:kivy 1.0.6

__all__ = ('TestBench',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'
import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.gesture import GestureDatabase
from kivy.uix.boxlayout import BoxLayout
from kivy.gesture import Gesture 
from kivy.uix.widget import Widget
import Gauge
from Automatic import AutomaticScreen
import Automatic
from Manuel import ManualScreen
from Settings import SettingsScreen
import random
from threading import Thread, RLock,Timer
from kivy.base import runTouchApp
from kivy.factory import Factory as F
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.lang import Builder
from dictionary import *
from LabtoolLayer import *
from kivy.config import Config
import configparser
import time
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '800')#'1024')
Config.set('graphics', 'height', '400')#'600')


filename = r"Config.txt"
ReadTM_Thread_ON = True
speed_reading_tm = 0.1

class ScreenManager(ScreenManager):
	pass

class TestBenchWindow(BoxLayout):
	pass

class HomeScreen(Screen):
	def __init__(self, app, **kwargs):
		super(HomeScreen, self).__init__(**kwargs)
		self.app = app
	def update(self, dt):
		pass



class TestBenchApp(App):
	tm = 1000
	title = 'TestBench ISIB'
	Table_Tm_Reg = []
	global ReadTM_Thread_ON
	def build(self):
		#self.root = Builder.load_file('TestBench.kv')
		
		
		self.labtooTestBench = LabtoolLayer(self)
		configParser = configparser.RawConfigParser()	
		configParser.read(filename)
		
		self.HomeScreen = HomeScreen(self,name='HomeScreen')
		self.AutomaticScreen = AutomaticScreen(self,name='AutomaticScreen')
		self.ManualScreen = ManualScreen(self,name='ManualScreen')
		self.SettingsScreen = SettingsScreen(self,name='SettingsScreen')
		
		self.AbsoluteMaxRatings = {
			'C_U_MOT_MAX'	: float(configParser.get('ABSOLUTEMAXRATINGS','UMotorMax')),
			'C_I_MOT_MAX'	: float(configParser.get('ABSOLUTEMAXRATINGS','IMotorMax')),
			'C_P_MOT_MAX' : float(configParser.get('ABSOLUTEMAXRATINGS','PMotorMax')),
			'C_SPEED_MOT_MAX'	  : float(configParser.get('ABSOLUTEMAXRATINGS','SpeedMax')),
			'C_U_BRAKE_MAX' : float(configParser.get('ABSOLUTEMAXRATINGS','UBrakeMax')),
			'C_I_BRAKE_MAX'		: float(configParser.get('ABSOLUTEMAXRATINGS','IBrakeMax')),
			'C_COUPLE_MAX'	   : float(configParser.get('ABSOLUTEMAXRATINGS','CoupleMax'))
		}
		
		Config.write()
		
		for k, v in TM_TABLE_ID.items():
			self.Table_Tm_Reg.append(0)
		
		
		sm = self.root.ids.sm
		
		sm.add_widget(self.HomeScreen)
		sm.add_widget(self.AutomaticScreen)
		sm.add_widget(self.ManualScreen)
		sm.add_widget(self.SettingsScreen)
		sm.transition = SlideTransition()
		Clock.schedule_interval(sm.current_screen.update, 1.0/60.0)
		#self.changeScreen(2)
		
	def changeScreen(self,idx_Screen):
		print(self.Table_Tm_Reg)
		sm = self.root.ids.sm
		self.labtooTestBench.SetUmot(0.0)
		Clock.unschedule(sm.current_screen.update)
		sm.current = Screens_dict[idx_Screen]
		Clock.schedule_once(self.StartUpdateCurrentScreen, SlideTransition().duration+0.1)
	def actionPrevious_Released(self):
		sm = self.root.ids.sm
		INV_SCREEN_DICT = {v: k for k, v in Screens_dict.items()}
		
		if(sm.current == Screens_dict[INV_SCREEN_DICT['AutomaticScreen']]):
			if(Automatic.thread_auto_running):
				self.AutomaticScreen.Start_Stop()
		self.changeScreen(0)
			#sm.current = 
			
	def StartUpdateCurrentScreen(self,dt):
		sm = self.root.ids.sm
		Clock.schedule_interval(sm.current_screen.update, 1.0/500.0)
		pass
	def quit(self):
		self.labtooTestBench.SetUmot(0.0)
		self.labtooTestBench.TMTC_COM.ReadBus_Threat_ON = False
		self.labtooTestBench.TMTC_COM.ReadThread.join()
		self.get_running_app().stop()

if __name__ == '__main__':
	TestBenchApp().run()
	
