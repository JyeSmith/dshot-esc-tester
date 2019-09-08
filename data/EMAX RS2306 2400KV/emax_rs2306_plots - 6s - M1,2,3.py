# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:53:08 2019

@author: Jye
"""

import numpy as np
import matplotlib.pyplot as plt


eleven_turn_1 = np.genfromtxt('11_turn - 6s.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_2 = np.genfromtxt('11_turn - 6s - 2.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_3 = np.genfromtxt('11_turn - 6s - 3.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])

eleven_turn_5046_1 = np.genfromtxt('11_turn_cyclone_5046 - 6s.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_5046_2 = np.genfromtxt('11_turn_cyclone_5046 - 6s - 2.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_5046_3 = np.genfromtxt('11_turn_cyclone_5046 - 6s - 3.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])


## KV plot
fig = plt.figure() 
ax1 = fig.add_subplot(221)
ax1.title.set_text('KV')
#ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))
fig.subplots_adjust(right=0.75)

ax3.plot(eleven_turn_1['Time_ms'], eleven_turn_1['dshot'], color='y', label='dshot')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

#ax1.plot(original['Time_ms'], original['RPM'] / original['Voltage_V'], color='b', label='original')
#ax1.plot(eight_turn['Time_ms'], eight_turn['RPM'] / eight_turn['Voltage_V'], color='r', label='8 turn')
#ax1.plot(nine_turn['Time_ms'], nine_turn['RPM'] / nine_turn['Voltage_V'], color='g', label='9 turn')
ax1.plot(eleven_turn_1['Time_ms'], eleven_turn_1['RPM'] / eleven_turn_1['Voltage_V'], color='b', label='11 turn - 1')
ax1.plot(eleven_turn_2['Time_ms'], eleven_turn_2['RPM'] / eleven_turn_2['Voltage_V'], color='r', label='11 turn - 2')
ax1.plot(eleven_turn_3['Time_ms'], eleven_turn_3['RPM'] / eleven_turn_3['Voltage_V'], color='g', label='11 turn - 3')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('KV')
ax1.set_ylim([1500, 2500])
ax1.legend()


## Response plot
ax1 = fig.add_subplot(223)
ax1.title.set_text('Response - Cyclone 5046 Vs 5050')
#ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))
fig.subplots_adjust(right=0.75)

ax3.plot(eleven_turn_5046_1['Time_ms'], eleven_turn_5046_1['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

#ax1.plot(original_5046['Time_ms'], original_5046['Thrust_g'], color='b', label='original')
#ax1.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'], color='r', label='8 turn')
ax1.plot(eleven_turn_5046_1['Time_ms'], eleven_turn_5046_1['Thrust_g'], color='b', label='11 turn - 5046 - 1')
ax1.plot(eleven_turn_5046_2['Time_ms'], eleven_turn_5046_2['Thrust_g'], color='r', label='11 turn - 5046 - 2')
ax1.plot(eleven_turn_5046_3['Time_ms'], eleven_turn_5046_3['Thrust_g'], color='g', label='11 turn - 5046 - 3')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('Thrust (g)')
ax1.set_xlim([11900, 12300])
ax1.set_ylim([0, 1500])
ax1.legend()


## Thrust efficiency plot Cyclone 5046
ax1 = fig.add_subplot(222)
ax1.title.set_text('Thrust (g) & Efficiency (g/W) - Cyclone 5046')
ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))

ax3.plot(eleven_turn_5046_1['Time_ms'], eleven_turn_5046_1['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

#ax2.plot(original_5046['Time_ms'], original_5046['Thrust_g'] / (original_5046['Voltage_V'] * original_5046['Current_A']/10), color='b', label='original')
#ax2.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'] / (eight_turn_5046['Voltage_V'] * eight_turn_5046['Current_A']/10), color='r', label='8 turn')
#ax2.plot(nine_turn_5046['Time_ms'], nine_turn_5046['Thrust_g'] / (nine_turn_5046['Voltage_V'] * nine_turn_5046['Current_A']/10), color='g', label='9 turn')
ax2.plot(eleven_turn_5046_1['Time_ms'], eleven_turn_5046_1['Thrust_g'] / (eleven_turn_5046_1['Voltage_V'] * eleven_turn_5046_1['Current_A']/10), color='b', label='11 turn - 1')
ax2.plot(eleven_turn_5046_2['Time_ms'], eleven_turn_5046_2['Thrust_g'] / (eleven_turn_5046_2['Voltage_V'] * eleven_turn_5046_2['Current_A']/10), color='r', label='11 turn - 2')
ax2.plot(eleven_turn_5046_3['Time_ms'], eleven_turn_5046_3['Thrust_g'] / (eleven_turn_5046_3['Voltage_V'] * eleven_turn_5046_3['Current_A']/10), color='g', label='11 turn - 3')
ax2.set_ylabel('Efficiency (g/W)')
ax2.set_ylim([0, 5])

#ax1.plot(original_5046['Time_ms'], original_5046['Thrust_g'], color='b', label='original')
#ax1.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'], color='r', label='8 turn')
#ax1.plot(nine_turn_5046['Time_ms'], nine_turn_5046['Thrust_g'], color='g', label='9 turn')
ax1.plot(eleven_turn_5046_1['Time_ms'], eleven_turn_5046_1['Thrust_g'], color='b', label='11 turn - 1')
ax1.plot(eleven_turn_5046_2['Time_ms'], eleven_turn_5046_2['Thrust_g'], color='r', label='11 turn - 2')
ax1.plot(eleven_turn_5046_3['Time_ms'], eleven_turn_5046_3['Thrust_g'], color='g', label='11 turn - 3')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('Thrust (g)')
ax1.set_ylim([0, 1500])
ax1.legend()


### Thrust efficiency plot Cyclone 5050
#ax1 = fig.add_subplot(224)
#ax1.title.set_text('Thrust (g) & Efficiency (g/W) - Cyclone 5050')
#ax2 = ax1.twinx()
#ax3 = ax1.twinx()
#ax3.spines["right"].set_position(("axes", 1.2))
#
#ax3.plot(eleven_turn_5050['Time_ms'], eleven_turn_5050['dshot'], color='y', label='dshot')
#ax3.set_xlabel('Time_ms')
#ax3.set_ylabel('dshot')
#ax3.set_ylim([0, 2100]) 
#
##ax2.plot(original_5050['Time_ms'], original_5050['Thrust_g'] / (original_5050['Voltage_V'] * original_5050['Current_A']/10), color='b', label='original')
##ax2.plot(eight_turn_5050['Time_ms'], eight_turn_5050['Thrust_g'] / (eight_turn_5050['Voltage_V'] * eight_turn_5050['Current_A']/10), color='r', label='8 turn')
##ax2.plot(nine_turn_5050['Time_ms'], nine_turn_5050['Thrust_g'] / (nine_turn_5050['Voltage_V'] * nine_turn_5050['Current_A']/10), color='g', label='9 turn')
#ax2.plot(eleven_turn_5050['Time_ms'], eleven_turn_5050['Thrust_g'] / (eleven_turn_5050['Voltage_V'] * eleven_turn_5050['Current_A']/10), color='orange', label='11 turn')
#ax2.plot(eleven_turn_5050_ms['Time_ms'], eleven_turn_5050_ms['Thrust_g'] / (eleven_turn_5050_ms['Voltage_V'] * eleven_turn_5050_ms['Current_A']/10), color='r', label='11 turn multistrand')
#ax2.set_ylabel('Efficiency (g/W)')
#ax2.set_ylim([0, 5])
#
##ax1.plot(original_5050['Time_ms'], original_5050['Thrust_g'], color='b', label='original')
##ax1.plot(eight_turn_5050['Time_ms'], eight_turn_5050['Thrust_g'], color='r', label='8 turn')
##ax1.plot(nine_turn_5050['Time_ms'], nine_turn_5050['Thrust_g'], color='g', label='9 turn')
#ax1.plot(eleven_turn_5050['Time_ms'], eleven_turn_5050['Thrust_g'], color='orange', label='11 turn')
#ax1.plot(eleven_turn_5050_ms['Time_ms'], eleven_turn_5050_ms['Thrust_g'], color='r', label='11 turn multistrand')
#ax1.set_xlabel('Time_ms')
#ax1.set_xlim([3500, 25000])
#ax1.set_ylabel('Thrust (g)')
#ax1.set_ylim([0, 1500])
#ax1.legend() 