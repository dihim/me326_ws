import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV files
filepaths = ['src/locobot_yicheng/scripts/data_kp_0.5.csv',
             'src/locobot_yicheng/scripts/data_kp_1.csv',
             'src/locobot_yicheng/scripts/data_kp_2.csv']
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

# Plotting the first figure
plt.figure(1)
for i in range(len(filepaths)):
    plt.plot(time[i], x[i], label=f'File {i+1}')
plt.plot(time[0], rx, label='Reference rx')
plt.xlabel('Time (s)')
plt.ylabel('X Position')
plt.title('X Position over Time for Different Kp Values')
plt.legend()

# Plotting the second figure
plt.figure(2)
for i in range(len(filepaths)):
    plt.plot(time[i], y[i], label=f'File {i+1}')
plt.plot(time[0], ry, label='Reference ry')
plt.xlabel('Time (s)')
plt.ylabel('Y Position')
plt.title('Y Position over Time for Different Kp Values')
plt.legend()

# Show the plots
plt.show()
