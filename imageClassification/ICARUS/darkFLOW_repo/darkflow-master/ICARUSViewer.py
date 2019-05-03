import cv2
import matplotlib.pyplot as plt
import requests

"""This Program can be used to visually verfy results of ICARUS, inspired by Mark Jay"""

folder_path = "icarusOUTPUT/"
infile_name = "georefMediaTweets2019-05-03.csv"

in_file = folder_path + infile_name


with open(in_file) as fp:
    line = fp.readline()

    while line:
        try:
            # read in lines as arrays
            array = line.split("; ")


            # extract coordinate information (lat/long), link to media, timestamp, uuid
            coord_x = array[0]
            coord_y = array[1]
            medurl = array[2]
            timestamp = array[3]
            avr_confidence = array[4]
            result = array[5]

            tl = (eval(result)[0]['topleft']['x'], eval(result)[0]['topleft']['y'])
            br = (eval(result)[0]['bottomright']['x'], eval(result)[0]['bottomright']['y'])
            label = eval(result)[0]['label']

            print("Avr. confidence: ", avr_confidenceq)

            # download image, if this fails, go with next one
            try:
                img_data = requests.get(medurl).content
                temp_name = 'temp_img.jpg'

                with open('images/temp/' + temp_name, 'wb') as handler:
                    # save image data from URL
                    handler.write(img_data)
                    handler.close()

                # pass image to yolo
                img = cv2.imread('images/temp/' + temp_name)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                img = cv2.rectangle(img, tl, br, (0, 255, 0), 7)
                img = cv2.putText(img, "ASR", tl, cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 0), 2)

                plt.imshow(img)
                plt.show()

            except:
                pass

        except:
            pass

        line = fp.readline()

