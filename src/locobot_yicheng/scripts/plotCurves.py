import matplotlib.pyplot as plt
import numpy as np

# close all previous plots
plt.close('all')

# Define the Kp values
kp = [0.5, 1, 2]
# Load data from CSV files
filepaths = [f'data_kp_{kp[0]}.csv',
             f'data_kp_{kp[1]}.csv',
             f'data_kp_{kp[2]}.csv']
data = []

for filepath in filepaths:
    with open(filepath, 'r') as file:
        lines = file.readlines()
        data.append([list(map(float, line.strip().split(','))) for line in lines])

# Extract data from each file
time = [file_data[0] for file_data in data]
x = [file_data[1] for file_data in data]
y = [file_data[2] for file_data in data]
rx = data[0][3]
ry = data[0][4] 

colors = ['r', 'g', 'b']

# find the first index of time that is larger than 20, and only plot the first 20 seconds of x and y
# the time interval is not 0.01s, so we need to find the index of the time that is closest to 20
for i in range(len(time)):
    for j in range(len(time[i])):
        if time[i][j] > 20:
            time_20s = time[i][:j]
            break

rx = rx[:len(time_20s)]
ry = ry[:len(time_20s)]

# Plotting the first figure
plt.figure(1)
plt.plot(time_20s, rx, label='Reference rx', color='k', linestyle='--') 

for i, color in zip(range(len(filepaths)), colors):
    plt.plot(time_20s, x[i][:len(time_20s)], label=f'Kp = {kp[i]}',color=color)
plt.xlabel('Time (s)')
plt.ylabel('X Position')
plt.title('X Position over Time for Different Kp Values')
plt.legend()
plt.savefig('X Position over Time for Different Kp Values.pdf')

# Plotting the second figure
plt.figure(2)
plt.plot(time_20s, ry, label='Reference ry', color='k', linestyle='--')
for i, color in zip(range(len(filepaths)), colors):
    plt.plot(time_20s, y[i][:len(time_20s)], label=f'Kp = {kp[i]}', color=color)
plt.xlabel('Time (s)')
plt.ylabel('Y Position')
plt.title('Y Position over Time for Different Kp Values')
plt.legend()
plt.savefig('Y Position over Time for Different Kp Values.pdf')

# Show the plots
plt.show()

