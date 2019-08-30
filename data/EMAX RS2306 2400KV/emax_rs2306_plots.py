# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:53:08 2019

@author: Jye
"""

import numpy as np
import matplotlib.pyplot as plt

original = np.genfromtxt('original.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eight_turn = np.genfromtxt('8_turn.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
nine_turn = np.genfromtxt('9_turn.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn = np.genfromtxt('11_turn.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])

original_5046 = np.genfromtxt('original_cyclone_5046.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eight_turn_5046 = np.genfromtxt('8_turn_cyclone_5046.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
nine_turn_5046 = np.genfromtxt('9_turn_cyclone_5046.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_5046 = np.genfromtxt('11_turn_cyclone_5046.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])

original_5050 = np.genfromtxt('original_cyclone_5050.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eight_turn_5050 = np.genfromtxt('8_turn_cyclone_5050.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
nine_turn_5050 = np.genfromtxt('9_turn_cyclone_5050.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
eleven_turn_5050 = np.genfromtxt('11_turn_cyclone_5050.csv', delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])

## KV plot
fig = plt.figure() 
ax1 = fig.add_subplot(221)
ax1.title.set_text('KV')
#ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))
fig.subplots_adjust(right=0.75)

ax3.plot(original['Time_ms'], original['dshot'], color='y', label='dshot')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

ax1.plot(original['Time_ms'], original['RPM'] / original['Voltage_V'], color='b', label='original')
ax1.plot(eight_turn['Time_ms'], eight_turn['RPM'] / eight_turn['Voltage_V'], color='r', label='8 turn')
ax1.plot(nine_turn['Time_ms'], nine_turn['RPM'] / nine_turn['Voltage_V'], color='g', label='9 turn')
ax1.plot(eleven_turn['Time_ms'], eleven_turn['RPM'] / eleven_turn['Voltage_V'], color='orange', label='11 turn')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('KV')
ax1.set_ylim([1500, 2500])
ax1.legend()


## Response plot
ax1 = fig.add_subplot(223)
ax1.title.set_text('Response - Cyclone 5046')
#ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))
fig.subplots_adjust(right=0.75)

ax3.plot(original['Time_ms'], original['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

ax1.plot(original_5046['Time_ms'], original_5046['Thrust_g'], color='b', label='original')
ax1.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'], color='r', label='8 turn')
ax1.plot(nine_turn_5046['Time_ms'], nine_turn_5046['Thrust_g'], color='g', label='9 turn')
ax1.plot(eleven_turn_5046['Time_ms'], eleven_turn_5046['Thrust_g'], color='orange', label='11 turn')
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

ax3.plot(original_5046['Time_ms'], original_5046['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

ax2.plot(original_5046['Time_ms'], original_5046['Thrust_g'] / (original_5046['Voltage_V'] * original_5046['Current_A']/10), color='b', label='original')
ax2.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'] / (eight_turn_5046['Voltage_V'] * eight_turn_5046['Current_A']/10), color='r', label='8 turn')
ax2.plot(nine_turn_5046['Time_ms'], nine_turn_5046['Thrust_g'] / (nine_turn_5046['Voltage_V'] * nine_turn_5046['Current_A']/10), color='g', label='9 turn')
ax2.plot(eleven_turn_5046['Time_ms'], eleven_turn_5046['Thrust_g'] / (eleven_turn_5046['Voltage_V'] * eleven_turn_5046['Current_A']/10), color='orange', label='11 turn')
ax2.set_ylabel('Efficiency (g/W)')
ax2.set_ylim([0, 5])

ax1.plot(original_5046['Time_ms'], original_5046['Thrust_g'], color='b', label='original')
ax1.plot(eight_turn_5046['Time_ms'], eight_turn_5046['Thrust_g'], color='r', label='8 turn')
ax1.plot(nine_turn_5046['Time_ms'], nine_turn_5046['Thrust_g'], color='g', label='9 turn')
ax1.plot(eleven_turn_5046['Time_ms'], eleven_turn_5046['Thrust_g'], color='orange', label='11 turn')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('Thrust (g)')
ax1.set_ylim([0, 1500])
ax1.legend()


## Thrust efficiency plot Cyclone 5050
ax1 = fig.add_subplot(224)
ax1.title.set_text('Thrust (g) & Efficiency (g/W) - Cyclone 5050')
ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))

ax3.plot(original_5050['Time_ms'], original_5050['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100]) 

ax2.plot(original_5050['Time_ms'], original_5050['Thrust_g'] / (original_5050['Voltage_V'] * original_5050['Current_A']/10), color='b', label='original')
ax2.plot(eight_turn_5050['Time_ms'], eight_turn_5050['Thrust_g'] / (eight_turn_5050['Voltage_V'] * eight_turn_5050['Current_A']/10), color='r', label='8 turn')
ax2.plot(nine_turn_5050['Time_ms'], nine_turn_5050['Thrust_g'] / (nine_turn_5050['Voltage_V'] * nine_turn_5050['Current_A']/10), color='g', label='9 turn')
ax2.plot(eleven_turn_5050['Time_ms'], eleven_turn_5050['Thrust_g'] / (eleven_turn_5050['Voltage_V'] * eleven_turn_5050['Current_A']/10), color='orange', label='11 turn')
ax2.set_ylabel('Efficiency (g/W)')
ax2.set_ylim([0, 5])

ax1.plot(original_5050['Time_ms'], original_5050['Thrust_g'], color='b', label='original')
ax1.plot(eight_turn_5050['Time_ms'], eight_turn_5050['Thrust_g'], color='r', label='8 turn')
ax1.plot(nine_turn_5050['Time_ms'], nine_turn_5050['Thrust_g'], color='g', label='9 turn')
ax1.plot(eleven_turn_5050['Time_ms'], eleven_turn_5050['Thrust_g'], color='orange', label='11 turn')
ax1.set_xlabel('Time_ms')
ax1.set_xlim([3500, 25000])
ax1.set_ylabel('Thrust (g)')
ax1.set_ylim([0, 1500])
ax1.legend() 