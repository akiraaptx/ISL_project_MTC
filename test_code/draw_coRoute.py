from scipy.io import loadmat
import pygmaps
import webbrowser

structure_data = loadmat('W1_coRoute.mat')
coRoute_data = structure_data['coRoute']
print coRoute_data

longitudes = []
latitudes = []
index = 0

for i in coRoute_data:
  longitudes.append(i[1])
  latitudes.append(i[0])

points = zip(longitudes, latitudes)
path = points

mymap = pygmaps.maps(longitudes[0], latitudes[0], 12)
mymap.addpoint(longitudes[0], latitudes[0], "#0000FF")
mymap.addpoint(longitudes[-1], latitudes[-1], "#FF0000")
mymap.addpath(path, "#00FF00")

#print points
mymap.draw('./mymap.draw.html')
url = './mymap.draw.html'
webbrowser.open_new_tab(url)
  