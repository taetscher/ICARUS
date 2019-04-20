from darkflow.net.build import TFNet
import cv2
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime
import uuid
import requests
import numpy as np

# -----------------------------------System Parameters Definition & Setup---------------------------------------
# importing authorization credentials from different file
autho_path = r'Authentication.txt'
authorization = eval(open(autho_path).read())

# applying credentials as consumer key, consumer secret, access token, access secret.
ckey = authorization['ckey']
csecret = authorization['csecret']
atoken = authorization['atoken']
asecret = authorization['asecret']

''' 
The following (options) is a dictionary that sets up yolo. change this to change what kind of pretrained model to use. 
[model] is a parameter that specifies which model to use like folder/model.cfg 
[load] is used to load predefined weights like bin/weights.weights 
[threshold] specifies the minimal confidence factor yolo needs to draw a bounding box 
'''
options = {"model": "cfg/tiny-yolo-ICARUS.cfg",
           "load": 20000,
           "threshold": 0.5
           }

# setting up the tensorflow net
tfnet = TFNet(options)
print('---------' * 10)

# mapping (output) savefiles
mapping_file_path = r'icarustream_OUTPUT/icarustreamOUTPUT.csv'
geo_media_tweet = r'icarustream_OUTPUT/georefMediaTweets.csv'

# write new section into output csv file
with open(geo_media_tweet, 'a') as gmt:
    # header = 'Indicator for new Run, timestamp, yolo parameters'
    gmt.write("\n\n\n\n{}{}\n".format("NEW RUN -------------------------\n",datetime.now()q))
    gmt.write("{}{}".format("header = 'coord_x, coord_y, link, timestamp, UUID'\n","---------------------------------\n\n"))
    gmt.close()

# write new section into output csv file
with open(mapping_file_path, 'a') as mapping:
    # header = 'Indicator for new Run, timestamp, yolo parameters'
    mapping.write("\n\n\n\n{}{}, {}\n".format("NEW RUN -------------------------\n",datetime.now(), options))
    mapping.write("{}{}".format("header = 'coord_x, coord_y, link, timestamp, UUID, average_confidence, confidence_list'\n","---------------------------------\n\n"))
    mapping.close()

# -------------------------------------------------------------------------------------------

class listener(StreamListener):
    def on_data(self, data):
        """Function that does all the work, handles the individually downloaded tweets,
        First checks if tweet has coordinates appended to it, then checks if tweet has media
        attached to it. If both is True, passes it through YOLO Image Classifier ICARUS and
        saves Metadata of tweet in a separate .txt file."""

        try:
            #get data from twitter stream
            tweet = json.loads(data)
            indi_id = uuid.uuid1()

            # get coordinates from data
            xyz = tweet['coordinates']  # Watch out, Coordinates are Saved as follows: xxx w, yyyy n

            if xyz == None:
                # Check if tweet has coordinates appended, if not return True and go to next Tweet
                print('no coordinates appended to tweet')
                return True
            else:
                # if tweet has coordinates, save to database,
                # otherwise the program gives error 'failed onData',
                # 'NoneType' object has no attribute 'get'
                enti = tweet.get('extended_entities')

                # from here, go to 'media'
                med = enti.get('media')
                med2 = med[0]
                medurl = med2.get('media_url')

                try:
                    # download the image, save it temporarily to pass it on to yolo
                    img_data = requests.get(medurl).content
                    temp_name = 'temp_img'
                    with open('images/temp/' + temp_name, 'wb') as handler:
                        # save image data from URL
                        handler.write(img_data)
                        print('ICARUS passing image...')

                    # write down tweet was georeferenced and had media appended
                    with open(geo_media_tweet, 'a') as gmt:
                        # header = 'coord_x, coord_y, link, timestamp, UUID'
                        gmt.write("{}, {}, {}, {}\n".format(str(xyz)[34:-2], medurl, datetime.now(), indi_id))
                        gmt.close()

                    # read image data into cv2
                    imgcv = cv2.imread('images/temp/' + temp_name)

                    # predict labels of objects in image
                    result = tfnet.return_predict(imgcv)

                    if len(result) > 0:
                        print('Well Done ##########################################')

                        # prepare yolo output to be saved in csv
                        a = range(0, len(result))
                        confidence_list = []
                        for element in a:
                            confidence = result[element]['confidence']
                            confidence_list.append(confidence)

                        avr_confidence = np.mean(confidence_list)

                        # basically, if anything was detected (if any all_Season_Roads were found), save data
                        with open(mapping_file_path, 'a') as mapping:
                            # save in csv format in order to import to GIS
                            # header = 'coord_x, coord_y, link, timestamp, UUID, average_confidence, confidence_list'
                            mapping.write("{}, {}, {}, {}, {}, {}\n".format(str(xyz)[34:-2], medurl, datetime.now(), indi_id, avr_confidence, str(confidence_list).strip('[').strip(']') ))
                            mapping.close()

                            print('---' * 10,
                                  '\nFACK YES YOU LEGEND!\nIMAGE DID CONTAIN ALLSEASON ROAD AND WAS SAVED TO icarustreamOUTPUT.CSV\n',
                                  '---' * 10)

                    else:
                        #elso continue to the next tweet
                        print('yolo did not see stuff')
                        pass

                except AssertionError:
                    # this catches errors of type 'image is not of type np.ndarray'
                    print('---AssertionError---\n#NumPy Fuckup\n--------------------')
                    pass

                return True

        except BaseException as e:
            print('failed onData, ', str(e))
            # time.sleep(1)

    def on_error(self, status):
        print(status)

''' 
change arguments of twitterStream.filter() to change what tweets to filter out: 
filter for keywords: track=['keyword'] 
filter for location: locations=[-180,-90,180,90] (covers the whole world, but excludes simultaneous use of 'track') 

location format: Each bounding box should be specified as a pair of longitude and latitude pairs, 
with the SW corner of the bounding box coming first, then the NE corner 
for example: -122.75,36.8,-121.75,37.8  San Francisco 

Watch out if you use Google Maps to set a bounding Polygon, as GMaps puts its coordinates in latitude/longitude pairs. 
You may need to adjust the format when trying to use this data in a GIS. 
It (GMaps) uses the WGS 84 Coordinate System and a Web Mercator Projection (WGS 84 Web Mercator, ) 


some bounding polygons of locations to track: 
    [28.645576, -26.599086, 57.700704, 16.518278] tracks eastern subsaharan Africa 
    [-95.295220, -55.085423, -32.204602, 18.638551] tracks the whole of South America 
    [65.601803, -15.131681, 167.369445, 53.424227] tracks South-Eastern Asia and Papua New Guinea 
    [-180,-90,180,90] tracks the whole world 

Coordinate System I use to display this stuff in ArcGIS:
    GCS_WGS_1984
    WKID: 4326 Authority: EPSG

    Angular Unit: Degree (0.0174532925199433)
    Prime Meridian: Greenwich (0.0)
    Datum: D_WGS_1984
    Spheroid: WGS_1984
        Semimajor Axis: 6378137.0
        Semiminor Axis: 6356752.314245179
        Inverse Flattening: 298.257223563
'''

# -------------------------------Let Her Rip---------------------------------
# set twitter authentication parameters
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

while True:
    # Keep the program going. Straight up just pass on errors, lol.
    try:
        twitterStream.filter(locations=[-180, -90, 180, 90])
    except:
        # this could use some more sophisticated form of error-handling.
        pass
# -------------------------------she ripped...-------------------------------