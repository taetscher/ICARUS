from darkflow.net.build import TFNet
import cv2
import os



#yolo setup
options = {"model": "cfg/tiny-yolo-ICARUS.cfg", "load": 21000, "threshold": 0.5, "gpu": 0.6}
tfnet = TFNet(options)


folder = "test/training/images/"

file_list = os.listdir(folder)



for n in file_list:

    # load image

    image = cv2.imread(folder + n)
    result = tfnet.return_predict(image)

    with open("icarustestOUTPUT.txt", 'a') as logger:
        logger.write(str(result))
        print(result)
