import pygmaps
import webbrowser

mymap = pygmaps.maps(43.579477,  -86.399497, 9)
# mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)
mymap.addpoint(37.427, -122.145, "#0000FF00")
mymap.addradpoint(37.429, -122.145, 1,  "#FF0000")

mymap.addpoint(42.99551, -82.44329, "#0000FF")
mymap.addpoint(42.99025, -82.45914, "#0000FF")
path2 = [(42.99551, -82.44329), (42.99025, -82.45914)]
mymap.addpath(path2, "#00FF00")

mymap.addpoint(43.579477, -86.399497, "#0000FF")
mymap.addpoint(43.55168, -86.39228, "#0000FF")
path3 = [(43.579477, -86.399497), (43.55168, -86.39228)]
mymap.addpath(path3, "#FF0000")

mymap.draw('./mymap.draw.html')
url = './mymap.draw.html'
webbrowser.open_new_tab(url)