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
from kivy.properties import NumericProperty
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
from Gauge import Gauge
from dictionary import *

from kivy.uix.popup import Popup
import csv
import os
class ManualScreen(Screen):
	value = NumericProperty(0.0)
	def __init__(self, app,**kwargs):
		super(ManualScreen, self).__init__(**kwargs)
		layout = FloatLayout()#FloatLayout(orientation='vertical', padding=20, spacing=5)
		self.add_widget(layout)
		self.app = app
		
		
		
		with self.canvas.before:
			Color(0.9, 0.9, 0.9, 1) 
			self.rect = Rectangle(size=(75,50), pos=(800-75,0),rgb=(1,1,1),source='Datas/irisib.png')
		
		box_Gauges = GridLayout(rows=3,cols=2,col_default_width=150, col_force_default=True,row_default_height=150, row_force_default=True, pos = (10,-20))
		gaugesize = 150
		fontSize = 20
		self.gaugeU_Motor = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="U Motor",size_desc=15,maxvalue = 100.0)#unit : 100V max TODO: COMPLETE WITH CONFIG FILE
		self.gaugeI_Motor = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="I Motor",size_desc=15,maxvalue = 3.0)#unit : 3A max				TODO: COMPLETE WITH CONFIG FILE
		self.gaugeU_Brake = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="U Brake",size_desc=15,maxvalue = 100.0)#unit : 100V max	TODO: COMPLETE WITH CONFIG FILE
		self.gaugeI_brake = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="I Brake",size_desc=15,maxvalue = 2.0)#unit : 2A max				TODO: COMPLETE WITH CONFIG FILE
		self.gauge_Speed  = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="Speed",size_desc=15,maxvalue = 1400.0)#unit : 2A max		TODO: COMPLETE WITH CONFIG FILE
		self.gauge_Couple = Gauge(value=0, size_gauge=gaugesize, size_text=fontSize,text_desc="Couple",size_desc=15,maxvalue = 10.0)#unit : 2Nm max		TODO: COMPLETE WITH CONFIG FILE
		
		box_Gauges.add_widget(self.gaugeU_Motor)
		box_Gauges.add_widget(self.gaugeI_Motor)
		box_Gauges.add_widget(self.gaugeU_Brake)
		box_Gauges.add_widget(self.gaugeI_brake)
		box_Gauges.add_widget(self.gauge_Speed)
		box_Gauges.add_widget(self.gauge_Couple)
		
		settings_layout = GridLayout(rows=3,cols=2,
									 col_default_width=150, col_force_default=True,
									 row_default_height=30, row_force_default=True, 
									 pos = (400,-20),spacing = [5,10])

		'''
		self.btnSetSpeed =Button(text="Set Speed", on_release = self.btnSetting_Release)#"TC_Set_Speed")
		self.btnSetSpeed.id = "TC_Set_Speed"
		self.btnSetUmotor=Button(text="Set Umotor", on_release = self.btnSetting_Release)
		self.btnSetUmotor.id = "TC_Set_Umotor"
		self.btnSetCouple=Button(text="Set Couple", on_release = self.btnSetting_Release)
		self.btnSetCouple.id = "TC_Set_Couple"
		self.txtbxSetSpeed	= TextInput(text='0', input_filter='float')
		self.txtbxSetUmotor = TextInput(text='0', input_filter='float')
		self.txtbxSetCouple = TextInput(text='0', input_filter='float')
		
		
		settings_layout.add_widget(self.txtbxSetSpeed)
		settings_layout.add_widget(self.btnSetSpeed)
		settings_layout.add_widget(self.txtbxSetUmotor)
		settings_layout.add_widget(self.btnSetUmotor)
		settings_layout.add_widget(self.txtbxSetCouple)
		settings_layout.add_widget(self.btnSetCouple)

		'''

		layout.add_widget(settings_layout)
		layout.add_widget(box_Gauges)

	def btn_Set_Manual_Release(self, TC_Man):
		setting = Manual_TC_dict[TC_Man]

		if(Manual_TC_dict['Manual_TC_Set_Umotor'] == setting):
			print(self.ids.txtIn_Manual_U.text)
		if(Manual_TC_dict['Manual_TC_Set_Imotor'] == setting):
			print(self.ids.txtIn_Manual_I.text)
		if(Manual_TC_dict['Manual_TC_Set_Speed'] == setting):
			print(self.ids.txtIn_Manual_S.text)
		if(Manual_TC_dict['Manual_TC_Set_Couple'] == setting):
			print(self.ids.txtIn_Manual_C.text)
		


	def LoadFileToModify(self,selection):
		
		#self.ids.file_choosen_input.text = selection[0]
		MotorFile = selection[0]
		#try to open the file. Do nothing if the file doesnt exist
		try:
				file = open(MotorFile, 'r')
				file.close()
		except IOError:
			return
		with open(MotorFile, 'r', newline='') as file:
			reader = csv.reader(file, delimiter=';')
			for row in reader:
				if(row[0] == "Name"):
					self.ids.lbl_man_Name.text = "Name : "+row[1]
					#self.ids.Manual_S.text = row[1]
				if(row[0] == "Type"):
					self.ids.lbl_man_Type.text = "Type : "+row[1]
				if(row[0] == "UMotorMax"):
					self.ids.manual_max_U.text = "Max :\n"+row[1]+"V"
					self.ids.slider_man_U.max = float(row[1])
					self.gaugeU_Motor.maxvalue = float(row[1])
					
				if(row[0] == "IMotorMax"):
					self.ids.manual_max_I.text = "Max :\n"+row[1]+"A"
					self.ids.slider_man_I.max = float(row[1])
					self.gaugeI_Motor.maxvalue = float(row[1])
					
				if(row[0] == "PMotorMax"):
					pass#self.ids.Manual_P.text = row[1]
					
				if(row[0] == "SpeedMax"):
					self.ids.manual_max_S.text = "Max :\n"+row[1]+"t/m"
					self.ids.slider_man_S.max = float(row[1])
					self.gauge_Speed.maxvalue = float(row[1])
					
				self.ids.manual_max_C.text =  "Max :\n"+str(self.app.AbsoluteMaxRatings['C_COUPLE_MAX'])+" Nm"
				self.ids.slider_man_C.max = self.app.AbsoluteMaxRatings['C_COUPLE_MAX']

	def update(self, dt):
		i = self.app.labtooTestBench.TMTC_COM.testNumber
		if(i<255):
			# self.gaugeU_Motor.value = (i/3)
			# self.gaugeU_Brake.value = (i/2)
			# self.gauge_Speed.value = i*10
			# self.gaugeI_Motor.value = (i)/33
			# self.gaugeI_brake.value = (i/50)
			self.gauge_Couple.value = (i*0.039)#*2.08)
		else:
			self.i=0
			