import csv
import sys
import xml.etree.ElementTree as etree

if __name__ == "__main__":

    file_name = sys.argv[1]
    csv_file_name = '.'.join(file_name.split('.')[:-1]) + ".csv"
    column_names = ['TRAFFIC_INCIDENTS_TIMESTAMP',
		    'TRAFFIC_ITEM_ID',
		    'ORIGINAL_TRAFFIC_ITEM_ID',
		    'TRAFFIC_ITEM_STATUS_SHORT_DESC',
		    'TRAFFIC_ITEM_TYPE_DESC',
		    'START_TIME',
		    'END_TIME',
		    'ENTRY_TIME',
		    'CRITICALITY_ID',
		    'CRITICALITY_DESCRIPTION',
		    'VERIFIED',
		    'LOCATION_LATITUDE',
		    'LOCATION_LONGITUDE']
    
    
    root = etree.parse(file_name).getroot()
    
    with open(csv_file_name, 'w') as file_:

        writer = csv.writer(file_, delimiter=",")
        writer.writerow(column_names)

        for a in zip(root.findall(".//TRAFFIC_ITEM_ID"),
                     root.findall(".//ORIGINAL_TRAFFIC_ITEM_ID"),
                     root.findall(".//TRAFFIC_ITEM_STATUS_SHORT_DESC"),
                     root.findall(".//TRAFFIC_ITEM_TYPE_DESC"),
                     root.findall(".//START_TIME"),
                     root.findall(".//END_TIME"),
                     root.findall(".//ENTRY_TIME"),
                     root.findall(".//CRITICALITY/ID"),
                     root.findall(".//CRITICALITY/DESCRIPTION"),
                     root.findall(".//VERIFIED"),
                     root.findall(".//LOCATION/GEOLOC/ORIGIN/LATITUDE"),
                     root.findall(".//LOCATION/GEOLOC/ORIGIN/LONGITUDE")):
	    incident_tuple = [root.attrib["TIMESTAMP"]]
	    for x in a:
	      incident_tuple.append(x.text)
	    # print(incident_tuple)
            writer.writerow(incident_tuple)

