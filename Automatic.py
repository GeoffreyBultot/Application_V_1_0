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
from dictionary import *

import csv
import os

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
	
	def Start_Stop(self):
		
		txtBox_Setpoints = self.ids.txtIn_Automatic_SetPoint
		txtBox_Measures = self.ids.txtIn_Automatic_Measures
		
		
		
		
		for i in range(0,10):
			txtBox_Measures.text += "voltage : " + str(i)+"V  "+"Current : " +str(i)+"\n"
		
	def LoadSetUpFile(self,selection):
		print(selection)
		#self.ids.file_choosen_input.text = selection[0]
		SetUpFile = selection[0]
		#try to open the file. Do nothing if the file doesnt exist
		try:
				file = open(SetUpFile, 'r')
				file.close()
		except IOError:
			return
		INV_AUTO_TESTS_IDS = {v: k for k, v in AUTO_TESTS_IDS.items()}
		print(INV_AUTO_TESTS_IDS)
		with open(SetUpFile, 'r', newline='') as file:
			reader = csv.reader(file, delimiter=';')
			for row in reader:
				#for(i in range(0, len(INV_AUTO_TESTS_IDS)):
				if(row[0] in AUTO_TESTS_IDS):
					
					print(AUTO_TESTS_IDS[row[0]])
					
		
		
	def update(self, dt):
		tab_TM = self.app.Table_Tm_Reg
		#print(tab_TM)
		raw_couple	= tab_TM[TM_TABLE_ID['TM_CR_MOT']]
		raw_U_Motor	= tab_TM[TM_TABLE_ID['TM_U_MOT']]
		raw_I_Motor	= tab_TM[TM_TABLE_ID['TM_I_MOT']]
		raw_Speed	= tab_TM[TM_TABLE_ID['TM_SP_MOT']]
		raw_U_Brake		= tab_TM[TM_TABLE_ID['TM_U_BRAKE']]
		raw_I_Brake		= tab_TM[TM_TABLE_ID['TM_I_BRAKE']]

		self.gaugeU_Motor.value		= (raw_U_Motor	*	TABLE_CONVERSION['TM_U_MOT'])#3.3/4095/0.0223)
		self.gaugeI_Motor.value		= (raw_I_Motor	*	TABLE_CONVERSION['TM_I_MOT'])
		self.gauge_Speed.value	= (raw_Speed		*	TABLE_CONVERSION['TM_SP_MOT'])
		self.gauge_Couple.value		= (raw_couple	*	TABLE_CONVERSION['TM_CR_MOT'])
		self.gaugeU_Brake.value		= (raw_U_Brake	*	TABLE_CONVERSION['TM_U_BRAKE'])
		self.gaugeI_brake.value		= (raw_I_Brake	*	TABLE_CONVERSION['TM_I_BRAKE'])
			
