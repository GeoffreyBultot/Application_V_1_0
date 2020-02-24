#:pyserial 3.4

__all__ = ('LabtoolLayer',)
__title__ = 'Application_V_0_1'
__version__ = '0.1'
__author__ = 'Bultot Geoffrey'

'''
########################### IDENTIFICATION #############################
## Project          : TEST BENCH MECA ISIB
## File name        : LabtoolLayer.py
## Description      : functions library for the testbench interface
## Contact          : BULTOT Geoffrey
## Creation date    : 12/02/2011 14h17
## for python 3.7.4
########################################################################
'''

import datetime             #same
import time
from threading import RLock
import UartLayer
'''Verrou for Communications with the DPC'''
Verrou_dpc = RLock()


'''
______________________________________________________________
                        Telemetries ID                    
______________________________________________________________
'''

C_TM_ID_GET_TM          = 0x10
C_TM_ID_GET_PARAM       = 0x11
C_TM_ID_GET_SUPPLY      = 0x12
C_TM_ID_GET_ERR_VECT    = 0X13
C_TM_ID_GET_COUNT       = 0x14

'''
______________________________________________________________
                        Telecommands ID                    
______________________________________________________________
'''
TC_ID_SET_PARAMETERS    = 0X11
TC_ID_ERASE_ERR_VECT    = 0x13

'''
______________________________________________________________
                        Dictionnary
______________________________________________________________
'''

class LabtoolLayer(object):
    """description of class"""    
    tm = 112
    def TMTC_CallBack(self):
        pass

    def __init__(self):

        '''
        ______________________________________________________________
                                Bytes position                    
        ______________________________________________________________
        '''
        
        '''object TMTC to dialog with the TMTC bbk on the DPC'''
        #TODO: modify the Module ID, and Baud rate
        self.TMTC_COM = UartLayer.UartLayer("COM10",9600,self.TMTC_CallBack)

        ''' Acknowledges '''
  