
from kivy.app import App
from kivy.config import Config

from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.filechooser import FileChooser
from kivy.lang import Builder
from kivy.uix.popup import Popup
import csv
import os
from dictionary import *
MotorsDatabase = os.curdir+"/Motors_Database"
ScriptsDatabase = os.curdir+"/Automatic_Set_Up"


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
		
		self.Automatic_Script_Content = []
		self.loadedMotorUMax = 0
		self.loadedMotorIMax = 0
		self.loadedMotorSPMax = 0
	def AddScript(self,title):
		print(self.Automatic_Script_Content)
		
		
		
		ScriptFile = ScriptsDatabase+"/"+title+".csv"
		try:
			file = open(ScriptFile, 'r')
			ValidDatas = False
			file.close()
		except IOError:
			file = open(ScriptFile, 'w')
			file.close()
		length = len(self.Automatic_Script_Content)
		
		with open(ScriptFile, 'w', newline='') as file:
			writer = csv.writer(file, delimiter=';')
			for i in range (0,length):
				writer.writerow([self.Automatic_Script_Content[i]])
		
	def AddScenarioToScript(self, TypeScenario, P1 , P2 , CST):
		
		lineScriptFile = [TypeScenario,P1,P2,CST]
		
		CRmax = self.app.AbsoluteMaxRatings['C_COUPLE_MAX']
		if( (P1 != "") & (P2 != "") ):
			if(TypeScenario in AUTO_TESTS_IDS):
				if(TypeScenario == 'U_MIN_TO_U_MAX'):
					if( (float(P1) < self.loadedMotorUMax) & (float(P2) < self.loadedMotorUMax) ):
						self.Automatic_Script_Content.append(lineScriptFile)
						self.ids.txtInput_Script_preparation_File.text += "\nU = " 	+ P1	+ "V to U = "		+ P2 +	"V"
				if(	CST != "") :
					
					if(TypeScenario == 'C_FCT_SP_U_CST'):
						if( (float(P1) < CRmax) & (float(P2) < CRmax) & (float(CST) < self.loadedMotorUMax)):
							self.Automatic_Script_Content.append(lineScriptFile)
							self.ids.txtInput_Script_preparation_File.text += "\nCr = "	+ P1 + "Nm to Cr = "  		+ P2	+ 	"Nm @ U = "	+ CST + "V"
							
					elif(TypeScenario == 'U_FCT_SP_C_CST'):
						if( (float(P1) < self.loadedMotorUMax) & (float(P2) < self.loadedMotorUMax) & (float(CST) < CRmax) ):
							self.Automatic_Script_Content.append(lineScriptFile)
							self.ids.txtInput_Script_preparation_File.text += "\nU = " 	+ P1 + "V to U = " 		+ P2	+ 	"V @ Cr = "	+ CST + "Nm"
							
					elif(TypeScenario == 'SP_FCT_U_C_CST'):
						if( (float(P1) < self.loadedMotorSPMax) & (float(P2) < self.loadedMotorSPMax) & (float(CST) < CRmax) ):
							self.Automatic_Script_Content.append(lineScriptFile)
							self.ids.txtInput_Script_preparation_File.text += "\nv = " 	+ P1 + "tr/min to v = "+ P2 + 	"tr/min @ Cr = "+ CST + "Nm"
	def LoadFileMotorToAutoCfg(self,selection):
		
		if(len(selection)):
			self.ids.file_choosen_input.text = selection[0]
			MotorFile = selection[0]
			self.Automatic_Script_Content = [] #new motor file, reset the script
			try:
					file = open(MotorFile, 'r')
					file.close()
			except IOError:
				return
			Name = "";Type="";UMotorMax=0;PMotorMax=0;IMotorMax=0;SPMotorMax=0
			with open(MotorFile, 'r', newline='') as file:
				reader = csv.reader(file, delimiter=';')
				for row in reader:
					self.Automatic_Script_Content.append(row[0]+";"+row[1])
					if(row[0] == "Name"): 
						Name	= str(row[1])	
					if(row[0] == "Type"):
						Type 	= row[1]
					if(row[0] == "UMotorMax"):
						UMotorMax = float(row[1])
						self.loadedMotorUMax = UMotorMax
					if(row[0] == "IMotorMax"):
						IMotorMax = float(row[1])
						self.loadedMotorIMax = IMotorMax
					if(row[0] == "PMotorMax"):
						PMotorMax = float(row[1])
					if(row[0] == "SpeedMax"):
						SPMotorMax 	= float(row[1])
						self.loadedMotorSPMax = SPMotorMax
			string = str(Type)+" Motor: "+str(Name)
			string += "\nUmax: " + str(UMotorMax) + " Imax: " + str(IMotorMax)
			string += "\nPmax: " + str(PMotorMax) + " Speedmax: " + str(SPMotorMax)
			self.ids.txtInput_Script_preparation_File.text = string
			self.ids.btnAdd_ScriptCfg.disabled  = False
	def updateAddScriptComponents(self,btn_clicked):
		
		if(btn_clicked in AUTO_TESTS_IDS):
			if(btn_clicked == 'U_MIN_TO_U_MAX'):
				self.updte_lbl_txtInput_AddScript('Umin','[V]',True,'Umax','[V]',True,'','Non-used',False)
			elif(btn_clicked == 'C_FCT_SP_U_CST'):
				self.updte_lbl_txtInput_AddScript('Cmin','[Nm]',True,'Cmax','[Nm]',True,'Ucste','[V]',True)
			elif(btn_clicked == 'U_FCT_SP_C_CST'):
				self.updte_lbl_txtInput_AddScript('Umin','[V]',True,'Umax','[V]',True,'Ccste','[Nm]',True)
			elif(btn_clicked == 'SP_FCT_U_C_CST'):
				self.updte_lbl_txtInput_AddScript('Umin','[V]',True,'Umax','[V]',True,'Ccste','[Nm]',True)
			
			
	def updte_lbl_txtInput_AddScript(self,lblP1,txtInputP1,IsEnabledP1,lblP2,txtInputP2,IsEnabledP2,lblCST,txtInputCST,IsEnabledCST):
		self.ids.lbl_AddScript_P1.text = lblP1
		self.ids.lbl_AddScript_P1.disabled = not(IsEnabledP1)
		self.ids.txtInput_AddScript_P1.hint_text=txtInputP1
		
		self.ids.lbl_AddScript_P2.text = lblP2
		self.ids.lbl_AddScript_P2.disabled =not(IsEnabledP2)
		self.ids.txtInput_AddScript_P2.hint_text=txtInputP2
		
		self.ids.lbl_AddScript_CST.text = lblCST
		self.ids.lbl_AddScript_CST.disabled =not(IsEnabledCST)
		self.ids.txtInput_AddScript_CST.hint_text=txtInputCST
		print(self.ids.lbl_AddScript_CST.disabled)

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
		if(len(selection)):
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