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
from threading import Thread

import csv
import os

thread_auto_running = False
tb_Scenarios = []

class thread_auto(Thread):
	'''
	This thread will execute un backgroud the automatic diagram and will update the MMI at the same time
	'''
	def __init__(self,app):
		Thread.__init__(self)		 #init the mother thread
		self.app=app
		self.pas = 0.1 #refresh time for the loading bars
	def run(self):
		'''
		loop of the thread 
		'''
		global thread_auto_running			   #receive the boolean that command the stop of the thread
		while(thread_auto_running):
			print(tb_Scenarios)
			
		Thread.__init__(self)
		# while(self.frame.actual_step < len(self.frame.list_diagram_buttons) and not stop_thread_auto):  #while were are not at the end of the sequence or the order to stop isn't given
			# if(not stop_thread_auto): 
				# if(self.frame.actual_step<=10):		  #from 0 to ten, diagram step are called only once
					# if (current_frame == "auto") : #don t update graphical components of frame automatic while not in this frame
						# self.frame.list_diagram_buttons[self.frame.actual_step-1].config(bg = 'grey')	  #reset the precedent step
				# self.fct_in_progress(self.frame.actual_step)	  #action of the step
				# time.sleep(0.5)	#used to slow the executio of the diagram
				# if(not stop_thread_auto):	 
					# if(self.frame.actual_step>=14 ):		  #make the last steps of the diagram loop
						# if (current_frame == "auto") : #don t update graphical components of frame automatic while not in this frame
							# self.frame.list_diagram_buttons[self.frame.actual_step-1].config(bg = 'grey')	  #reset them
							# self.frame.list_diagram_buttons[self.frame.actual_step-2].config(bg = 'grey')
							# self.frame.list_diagram_buttons[self.frame.actual_step-3].config(bg = 'grey')
						# self.frame.actual_step = 10	  #overwrite the actual step 
		

class AutomaticScreen(Screen):
	i = 0
	j = 0
	def __init__(self, app, **kwargs):
		super(AutomaticScreen, self).__init__(**kwargs)

		layout = FloatLayout()
		self.add_widget(layout)

		self.app = app
		self.Automatic_Thread=thread_auto(self.app)
		
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
		global thread_auto_running
		global tb_Scenarios
		txtBox_Setpoints = self.ids.txtIn_Automatic_SetPoint	 #get txtbox by ID
		txtBox_Measures = self.ids.txtIn_Automatic_Measures	 #get txtbox by ID
		
		if(self.ids.btn_Auto_START_STOP.text == "STOP"):
			self.ids.btn_Auto_LOAD.disabled = False
			self.ids.btn_Auto_START_STOP.text = "START"
			thread_auto_running = False
			self.Automatic_Thread.join()
		else:
			self.ids.btn_Auto_LOAD.disabled = True
			self.ids.btn_Auto_START_STOP.text = "STOP"
			thread_auto_running = True
			self.Automatic_Thread.start()
			
		for i in range(0,10):
			txtBox_Measures.text += "voltage : " + str(i)+"V  "+"Current : " +str(i)+"\n"
		
	def LoadSetUpFile(self,selection):
		global tb_Scenarios
		tb_Scenarios = []
		if(len(selection)):
			tb_Scenarios = []
			#self.ids.file_choosen_input.text = selection[0]
			SetUpFile = selection[0]
			#try to open the file. Do nothing if the file doesnt exist
			try:
					file = open(SetUpFile, 'r')
					file.close()
			except IOError:
				return
			INV_AUTO_TESTS_IDS = {v: k for k, v in AUTO_TESTS_IDS.items()}
			
			with open(SetUpFile, 'r', newline='') as file:
				reader = csv.reader(file, delimiter=';')
				for row in reader:
					print(row)
					#for(i in range(0, len(INV_AUTO_TESTS_IDS)):
					print(row[0])
					if(row[0] in AUTO_TESTS_IDS):
						tb_Scenarios.append(row)
		
		if(len(tb_Scenarios) > 0):
			self.ids.btn_Auto_START_STOP.disabled= False
		else:
			self.ids.btn_Auto_START_STOP.disabled= True
					
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
			
