
import numpy as np
import matplotlib.pyplot as plt
import sys

print(sys.argv[1])

thrustFile = sys.argv[1]

data = np.genfromtxt(thrustFile, delimiter=',', skip_header=1,
                     names=['Time_ms', 'dshot', 'Voltage_V', 'Current_A', 'RPM', 'Thrust_g'])
fig = plt.figure()

ax1 = fig.add_subplot(311)
fig.subplots_adjust(right=0.75)
ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))

ax3.plot(data['Time_ms'], data['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100])

ax2.plot(data['Time_ms'], data['Thrust_g']/(data['Voltage_V']*data['Current_A']/10), color='r', label='g/W')
ax2.set_ylabel('g/W')
ax2.set_ylim([0, 5])
ax2.legend()

ax1.plot(data['Time_ms'], data['Thrust_g'], color='b', label='Thrust (g)')
ax1.set_ylabel('Thrust (g)')
ax1.set_ylim([0, 1500])
ax1.legend()


ax1 = fig.add_subplot(312)
fig.subplots_adjust(right=0.75)
ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))

ax3.plot(data['Time_ms'], data['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100])

ax2.plot(data['Time_ms'], data['Voltage_V'], color='r', label='Voltage (V)')
ax2.set_ylabel('Voltage (V)')
ax2.set_ylim([15.5, 26])
ax2.legend()

ax1.plot(data['Time_ms'], data['Current_A']/10, color='b', label='Current (A)')
ax1.set_ylabel('Current (A)')
ax1.set_ylim([0, 50])
ax1.legend()


ax1 = fig.add_subplot(313)
fig.subplots_adjust(right=0.75)
ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.2))

ax3.plot(data['Time_ms'], data['dshot'], color='y', label='dshot')
ax3.set_xlabel('Time_ms')
ax3.set_ylabel('dshot')
ax3.set_ylim([0, 2100])

ax1.plot(data['Time_ms'], data['RPM'], color='r', label='RPM')
ax1.set_ylabel('RPM')
ax1.set_ylim([0, 30000])
ax1.legend()

ax2.plot(data['Time_ms'], data['RPM']/data['Voltage_V'], color='b', label='KV')
ax2.set_ylabel('KV')
ax2.set_ylim([0, 2600])
ax2.legend()


fig.savefig(thrustFile+'.plot.png')
#fig.savefig('plot.pdf')