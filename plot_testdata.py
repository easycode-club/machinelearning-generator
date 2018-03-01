import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


dataframe = pd.read_csv('data.csv')
data = dataframe.values
a = data[:,[1]]
b = data[:,[2]]

c = data[:,[3]]

ax.scatter(a,b,c)

plt.show()
