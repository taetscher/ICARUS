#----------------------------------------------------------------------------------------------------------------------
# Authentication Information: set environment Variable as follows
# GOOGLE_APPLICATION_CREDENTIALS = 'E:\Local_Repositories\Masters_Thesis_Repo\Master Thesis-7ba88bc81b55.json'
# ---------------------------------------------------------------------------------------------------------------------

import requests
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

k = 0

with open(r'E:\Local_Repositories\Masters_Thesis_Repo\twitterStream\GEOsaveFile.txt') as f:
    #each line in the GeoSaveFile represents an entry of a tweet with annexed picture
    #read each line, download the image, then send it to googleCloudVision and save if it has a
    #road in it
    for line in f:
        k += 1

        try:
            # Read list from saveFile.txt, prepare data and select URL
            x = line.split(';')
            url = x[1]
            url = url[2:-1]

            # Get uuID
            ID = x[3]

            # give user indication that program is working
            print('_'*20 ,'\n\nASSESSING IMAGE {}'.format(k), '  URL:', url, '   UUID:', ID)

            # get image data from URL, assing content
            content = requests.get(url).content
            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            print('GCV_API call... \n')
            print('Labels:\n')

            # adds the lables to a list
            labellist = []
            for label in labels:
                labellist.append(str(label.description))

            print(labellist, '\n')

            #creates list with labels that we look for
            findList = ['road', 'asphalt', 'concrete', 'street', 'pathway', 'highway', 'lane', 'road surface']

            if any(i in labellist for i in findList):

                # hier auch noch aufnehmen: asphalt, road surface, lane, highway, street
                # if any are in labellist, save image as follows:

                with open(str(ID) + '.jpg', 'wb') as handler:
                    # save image data from URL
                    handler.write(content)
                    print('Image saved.', '\n')
                    print('_' * 20)
            else:
                print('Image did not contain keywords in findList, was not saved')
                print('_'*20)
                pass
        except:
            # this could use some more sophisticated form of error handling
            pass