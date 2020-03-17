#:pyserial 3.4

__all__ = ('LabtoolLayer',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'

'''
########################### IDENTIFICATION #############################
## Project			: TEST BENCH MECA ISIB
## File name		: LabtoolLayer.py
## Description		: functions library for the testbench interface
## Contact			: BULTOT Geoffrey
## Creation date	: 12/02/2011 14h17
## for python 3.7.4
########################################################################
'''

import datetime				#same
import time
from threading import RLock
import UartLayer
from dictionary import *
'''Verrou for Communications with the DPC'''


'''
______________________________________________________________
						Telemetries ID					  
______________________________________________________________
'''

C_TM_ID_GET_TM			= 0x10
C_TM_ID_GET_PARAM		= 0x11
C_TM_ID_GET_SUPPLY		= 0x12
C_TM_ID_GET_ERR_VECT	= 0X13
C_TM_ID_GET_COUNT		= 0x14

'''
______________________________________________________________
						Telecommands ID					   
______________________________________________________________
'''
TC_ID_SET_PARAMETERS	= 0X11
TC_ID_ERASE_ERR_VECT	= 0x13

'''
______________________________________________________________
						Dictionnary
______________________________________________________________
'''

class LabtoolLayer(object):
	"""description of class"""	  
	tm = 112

	def __init__(self,app):
		self.app = app
		'''
		______________________________________________________________
								Bytes position					  
		______________________________________________________________
		'''
		
		'''object TMTC to dialog with the TMTC bbk on the DPC'''
		#TODO: modify the Module ID, and Baud rate
		self.TMTC_COM = UartLayer.UartLayer(self.app)

		''' Acknowledges '''
	def FloatToRaw(self,floatValue,nameTM):
		value = float(floatValue)
		value /= ( TABLE_CONVERSION[nameTM] ) 
		value = int(value)
		return value
	
	def RawToFloat(self,rawValue,nameTM):
		value = rawValue
		value *= ( TABLE_CONVERSION[nameTM] ) 
		value = int(value)
		return value
		
	def SendTC(self,TC_ID,P1,P2=0X0000):
		#print("OK BOOMER")
		ArrayToSend = []
		print(P1)
		ArrayToSend.append(0X20)
		ArrayToSend.append(TC_ID)
		ArrayToSend.append(int(P1/256))
		ArrayToSend.append(P1&0XFF)
		ArrayToSend.append(int(P2/256))
		ArrayToSend.append(P2&0XFF)
		print(ArrayToSend)
		self.TMTC_COM.SendDatas(ArrayToSend)

	def SetMode(self,mode):
		value = 1
		self.SendTC(TC_TABLE_ID['TC_SET_MODE'],mode)
		
	def SetUmot(self,value):	
		value = self.FloatToRaw(value,'TM_U_MOT')
		self.SendTC(TC_TABLE_ID['TC_SET_U_MOT'],value)

	def SetImot(self,value):
		value = self.FloatToRaw(value,'TM_I_MOT')
		self.SendTC(TC_TABLE_ID['TC_SET_I_MOT'],value)

	def SetUbrake(self,value):
		value = self.FloatToRaw(value,'TM_U_BRAKE')
		self.SendTC(TC_TABLE_ID['TC_SET_U_BRAKE'],value)
	
	def SetIbrake(self,value):
		value = self.FloatToRaw(value,'TM_I_BRAKE')
		self.SendTC(TC_TABLE_ID['TC_SET_I_BRAKE'],value)
	
	def SetSpeedMot(self,value):
		value = self.FloatToRaw(value,'TM_SP_MOT')
		self.SendTC(TC_TABLE_ID['TC_SET_SP_MOT'],value)
	
	def SetCrMot(self,value):
		value = self.FloatToRaw(value,'TM_CR_MOT')
		self.SendTC(TC_TABLE_ID['TC_SET_CR_MOT'],value)
		
	
  