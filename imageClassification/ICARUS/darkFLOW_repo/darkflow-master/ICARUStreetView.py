import json
from datetime import datetime

import cv2
import google_streetview.api as streetview
import numpy as np

from darkflow.net.build import TFNet

#setting up API key import from different folder
with open('icarustreetview_OUTPUT/APIkey.txt', 'r') as file:
  content = file.read()
  key = str(content)
  file.close()

#taking time
start = datetime.now()

#-----------------------SETTING PARAMETERS--------------------
#Enter NW corner of quadrant
lat = 9.962211
lng = 79.436732

#Enter SE corner of quadrant
lat_stop = 5.888902
lng_stop = 81.992929

#specify step
lat_step = 1
lng_step = 1
total_steps = int(np.rint(((lat - lat_stop) / lat_step) * ((lng_stop - lng) / lng_step)))
print('Program will assess around {} points.'.format(total_steps))
print('Running ICARUStreetview with these input parameters will take about ', np.rint(total_steps/60*0.5),' minutes (or ', np.rint(total_steps/60/60*0.5),' hours, or ', np.rint(total_steps/60/60/24*0.5), ' days).')

#Streetview API Parameters:
fov = 120
pitch = 0
radius = 25
source = 'outdoor'
streetview_params = {"fov": fov,
           "pitch": pitch,
           "radius": 25, "source": source
           }

#savefile name:
s_file = 'streets_' + str(datetime.now())[0:10] + '.csv'
s_file_path = 'icarustreetview_OUTPUT/' + str(s_file)
assess_file_path = 'icarustreetview_OUTPUT/assessed_' + str(datetime.now())[0:10] + '.csv'
metadata_file_path = 'icarustreetview_OUTPUT/metadata_' + str(datetime.now())[0:10] + '.txt'

#setting up csv headers to:
with open(assess_file_path, 'a') as assess_file:
    assess_file.write('\n' + 'coord_x_lng, coord_y_lat' + '\n')
    print('setting up savefile for all assessed points...')
    assess_file.close()

with open(s_file_path, 'a') as savefile:
    savefile.write('\ncoord_x_lng, coord_y_lat, timestamp, avr_confidence, UUID\n')

#setting up yolo
options = {"model": "cfg/tiny-yolo-ICARUS.cfg",
           "load": 20000,
           "threshold": 0.1
           }
#-------------------------------------------------------------

# setting up the tensorflow net for yolo
tfnet = TFNet(options)
print('---------' * 10)

# setting up program statistics
#all points that will be assessed
n = 0
#streets that were found during assessment
m = 0


i = lat
i_stop = lat_stop

#--------------------------------MAIN LOOP STARTS HERE-----------------------------------------------
while i_stop < i:
    #watch out, depending on your location on the globe this condition changes (adding or subtracting to move along)

    j = lng
    j_stop = lng_stop

    while j < j_stop:

        location = str(i) + ',' + str(j)
        print('Currently assessing location: ', str(str(i) + ',' + str(j)))
        with open(assess_file_path, 'a') as assess_file:
            assess_file.write(str(j) + ', ' + str(i) +'\n')
            assess_file.close()

        # Define parameters for street view api
        params = [{
                'size': '640x640',  # max 640x640 pixels
                'location': location,
                'fov': fov,
                'pitch': pitch,
                'radius': radius,
                'source': source,
                'key': key
            }]

        # Create a results object
        results = streetview.results(params)
        # Download images to directory 'downloads'
        results.download_links('icarustreetview_OUTPUT/temp')

        j_file = open('icarustreetview_OUTPUT/temp/metadata.json').read()
        metadata = json.loads(j_file)[0]

        status = metadata['status']
        print('API response for status: status == {}'.format(status))

        try:
            pano_id = metadata['pano_id']

            if status == 'OK':
                print('metadata: OK')
                picturepath = 'icarustreetview_OUTPUT/temp/' + metadata['_file']

                # read image date into cv2
                imgcv = cv2.imread(picturepath)

                # predict labels of objects in image
                result = tfnet.return_predict(imgcv)

                if len(result) > 0:
                    # prepare yolo output to be saved in csv
                    a = range(0, len(result))
                    confidence_list = []
                    for element in a:
                        confidence = result[element]['confidence']
                        confidence_list.append(confidence)

                    avr_confidence = np.mean(confidence_list)

                    with open(s_file_path, 'a') as savefile:
                        # save results to csv file
                        print('saving...')
                        savefile.write('{}, {}, {}, {}, {}\n'.format(metadata['location']['lng'], metadata['location']['lat'], datetime.now(), avr_confidence, pano_id))
                        savefile.close()

                    print('done, location saved to ' + s_file_path + '\n' + '--' * 20)
                    m += 1

                else:
                    print('No all-season Road detected.')
                    pass

        except:
            if KeyError:
                print('Key Error (Requested Position not contained in Metadata, either "Pano_ID" or "Status")')
            elif FileNotFoundError:
                print('No savefile exists yet')
            pass

        #counter increases
        n += 1


        # watch out for plus or minus sign here, always double check if the program
        # loops the correct way through
        j += lng_step
    i -= lat_step
#--------------------------------MAIN LOOP ENDS HERE-------------------------------------------------

with open(metadata_file_path, 'a') as meta:
    meta.write('\nDatetime: '+str(start))
    meta.write('\nAssessed Points: ' + str(n))
    meta.write('\nFound Streets: ' + str(m))
    meta.write('\nTFNet options: ' + str(options))
    meta.write('\nBounding polygon (lat/long, lat_stop/long_stop: ' + str(lat) + ', ' + str(lng) + ', ' + str(lat_stop) + ', ' + str(lng_stop))
    meta.write('\nLat/Lng Step: ' + str(lat_step) + ', ' + str(lng_step))
    meta.write('\nStreetView API Parameters: ' + str(streetview_params))
    meta.close()

print('\n\n', '--' * 20)
print('ICARUStreetView is done. time elapsed: {}, Points analysed: {}'.format(datetime.now()-start, n))
print('--' * 20)
print('Assessed {} Points, found {} "all Season Roads".'.format(n, m))
print('--' * 20)
print('Program ran with the following Streetview-API parameters:'
      '\nNW Corner: lat_start = {}, lng_start = {}\nSE Corner: lat_stop = {}, lng_stop = {}\n'
      'lat step = {}, lng_step = {}\n'
      'fov = {}, pitch = {}, radius = {}'.format(lat, lat_stop, lng, lng_stop, lat_step, lng_step, fov, pitch, radius))
print('--'*20)
print('YOLO-Parameters used:\n', options)