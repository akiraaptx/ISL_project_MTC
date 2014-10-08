import scipy.io as spio
import pygmaps
import webbrowser
import os
import errno
import gzip
import zlib
import struct
import sys
from optparse import OptionParser

class Point:
  longitude = 0.0
  latitude = 0.0
  
class Trip:
  name = ''
  start_point = Point()
  end_point = Point()
  path_list = None # list cannot be initialized here!
  path_color = ''
  Trip_index = 0
  
def traverseFolder(directory, suffix, number):
    fileList = []
    for file in os.listdir(directory):
        if os.path.isdir(directory + file): # if current path is still the folder, then get into it
            thisPath = directory + file + '/'
            fileList = fileList+traverseFolder(thisPath, suffix)
        elif file.endswith(suffix):
            fileName = directory + file
            fileList.append(fileName)
            if len(fileList) >= number:
              break
    return fileList

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict
  
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
	  
def draw_trips(directory, outputpath, number):
  filelist = traverseFolder(directory, '.mat', number)
  print(filelist)
  
  make_sure_path_exists(outputpath)
  
  color_list = ['Aqua',
    'Alizarin crimson',
    'Amber',
    'Amethyst',
    'Android Green',
    'Azure',
    'Deep pink',
    'Magenta']
  
  color_dictionary = {'Aqua':       "#00ffff",
          'Alizarin crimson': "#e32636",
          'Amber':      "#ffbf00",
          'Amethyst':   "#9966cc",
          'Android Green':    "#a4c639",
          'Azure':      "#007fff",
          'Deep pink':    "#ff1493",
          'Magenta':	"#f00ff"
      }
  
  start_color = "#0000FF"
  end_color = "#FF0000"
  
  index = 0
  Trip_list = []
  
  for file in filelist:
    Trip_data = load_mat_file(file) # load origin .mat data
    point_list = extract_points_location(Trip_data)
    
    trip = Trip()
    trip.name = file
    trip.start_point = point_list[0]
    trip.end_point = point_list[-1]
    trip.Trip_index = index
    trip.path_list = []
    trip.path_color = color_list[index]
    
    for i in point_list:
      trip.path_list.append(tuple([i.latitude, i.longitude]))

    # draw start point, end point, route_path
    mymap = pygmaps.maps(trip.start_point.latitude, trip.start_point.longitude, 12) # start a map
    mymap.addpoint(trip.start_point.latitude, trip.start_point.longitude, start_color)
    mymap.addpoint(trip.end_point.latitude, trip.end_point.longitude, end_color)
    mymap.addpath(trip.path_list, color_dictionary[trip.path_color])
    index = index + 1
    
    map_path = outputpath + file.split("/")[-1][:-4] + '.map.draw.html'  # delete the '.mat' and add '.map.draw.html'
    mymap.draw(map_path)
    url = map_path
    webbrowser.open_new_tab(url)
    Trip_list.append(trip)

def load_mat_file (filepath):
  structure_data = loadmat(filepath)
  Trip_data = structure_data['trip']
  return Trip_data

# extract data of each point
def extract_points_location (Trip_data):
  Location = Trip_data['Location']
  Latitude = Location['Latitude']
  Longitude = Trip_data['Location']['Longitude']

  point_list = []
  for i in range(1, len(Latitude)):
    new_point = Point()
    new_point.latitude = Latitude[i]
    new_point.longitude = Longitude[i]
    point_list.append(new_point)
  return point_list

def main(): 
    parser = OptionParser(usage = "usage: %prog [-b] arg1 [-n] arg2", version = "%prog 1.0")
    parser.add_option("-d", "--directory", action="store", dest="directory",
          default='../test_data/SOSD1/',
          help="set directory path of trips .mat files.")
    parser.add_option("-n", "--number", action="store", dest="number",
          default=10,
                      help="Choose how many trips you want to draw")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    parser.add_option("-o", "--output", action="store", dest="outputpath",
          default='./output/trips/',
          help="output path.")
    (options, args) = parser.parse_args()
    # print options
    # print args
    # if len(options) < 3:
        # parser.error("incorrect number of arguments")
    if options.verbose:
        print "unzip all .gz files in %s..., and extract them in the same folder hierachy in %s" % (options.directory, options.number)
    
    draw_trips(options.directory, options.outputpath, 8)
    
if __name__ == '__main__':
  main()
