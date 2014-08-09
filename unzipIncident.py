import os
import gzip
import zlib
import struct

def unzipIncident():
    basePath = '/media/mayuanakira/Seagate Fast HDD Drive/Mobility_Data_Mining/origin_data/'	# the basePath is the path where you data folder is
    # DSTdates = getRecentDSTdates()
    destPath = '/media/mayuanakira/Seagate Fast HDD Drive/Mobility_Data_Mining/unzip_data/'
    if not os.path.exists(destPath): os.makedirs(destPath)
    
    global count
    count = 0
    print("Start Generating FileList ...")
    fileList = traverseFolder(basePath, '.gz')	# get filelist containing all files in the basePath
    print("FileList Generation Completed!")
    print("There are " + str(count) + " files in total.")
    
    for file in fileList:
        try:
            thisFile = gzip.GzipFile(fileobj=open(file, 'rb'))
            # thisFile = open(file, 'rb')
            data = thisFile.read()
            dataStr = str(data)
            filepath = destPath + file[len(basePath):-3]
            if not os.path.exists(filepath):	# if the file has already been unzipped, do nothing here
	      try:
		output = open(filepath, 'w+')
	      except IOError:
		# If not exists, create the file
		os.makedirs(os.path.dirname(filepath))
		output = open(filepath, 'w+')
	      output.write(dataStr)
	      output.close()
	      print("file: " + filepath + "has been created.")
	      # output.write(dataStr)
	    else: 
	      #print("file: " + filepath + " already exists")
	      continue 
        except (struct.error, zlib.error, OSError) as e:	# need explain
            pass
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

if __name__ == '__main__':
    unzipIncident()
