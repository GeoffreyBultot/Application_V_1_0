
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
	def __init__(self,comPort,BaudRate, Notify_Appli_Data_Available):
		self.testNumber = 0
		self.rawUMotor = 0
		self.rawIMotor = 0
		self.rawUBrake = 0
		self.rawIBrake = 0
		self.rawSpeed = 0
		self.rawCouple=0
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
				resp = self.spi.xfer2([0x35,2,0x80,0x24,0x41,0x2,0x1,0x2,0x1,0x2,0x1,0x2,0x1,0x2,0x1,0x2])
				time.sleep(0.2)
				
				if(len(resp)==16):
					print(resp)
					if( (resp[0]==0XC5)&(resp[2]==0X80)&(resp[1]==16) ):
						self.rawCouple =resp[3]+((resp[4])<<8)
						self.rawUMotor = resp[5]+((resp[6])<<8)
						self.rawIMotor = resp[7]+((resp[8])<<8)
						self.rawUBrake = resp[9]+((resp[10])<<8)
						self.rawIBrake = resp[11]+((resp[12])<<8)
						self.rawSpeed = resp[13]+((resp[14])<<8)
				#p_data = self.spi.xfer2([0x40,0x00,0x00,0x00])#self.spi.readbytes(1)
				# if(p_data!=[0]):
					# p_data = p_data[0]
					# print(p_data)
					# self.testNumber = (p_data)
					# p_data=None
					
					
					
					
					