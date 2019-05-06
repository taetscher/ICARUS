import cv2
import matplotlib.pyplot as plt
import requests

"""This Program can be used to visually verfy results of ICARUS, inspired by Mark Jay"""

# Set up and prepare infile read
folder_path = "icarusOUTPUT/ICARUS1/"
infile_name = "georefMediaTweets2019-05-03.csv"
in_file = folder_path + infile_name

# set up threshold for conficence
tresh = 0.8

#Viewer magic
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
            result = eval(array[5])


            # generate list of confidence probabilities that are above threshhold set in the beginning
            index_list = []
            for n in range(0,len(result)):
                conf = result[n]['confidence']

                if conf > tresh:
                    index_list.append(n)

                else:
                    pass

            # if any entry of result['confidence'] exceeds thresh, draw bboxes and show image.
            if len(index_list) > 0:
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

                    for x in range(0, len(index_list)):
                        # get parameters that you need to display image
                        tl = result[x]['topleft']['x'], result[x]['topleft']['y']
                        br = result[x]['bottomright']['x'], result[x]['bottomright']['y']
                        confidence = result[x]['confidence']
                        label = "ASR: " + str(confidence)[:4]

                        # prepare display of text
                        fontface = cv2.FONT_HERSHEY_PLAIN
                        fontscale = 2
                        thickness = 2
                        predict_color = (0, 255, 0)
                        predict_thickness = 3
                        font_color = (255, 255, 255)
                        background_color = (0, 0, 0)

                        label_size = cv2.getTextSize(label, fontface, fontscale, thickness)

                        # determine where to put label
                        height, width = img.shape[:2]
                        print(height, width)

                        if tl[0] > width / 2:
                            # put label left of predict if it were off-screen otherwise
                            text_width = label_size[0][0]
                            text_height = label_size[0][1] + 5

                            label_tl = (tl[0] - text_width, tl[1] - 10)
                            label_br = (label_tl[0] + text_width, label_tl[1] - text_height)


                        else:
                            # put label on top of predict for all other cases
                            text_width = label_size[0][0]
                            text_height = label_size[0][1] + 5

                            label_tl = (tl[0], tl[1] - 10)
                            label_br = (label_tl[0] + text_width, label_tl[1] - text_height)

                        # draw rectangle for prediction
                        img = cv2.rectangle(img, tl, br, predict_color, predict_thickness)
                        # draw background for label
                        img = cv2.rectangle(img, label_tl, label_br, background_color, -1)
                        # draw label
                        img = cv2.putText(img, label, label_tl, fontface, fontscale, font_color, thickness)

                    # make plt show the image fullscreen
                    mng = plt.get_current_fig_manager()
                    mng.window.state('zoomed')
                    plt.imshow(img)
                    plt.show()

                except:
                    pass



            else:
                pass




        except:
            pass

        line = fp.readline()

