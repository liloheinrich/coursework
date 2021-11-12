import serial
import math
import pandas as pd

coeff = [97.4512, -0.841732, 0.00377858, -0.00000921155, 1.1576*10**-8, -5.9236*10**-12]

def convert_ir_to_dist(ir, coeff):
    dist = 0.0
    for i in range(len(coeff)):
        dist += coeff[i] * ir**i
    return dist

arduinoComPort = "COM13"
baudRate = 9600

# open the serial port
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)

tilt = 50
max_tilt_angle = 120

d = {'pan':[], 'tilt':[], 'ir':[], 'dist':[]}
df = pd.DataFrame(data=d)

# main loop to read data from the Arduino, then display it
while tilt < max_tilt_angle:
  # ask for a line of data from the serial port, the ".decode()" converts the
  # data from an "array of bytes", to a string
  lineOfData = serialPort.readline().decode()

  # check if data was received
  if len(lineOfData) > 0:
    # data was received, convert it into integers
    pan, tilt, ir = (float(x) for x in lineOfData.split(','))
    # pan: 30-150, tilt: 60-120, ir: 60-600

    dist = convert_ir_to_dist(ir, coeff)
    # print the results
    print(str(pan), end="")
    print("," + str(tilt), end="")
    print("," + str(ir) + ",", end="")
    print(round(dist, 2))

    # if dist < 24 and dist > 6:
    df_add = {'pan':pan, 'tilt':tilt, 'ir':ir, 'dist':dist}
    df = df.append(df_add, ignore_index=True)

df.to_csv('mp2_data.csv', index=False)