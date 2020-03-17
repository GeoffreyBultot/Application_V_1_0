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
num_of_scenarios = len(tb_Scenarios)
idx_current_scenario = 0
current_scenario = []
textFor_txtBox_Measures = ""
textFor_txtBox_SetPoints = ""
textFor_lbl_SetPoints = "Test : No test in progress"

class thread_auto(Thread):
	'''
	This thread will execute un backgroud the automatic diagram and will update the MMI at the same time
	'''
	
		
	def __init__(self,screen):
		Thread.__init__(self)		 #init the mother thread
		self.screen=screen
		self.pas = 0.1 #refresh time for the loading bars
		
		num_of_scenarios = len(tb_Scenarios)
		idx_current_scenario = 0
		current_scenario = []
		
	def run(self):
		'''
		loop of the thread 
		'''
		global thread_auto_running			   #receive the boolean that command the stop of the thread
		global num_of_scenarios
		global idx_current_scenario
		global current_scenario
		
		num_of_scenarios = len(tb_Scenarios)
		idx_current_scenario = 0
		current_scenario = []
		
		while( (idx_current_scenario < num_of_scenarios) & (thread_auto_running) ):
			current_scenario = tb_Scenarios[idx_current_scenario]
			if(current_scenario[0] in AUTO_TESTS_IDS):
				scenario = current_scenario[0]
				P1 = float(current_scenario[1])
				P2 = float(current_scenario[2])
				print(current_scenario[3])
				CST = float(current_scenario[3])
				self.exectute_scenario(scenario,P1,P2,CST)
			idx_current_scenario += 1
			
	def exectute_scenario(self,scenario,P1,P2,CST):
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		global textFor_lbl_SetPoints
		
		textFor_lbl_SetPoints = "Test : "
		if(scenario == 'U_MIN_TO_U_MAX'):
			textFor_lbl_SetPoints += "Umin to Umax"
			self.scenario_U_MIN_TO_U_MAX(P1,P2,CST)
			
		elif(scenario == 'C_FCT_SP_U_CST'):
			textFor_lbl_SetPoints += "Couple = fct(speed) @ Umot = "+(str(round(CST,2)))+"V"
			self.scenario_C_FCT_SP_U_CST(P1,P2,CST)
				
		elif(scenario == 'U_FCT_SP_C_CST'):
			textFor_lbl_SetPoints += "Umot = fct(speed) @ Couple = "+(str(round(CST,2)))+"Nm"
			self.scenario_U_FCT_SP_C_CST(P1,P2,CST)
			
		elif(scenario == 'SP_FCT_U_C_CST'):
			textFor_lbl_SetPoints += "Speed = fct(Umot) @ Couple = "+(str(round(CST,2)))+"Nm"
			self.scenario_SP_FCT_U_C_CST(P1,P2,CST)
			
	
	def scenario_U_MIN_TO_U_MAX(self,P1,P2,CST):
		
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		interval = (P2-P1)/10
		interval = round(interval,2)
		currentU = round(P1,2)
		while( (currentU < (P2+interval) ) & (thread_auto_running) ):
			textFor_txtBox_SetPoints += "Umot set : "+str(currentU)+" V \n"
			self.screen.app.labtooTestBench.SetUmot(currentU)
			
			U =	round(self.screen.gaugeU_Motor.value,2)
			V =	round(self.screen.gauge_Speed.value,2) 
			I =	round(self.screen.gaugeI_Motor.value,2)
			textFor_txtBox_Measures += "U = "	+ str(U)	+ "V  "
			textFor_txtBox_Measures += "v = "	+ str(V)	+ "tr/min  "
			textFor_txtBox_Measures += "I = "	+ str(I) 	+ "A \n"
			
			currentU += interval
			currentU = round(currentU,2)
			time.sleep(0.5)
			
	def scenario_C_FCT_SP_U_CST(self,P1,P2,CST):
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		interval = (P2-P1)/10
		interval = round(interval,2)
		currentCR = round(P1,2)
		
		while( (currentCR < (P2+interval) ) & (thread_auto_running) ):
			textFor_txtBox_SetPoints += "Couple set : "+str(currentCR)+" Nm\n"
			
			self.screen.app.labtooTestBench.SetCrMot(currentCR)
			self.screen.app.labtooTestBench.SetUmot(CST)
			
			C =	round(self.screen.gauge_Couple.value,2)
			V =	round(self.screen.gauge_Speed.value,2) 
			I =	round(self.screen.gaugeI_Motor.value,2)
			U =	round(self.screen.gaugeU_Motor.value,2)
			textFor_txtBox_Measures += "Cr = "	+ str(C)	+ "Nm  "
			textFor_txtBox_Measures += "v = "	+ str(V)	+ "tr/min  "
			textFor_txtBox_Measures += "I = "	+ str(I) 	+ "A \n"
			textFor_txtBox_Measures += "U = "	+ str(I) 	+ "V \n"
			
			currentCR += interval
			currentCR = round(currentCR,2)
			time.sleep(0.5)
		
	def scenario_U_FCT_SP_C_CST(self,P1,P2,CST):
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		interval = (P2-P1)/10
		interval = round(interval,2)
		currentSP = round(P1,2)
		while( (currentSP < (P2+interval) ) & (thread_auto_running) ):
			textFor_txtBox_SetPoints += "Speed set : "+str(currentSP)+"tr/min \n"
			
			self.screen.app.labtooTestBench.SetSpeedMot(currentSP)
			self.screen.app.labtooTestBench.SetCrMot(CST)
			
			U =	round(self.screen.gaugeU_Motor.value,2)
			V =	round(self.screen.gauge_Speed.value,2) 
			I =	round(self.screen.gaugeI_Motor.value,2)
			textFor_txtBox_Measures += "U = "	+ str(U)	+ "V  "
			textFor_txtBox_Measures += "v = "	+ str(V)	+ "tr/min  "
			textFor_txtBox_Measures += "I = "	+ str(I) 	+ "A \n"
			
			currentSP += interval
			currentSP = round(currentSP,2)
			time.sleep(0.5)
				
	def scenario_SP_FCT_U_C_CST(self,P1,P2,CST):
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		interval = (P2-P1)/10
		interval = round(interval,2)
		currentU = round(P1,2)
		while( (currentU < (P2+interval) ) & (thread_auto_running) ):
			textFor_txtBox_SetPoints += "Voltage set : "+str(currentU)+" V\n"
			
			
			self.screen.app.labtooTestBench.SetUmot(currentU)
			self.screen.app.labtooTestBench.SetCrMot(CST)
			
			C =	round(self.screen.gauge_Couple.value,2)
			U =	round(self.screen.gaugeU_Motor.value,2)
			V =	round(self.screen.gauge_Speed.value,2) 
			I =	round(self.screen.gaugeI_Motor.value,2)
			textFor_txtBox_Measures += "Cr = "	+ str(C)	+ "Nm  "
			textFor_txtBox_Measures += "U = "	+ str(U)	+ "V  "
			textFor_txtBox_Measures += "v = "	+ str(V)	+ "tr/min  "
			textFor_txtBox_Measures += "I = "	+ str(I) 	+ "A \n"
			
			currentU += interval
			currentU = round(currentU,2)
			time.sleep(0.5)
				
		

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
		global textFor_txtBox_SetPoints
		global textFor_txtBox_Measures
		global textFor_lbl_SetPoints
		
		if(self.ids.btn_Auto_START_STOP.text == "STOP"):
			thread_auto_running = False
			self.ids.btn_Auto_LOAD.disabled = False
			self.ids.btn_Auto_START_STOP.text = "START"
			textFor_lbl_SetPoints = "Test : No test in progress"
			self.Automatic_Thread.join(0)
			#todo: arreter le moteur et le frein
		else:
			self.ids.btn_Auto_LOAD.disabled = True
			self.ids.btn_Auto_START_STOP.text = "STOP"
			thread_auto_running = True
			self.Automatic_Thread =thread_auto(self)
			self.Automatic_Thread.start()
			textFor_txtBox_SetPoints = ""
			textFor_txtBox_Measures = ""
			
			
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
				print(":o")
				return
			INV_AUTO_TESTS_IDS = {v: k for k, v in AUTO_TESTS_IDS.items()}
			
			with open(SetUpFile, 'r', newline='') as file:
				reader = csv.reader(file, delimiter=';')
				
				
				for row in reader:
					print(row)
					print(row[0])
					#for(i in range(0, len(INV_AUTO_TESTS_IDS)):
					if(row[0] in AUTO_TESTS_IDS):
						print(":o")
						tb_Scenarios.append(row)
		
		if(len(tb_Scenarios) > 0):
			self.ids.btn_Auto_START_STOP.disabled= False
		else:
			self.ids.btn_Auto_START_STOP.disabled= True
					
	def update(self, dt):
		global thread_auto_running
		global textFor_lbl_SetPoints
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
		self.gauge_Speed.value		= (raw_Speed		*	TABLE_CONVERSION['TM_SP_MOT'])
		self.gauge_Couple.value		= (raw_couple	*	TABLE_CONVERSION['TM_CR_MOT'])
		self.gaugeU_Brake.value		= (raw_U_Brake	*	TABLE_CONVERSION['TM_U_BRAKE'])
		self.gaugeI_brake.value		= (raw_I_Brake	*	TABLE_CONVERSION['TM_I_BRAKE'])
		#At the end of test, button clickable and and script loadable
		if( (idx_current_scenario >= num_of_scenarios) & (thread_auto_running == True) ):
			self.ids.btn_Auto_LOAD.disabled = False
			self.ids.btn_Auto_START_STOP.text = "START"
			thread_auto_running = False
			textFor_lbl_SetPoints = "Test : No test in progress"
		
		self.ids.txtIn_Automatic_SetPoint.text = textFor_txtBox_SetPoints
		self.ids.txtIn_Automatic_Measures.text = textFor_txtBox_Measures
		self.ids.lbl_Automatic_Set_Point.text = textFor_lbl_SetPoints
			
			