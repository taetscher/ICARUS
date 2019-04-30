from darkflow.net.build import TFNet
import cv2
import os

n = 0

img_folder = "icarusVALIDATION/validationImages/validation/"
file_list = os.listdir(img_folder)

#setting up YOLO
options = {"model": "cfg/tiny-yolo-ICARUS.cfg", "load": 21000, "threshold": 0.5}
tfnet = TFNet(options)

#running validation
for number in range(0, len(file_list)):
    photo_name = str(file_list[n])
    file_path = img_folder + photo_name
    print(file_path)

    # load image
    imgcv = cv2.imread(file_path)

    # predict labels of objects in image
    result = tfnet.return_predict(imgcv)

    # outputs a list of dictionaries, each dictionary representing a detected object
    print(result)

    n += 1




