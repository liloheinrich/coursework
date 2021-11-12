import math
import matplotlib.pyplot as plt
import pandas as pd
# import astropy.coordinates as ac

def compensate_angle(pan, tilt, dist):
    pan_radians = - math.radians(pan)
    tilt_radians = - math.radians(tilt)

    x = dist * math.sin(pan_radians) 
    y = dist * math.sin(tilt_radians) 
    z = dist * math.cos(pan_radians) * math.cos(tilt_radians)
    # z, x, y = ac.spherical_to_cartesian(dist, tilt_radians, pan_radians)

    return float(x), float(y), float(z)

data = pd.read_csv('mp2_data_final.csv')
df = pd.DataFrame(data=data)
print(df)

pan_center_angle = 90
tilt_center_angle = 90
df["pan_centered"] = df["pan"] - pan_center_angle
df["tilt_centered"] = df["tilt"] - tilt_center_angle

x, y, z = [], [], []
for i in range(len(df)):
    x_i, y_i, z_i = compensate_angle(df["pan_centered"][i], df["tilt_centered"][i], df["dist"][i])
    # print(df["tilt_centered"][i])
    # if df["tilt_centered"][i] == -10.0:
    if df["tilt_centered"][i] == 0.0:

    # if z_i < 19 and z_i > 17 and y_i > -4.0:
        x.append(round(x_i, 2))
        y.append(round(y_i, 2))
        z.append(round(z_i, 2))

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot()
# plt.scatter(x, y)
ax.set_xlabel('x (inches)')
ax.set_ylabel('y (inches)')
ax.set_aspect('equal', adjustable='box')
# ax = plt.axes(projection='3d')
# ax.scatter3D(x, y, z)
# ax.set_zlabel('z (inches)')
plt.scatter(x, z)
ax.set_ylabel('z (inches)')
plt.show()