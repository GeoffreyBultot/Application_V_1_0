TM_dict ={
    }


Manual_TC_dict = {
    'Manual_TC_Set_Umotor':1,
    'Manual_TC_Set_Imotor':2,
    'Manual_TC_Set_Speed':3,
    'Manual_TC_Set_Couple':4
    }


Screens_dict = {
    0 : 'HomeScreen' ,
    1 : 'ManualScreen',
    2 : 'AutomaticScreen',
    3 : 'SettingsScreen'}
	
#make a correspondence between TM and their line in tha matrice
TM_TABLE_ID = {	'TM_TB_MODE':		0,
							'TM_CR_MOT':			1,
							'TM_U_MOT':			2,
							'TM_I_MOT':			3,
							'TM_SP_MOT':			4,
							'TM_PWM_MOT':		5,
							'TM_U_BRAKE':		6,
							'TM_I_BRAKE':		7,
							'TM_PWM_BRAKE':	8,} 

#make a correspondence between TC and their line in tha matrice
TC_TABLE_ID = {	'TC_SET_MODE':				0,
							'TC_SET_CR_MOT':			1,
							'TC_SET_U_MOT':			2,
							'TC_SET_I_MOT':				3,
							'TC_SET_SP_MOT':			4,
							'TC_SET_PWM_MOT':		5,
							'TC_SET_U_BRAKE':			6,
							'TC_SET_I_BRAKE':			7,
							'TC_SET_PWM_BRAKE':	8,} 
							
							
#conversion : 
#when TM received : Raw value * factor = real value
#To send TC parameter : Real value / factor = raw_value
TABLE_CONVERSION = {	'TM_CR_MOT'		:			0.00724,#0.039*0.186
									'TM_U_MOT'		:			0.037875,#3.3/4095/0.0223),
									'TM_I_MOT'		:			0.00236,#3,3.3/4095/6.82927/0.05)
									'TM_SP_MOT'		:			10,#NOT REAL
									'TM_U_BRAKE'		:			0.037875,#
									'TM_I_BRAKE'		:			0.00236}#
									
									
									
