
#:pyserial 3.4

__all__ = ('UartLayer',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'

import serial
import serial.tools.list_ports
from threading import Thread
import time
import spidev
from dictionary import *

C_BUS_IDLE = 0x00
C_BUS_BUSY = 0x01


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
		sys.exit()

	'''****************************************************************************************'''
	def __init__(self,app):
		self.app = app
		self.BusState = C_BUS_IDLE
		# We only have SPI bus 0 available to us on the Pi
		bus = 0
		#Device is the chip select pin. Set to 0 or 1, depending on the connections
		device = 0
		# Enable SPI
		self.spi = spidev.SpiDev()
		# Open a connection to a specific bus and device (chip select pin)
		self.spi.open(bus, device)
		# Set SPI speed and mode
		self.spi.max_speed_hz = 375000
		
		self.spi.lsbfirst=False
		
		self.spi.mode=0b00
		
		self.ReadBus_Threat_ON	= True
		self.ReadThread= Thread(target=self.RefreshTM_Thread,args=())
		self.ReadThread.start()
		
		
		'''Buffers to store Telemetries received by DPC'''
		
	def SendDatas(self,array):
		while(self.BusState == C_BUS_BUSY):
			pass
		self.BusState == C_BUS_BUSY
		respA=self.spi.xfer2(array)
		resp = self.spi.readbytes(6)
		self.BusState == C_BUS_IDLE
		
		
	def RefreshTM_Thread(self):
			#To store the current segment
			CurrentSegment = []
			#Current position of segment
			Rx_framePosition = 0
			
			Message_Sent = False
			inv_TM_TABLE_ID = {v: k for k, v in TM_TABLE_ID.items()}		#reverse the id table to get the name depending of the ID 
			#print(inv_TM_TABLE_ID)
			while self.ReadBus_Threat_ON:
				temptable = []
				if(self.BusState == C_BUS_IDLE):
					self.BusState = C_BUS_BUSY
					for i in range (0,len(TM_TABLE_ID)):	
						ID = TM_TABLE_ID[inv_TM_TABLE_ID[i]]
						respA=self.spi.xfer2([0x80,i,0,0,0,0])#,0x80,0x24,0x41,0x2,0x1,0x2,0x1,0x2,0x1,0x2,0x1,0x2,0x1,0x2])
						temptable.append(self.spi.readbytes(6))
					buff_Telemetries_Words = []
					for i in range (0,len(temptable)):
						data_temp =  temptable[i][1]
						data_temp += temptable[i][2] * 256
						buff_Telemetries_Words.append(data_temp)
						
					#print(buff_Telemetries_Words)
					self.app.Table_Tm_Reg =buff_Telemetries_Words
					self.BusState = C_BUS_IDLE
					time.sleep(0.1)
					
					
					
				#self.app.Table_Tm_Reg = self.TM_list
				# if( (resp[0]==0XC5)&(resp[2]==0X80)&(resp[1]==16) ):
					# self.rawCouple =resp[3]+((resp[4])<<8)
					# self.rawUMotor = resp[5]+((resp[6])<<8)
					# self.rawIMotor = resp[7]+((resp[8])<<8)
					# self.rawUBrake = resp[9]+((resp[10])<<8)
					# self.rawIBrake = resp[11]+((resp[12])<<8)
					# self.rawSpeed = resp[13]+((resp[14])<<8)
			#p_data = self.spi.xfer2([0x40,0x00,0x00,0x00])#self.spi.readbytes(1)
			# if(p_data!=[0]):
				# p_data = p_data[0]
				# print(p_data)
				# self.testNumber = (p_data)
				# p_data=None
				
				
					
					
					