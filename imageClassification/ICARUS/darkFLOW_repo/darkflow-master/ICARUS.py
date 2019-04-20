from darkflow.net.build import TFNet
import cv2

#---------------------------------------------------------
"""
ICARUS (Image Classification Application for Road Utility Status)

This program provides an algorithm to determine the presence/status
of roads in digital images.

It is part of a masters thesis at the Geographic Institute of the
University of Bern (Switzerland)


This project was mentored by

PD Dr. Andreas Heinimann from the
Geographic Institute / Centre for Development and Environment of
the University of Berne

and

Prof. Dr. Paolo Favoro from the
Computer Vision Group of the
Computer Science Department of the University of Berne



ICARUS was authored by

Benjamin Schuepbach
benjamin.schuepbach@students.unibe.ch

"""

#inspired by Mark Jay (YouTube)
#---------------------------------------------------------

# NEED TO TRAIN YOLO ON ALL-SEASON ROADS BEFORE THIS IS USED AGAIN!
# NEED TO GET SOME 4000 MORE IMAGES TO GET 10,000 FOR TRAINING SET.

'''
this is a dictionary that sets up yolo.
[model] is a parameter that specifies which model to use like folder/model.cfg
[load] is used to load predefined weights like bin/weights.weights
[threshold] specifies the minimal confidence factor yolo needs to draw a bounding box
'''
options = {"model": "cfg/tiny-yolo-ICARUS.cfg", "load": 21000, "threshold": 0.5}
tfnet = TFNet(options)

#loading image
imgcv = cv2.imread("./images/000807.jpg")

#predict labels of objects in image
result = tfnet.return_predict(imgcv)

#outputs a list of dictionaries, each dictionary representing a detected object
print(result)