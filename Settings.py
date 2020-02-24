
from kivy.app import App
from kivy.config import Config

from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.filechooser import FileChooser
from kivy.lang import Builder
from kivy.uix.popup import Popup
import csv
import os
	
MotorsDatabase = os.curdir+"/Motors_Database"

class SettingsScreen(Screen):
	i = 0
	j = 0
	def __init__(self, app, **kwargs):
		super(SettingsScreen, self).__init__(**kwargs)
		#layout = FloatLayout()
		#self.add_widget(layout)
		self.app = app
		
		self.Popup_Choose_File = self.ids.Popup_Choose_File
		self.Popup_Edit_Motor = self.ids.Popup_Edit_Motor
		self.Popup_Add_Motor = self.ids.Popup_Add_Motor
		
	def AddMotor(self, Type, Name , MaxI , MaxU , MaxP , MaxSpeed , AddOrEdit):
		MaxValues = self.app.AbsoluteMaxRatings
				
		if not os.path.exists(MotorsDatabase):
			os.mkdir(MotorsDatabase)
		
		ValidDatas = True
		MotorFile = MotorsDatabase+"/"+Name+".csv"
		
		try:
			if not( self.IsRightValue(float(MaxI),MaxValues['C_I_MOT_MAX'])):
				ValidDatas = False
			if not( self.IsRightValue(float(MaxU),MaxValues['C_U_MOT_MAX'])):
				ValidDatas = False
			if not( self.IsRightValue(float(MaxP),MaxValues['C_P_MOT_MAX'])):
				ValidDatas = False
			if not( self.IsRightValue(float(MaxSpeed),MaxValues['C_SPEED_MOT_MAX'])):
				ValidDatas = False
		except:
			ValidDatas = False
		
		if(ValidDatas):
			try:
				file = open(MotorFile, 'r')
				ValidDatas = False
				file.close()
			except IOError:
				file = open(MotorFile, 'w')
				file.close()
				
			with open(MotorFile, 'w', newline='') as file:
				writer = csv.writer(file, delimiter=';')
				writer.writerow(["Name", Name])
				writer.writerow(["Type", Type])
				writer.writerow(["UMotorMax", MaxU])
				writer.writerow(["IMotorMax", MaxI])
				writer.writerow(["PMotorMax", MaxP])
				writer.writerow(["SpeedMax", MaxSpeed])
			pass
		
	def IsRightValue(self,value,max):
		ret = True
		if value>max :
			ret = False
		return ret
		
	def LoadFileToModify(self,selection):
		
		self.ids.file_choosen_input.text = selection[0]
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
					self.ids.EditMotor_Name.text = row[1]
				if(row[0] == "Type"):
					pass#self.ids.EditMotor_Name.text = 
				if(row[0] == "UMotorMax"):
					self.ids.EditMotor_MaxU.text = row[1]
					
				if(row[0] == "IMotorMax"):
					self.ids.EditMotor_MaxI.text = row[1]
					
				if(row[0] == "PMotorMax"):
					self.ids.EditMotor_MaxP.text = row[1]
					
				if(row[0] == "SpeedMax"):
					self.ids.EditMotor_MaxSpeed.text = row[1]
					
			
	
	def update(self, dt):
		pass