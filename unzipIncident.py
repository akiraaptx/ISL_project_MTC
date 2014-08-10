import os
import gzip
import zlib
import struct
import sys
from optparse import OptionParser

def unzipIncident(basePath, destPath):
    # DSTdates = getRecentDSTdates()
    if not os.path.exists(basePath):
      print "Error: basepath %s doesn't exist" % basePath
      sys.exit(-1)
    if not os.path.exists(destPath):
      try:
	os.makedirs(destPath)
      except OSError:
	if not os.path.isdir(path):
	  raise
    
    global count
    count = 0
    print("Start Generating FileList ...")
    fileList = traverseFolder(basePath, '.gz')	# get filelist containing all files in the basePath
    print("FileList Generation Completed!")
    print("There are " + str(count) + " files in total.")
    
    for file in fileList:
	filepath = destPath + file[len(basePath):-3]
        if not os.path.exists(filepath):	# if the file has already been unzipped, do nothing here
	  try:
	    thisFile = gzip.GzipFile(fileobj=open(file, 'rb'))
	    # thisFile = open(file, 'rb')
	    data = thisFile.read()
	    dataStr = str(data)
	    try:
	      output = open(filepath, 'w+')
	    except IOError:
	      # If not exists, create the file
	      os.makedirs(os.path.dirname(filepath))
	      output = open(filepath, 'w+')
	    output.write(dataStr)
	    output.close()
	    print("file: " + filepath + " has been created.")
	      # output.write(dataStr)
	  except (struct.error, zlib.error, OSError) as e:	# need explain
	    pass
    	else: 
	  print("file: " + filepath + " already exists")
	  continue 
    print("Unzip .gz files to xml Completed.")

def traverseFolder(basePath, suffix):
    # print(basePath)
    # os.chdir(basePath)
    fileList = []
    for file in os.listdir(basePath):
	# print (basePath+file)
        if os.path.isdir(basePath+file): # if current path is still the folder, then get into it
            thisPath = basePath+file+'/'
            fileList = fileList+traverseFolder(thisPath, suffix)
        elif file.endswith(suffix):
	    global count
	    count = count + 1
            fileName = basePath+file
            fileList.append(fileName)
    return fileList

def main(): 
    parser = OptionParser(usage = "usage: %prog [-b] arg1 [-d] arg2", version = "%prog 1.0")
    parser.add_option("-b", "--basepath", action="store", dest="basepath",
		      default='/media/mayuanakira/Seagate Fast HDD Drive/Mobility_Data_Mining/origin_data/',
		      help="set BASEPATH of the zipped files.")
    parser.add_option("-d", "--destpath", action="store", dest="destpath",
		      default='/media/mayuanakira/Seagate Fast HDD Drive/Mobility_Data_Mining/unzip_data/',
                      help="set DESTPATH of the zipped files.")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    # print options
    # print args
    # if len(options) < 3:
        # parser.error("incorrect number of arguments")
    if options.verbose:
        print "unzip all .gz files in %s..., and extract them in the same folder hierachy in %s" % (options.basepath, options.destpath)
    
    unzipIncident(options.basepath, options.destpath)
    
if __name__ == '__main__':
  main()

