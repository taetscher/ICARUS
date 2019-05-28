from darkflow.net.build import TFNet
import cv2
import os
from datetime import datetime
import numpy as np

# set up global variables
t = 0
detect = 0
start = datetime.now()
confidence_list = []

# choose validation data here (give folder path, where inside the folder images are saved as .jpg)
img_folder = "icarusVALIDATION/validationImages/validation/"
file_list = os.listdir(img_folder)




#setting up YOLO
options = {"model": "cfg/tiny-yolo-ICARUSv2.cfg", "load": 142750, "threshold": 0.5, 'gpu': 0.75}
tfnet = TFNet(options)

print("Running validation of ICARUS...")

#running validation
for number in file_list:
    photo_name = str(file_list[t])
    file_path = img_folder + photo_name
    print("Assessing: ", file_path[-10:])

    # load image
    imgcv = cv2.imread(file_path)

    # predict labels of objects in image
    result = tfnet.return_predict(imgcv)

    if len(result) > 0:
        detect += 1

        # get confidence and append to confidence list for statistics
        a = range(0, len(result))
        for element in a:
            confidence = result[element]['confidence']
            confidence_list.append(confidence)


    else:
        # if ICARUS did not find anything, continue to the next image
        pass

    # outputs a list of dictionaries, each dictionary representing a detected object
    #print(result)

    t += 1

# perpare validation statistics
stop = datetime.now()
n = len(file_list)
percentage = 100*(detect/n)
avr_confidence = np.mean(confidence_list)
med_confidence = np.median(confidence_list)

# save validation statistics
with open("icarusVALIDATION/validationStatistics.txt",'a') as logger:
    logger.write("-"*90)
    logger.write("\nNEW RUN at {}\n".format(datetime.now()))
    logger.write("-" * 90)
    logger.write("\nTesting Dataset: {}\n".format(img_folder))
    logger.write("-" * (17 + len(img_folder)))
    logger.write("\nICARUS running with the following options")
    logger.write("\nYOLO-Options: {}".format(options))
    logger.write("\nNumber of Images assessed: {}".format(n))
    logger.write("\nAllSeasonRoads detected: {}, as percentage: {}%".format(detect,percentage))
    logger.write("\nAverage confidence: {}".format(avr_confidence))
    logger.write("\nMedian confidence: {}".format(med_confidence))
    logger.write("\nDuration: [HH:MM:SS.MS] {}\n".format(stop-start))
    logger.write("-" * 90)
    logger.write("\n\n\n")
    logger.close()

print("\n\nValidation of ICARUS finished, check icarusVALIDATION/validationStatistics.txt for results")



