from darkflow.net.build import TFNet
import cv2
import matplotlib.pyplot as plt
import requests
import numpy as np
import os


def saver(in_file, thresh, checkpt):
    # Viewer magic
    t=0

    with open(in_file) as fp:
        line = fp.readline()

        while line:
            try:
                # read in lines as arrays
                array = line.split("; ")
                print(array)

                # extract coordinate information (lat/long), link to media, timestamp, uuid
                img_name = array[0]
                result = eval(array[2])

                # generate list of confidence probabilities that are above threshhold set in the beginning
                index_list = []
                for n in range(0, len(result)):
                    conf = result[n]['confidence']

                    if conf > thresh:
                        index_list.append(n)

                    else:
                        # print("fail")
                        pass

                # if any entry of result['confidence'] exceeds thresh, draw bboxes and show image.
                if len(index_list) > 0:
                    # download image, if this fails, go with next one
                    try:
                        img = cv2.imread('icarusValidation/validationImages/batch26/' + str(img_name))

                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        for x in index_list:
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

                        # save the image with annotation for easy looking looking
                        plt.imsave("icarusTESTING/output_ckpt_{}/{}".format(checkpt, img_name), img)
                        t+=1

                    except:
                        # print("fail2")
                        pass

                else:
                    # print("fail3")
                    pass

            except:
                # print("fail4")
                pass

            line = fp.readline()

def testingICARUS(ckpt_dir):

    ckptfile_list = os.listdir(ckpt_dir)

    #remove the first entry of the list, which is a checkpoint summary file
    ckptfile_list.remove(ckptfile_list[0])

    ckpt_numbers = []

    for element in ckptfile_list:
        #get checkpoint number from list
        element = element.split(".")
        element = element[0].split("-")
        ckpt_numbers.append(element[3])

    #remove duplicate entries
    ckpt_list = set(ckpt_numbers)

    print(ckpt_list)

    for checkpoint in ckpt_list:
        save_dir = 'icarusTESTING/output_ckpt_{}'.format(checkpoint)
        os.mkdir(save_dir)

        ''' 
        The following (options) is a dictionary that sets up yolo. change this to change what kind of pretrained model to use. 
        [model] is a parameter that specifies which model to use like folder/model.cfg 
        [load] is used to load predefined weights like bin/weights.weights 
        [threshold] specifies the minimal confidence factor yolo needs to draw a bounding box 
        '''
        options = {"model": "cfg/tiny-yolo-ICARUSv2.cfg",
                   "load": int(checkpoint),
                   "threshold": 0.5
                   }

        # setting up the tensorflow net
        tfnet = TFNet(options)
        print('---------' * 10)

        # pass image to yolo
        pic_list = os.listdir('icarusVALIDATION/validationImages/batch26/')
        print(pic_list)

        for picture in pic_list:
            imgcv = cv2.imread('icarusVALIDATION/validationImages/batch26/' + str(picture))

            # assess image with yolo
            result = tfnet.return_predict(imgcv)
            print(result)

            if len(result) > 0:

                # prepare yolo output to be saved in csv
                a = range(0, len(result))
                confidence_list = []
                for element in a:
                    confidence = result[element]['confidence']
                    confidence_list.append(confidence)

                avr_confidence = np.mean(confidence_list)

                # basically, if anything was detected (if any all_Season_Roads were found), save data
                with open("icarusTESTING/{}_{}.csv".format(checkpoint, "output"), 'a') as outfile:
                    outfile.write(
                        "{}; {}; {}\n".format(str(picture), avr_confidence, result))

            else:
                # elso continue to the next tweet
                pass

        saver("icarusTESTING/{}_{}.csv".format(checkpoint, "output"), 0.5, checkpoint)





testingICARUS("ckpt")