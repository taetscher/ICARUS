from darkflow.net.build import TFNet
import cv2
import os
from datetime import datetime

t = 0
detect = 0
start = datetime.now()

img_folder = "icarusVALIDATION/validationImages/validation/"
file_list = os.listdir(img_folder)



#setting up YOLO
options = {"model": "cfg/tiny-yolo-ICARUS.cfg", "load": 21000, "threshold": 0.5}
tfnet = TFNet(options)

print("Running validation of ICARUS...")
#running validation
for number in range(0, len(file_list)):
    photo_name = str(file_list[t])
    file_path = img_folder + photo_name
    print("Assessing: ", file_path[-10:])

    # load image
    imgcv = cv2.imread(file_path)

    # predict labels of objects in image
    result = tfnet.return_predict(imgcv)

    if len(result) > 0:
        print("this would have been saved\n")
        detect += 1


    else:
        # elso continue to the next tweet
        print('No Detection\n')
        pass





    # outputs a list of dictionaries, each dictionary representing a detected object
    #print(result)

    t += 1


# perpare validation statistics
stop = datetime.now()
n = len(file_list)
percentage = 100*(detect/n)

# save validation statistics
with open("icarusVALIDATION/validationStatistics.txt",'a') as logger:
    logger.write("-"*90)
    logger.write("\nNEW RUN at {}\n".format(datetime.now()))
    logger.write("-" * 90)
    logger.write("\nTesting Dataset: {}\n".format(img_folder))
    logger.write("-" * 62)
    logger.write("\nICARUS running with the following options")
    logger.write("\nOptions: {}".format(options))
    logger.write("\nImages assessed: {}".format(n))
    logger.write("\nAllSeasonRoads detected: {}, as percentage: {}%".format(detect,percentage))
    logger.write("\nDuration: [HH:MM:SS.MS] {}\n".format(stop-start))
    logger.write("-" * 90)
    logger.write("\n\n\n")
    logger.close()

print("Validation of ICARUS finished, check icarusVALIDATION/validationStatistics.txt for results")
print("length image folder path", len(img_folder))




