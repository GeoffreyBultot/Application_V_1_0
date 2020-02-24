
#:pyserial 3.4

__all__ = ('UartLayer',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'

import serial
import serial.tools.list_ports
from threading import Thread

class UartLayer(object):
	'''
	classdocs
	''' 
	def quit(self):
		'''
		close UART connexion 
		'''
		self.ReadBus_Threat_ON	= False
		self.ReadThread1.join(0)
		self.ser.close()
		sys.exit()

	'''****************************************************************************************'''
	def __init__(self,comPort,BaudRate, Notify_Appli_Data_Available):
		#serialPort = OpenSerialPort('/dev/ttyUSB0')	   
		ports = serial.tools.list_ports.comports()
		self.testNumber = 0
		available_ports = []
		for p in ports:
			#ser = serial.Serial(p[0], BaudRate)
			available_ports.append(p[0])
		self.ser = serial.Serial(available_ports[0],BaudRate)
		self.ReadBus_Threat_ON	= True
		self.ReadThread= Thread(target=self.ReadBus_Threat,args=())
		self.ReadThread.start()
		'''Buffers to store Telemetries received by DPC'''
		
		
	def ReadBus_Threat(self):
			#To store the current segment
			CurrentSegment = []
			#Current position of segment
			Rx_framePosition = 0
			
			Message_Sent = False
			
			while self.ReadBus_Threat_ON:
				p_data = self.ser.read()
				p_data = ord(p_data)
				print(p_data)
				self.testNumber = (p_data)