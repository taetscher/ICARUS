**I**mage **C**lassification **A**pplication for **R**oad **U**tility **S**tatus  

# :bird: :sunny: ICARUS  



This project is mentored by



+ [_PD Dr. Andreas Heinimann_](http://www.geography.unibe.ch/ueber_uns/personen/pd_dr_heinimann_andreas/index_ger.html)  
   from the Institute of Geography / Centre for Development and Environment of  
   the University of Bern  


Also thank you to


+ [_Prof. Dr. Paolo Favaro_](http://www.inf.unibe.ch/about_us/people/prof_dr_favaro_paolo/index_eng.html)  
   from the Computer Vision Group of the  
   Computer Science Department of the University of Bern  

for his insights into Image Classification.


ICARUS was implemented by


+ _Benjamin Schuepbach_  
   Master Student at the Institute of Geography  
   of the University of Bern  
   benjamin.schuepbach@students.unibe.ch  


----


## About ICARUS 
This program provides an algorithm to determine the presence
of all-season roads in digital images. It is currently a work in progress.

ICARUS is part of a masters thesis at the Institute of Geography of the
University of Bern (Switzerland). 

## How to set up ICARUS
### Requirements & Setup
#### Twitter API Access
#### Google Street View API Access
#### Trained YOLO Weights
Here is a list of the currently top performing checkpoints from training.
Their success is measured as percentage of ASR detections on a validation dataset:

- 52500
- 57500
- 64500 (55%)
- 65250
- 68750
- 80750 (60.5%, med. conf: 0.58)
- 82500 (59%)
- 84250 (55%)
- 86250 (57%)
- 88500 (57%, med. conf: 0.6)
- **94500** (59%, med. conf: 0.61)
- **96500** (64%, med. conf: 0.6)


If you want to use some version of ICARUS yourself, leave me a message here on GitHub and ask me to send you a .ckpt file. I will gladly do so.

---


## How to ICARUS
ICARUS, as the name so adequatly describes, is an image classification algorithm that detects all-season Roads in digital images.

EXPLAIN CONNECTION TO SUSTAINABILITY AND METAPHOR OF ICARUS HIMSELF WHO FLEW TOO CLOSE TO THE SUN

ICARUS is based on tiny-yolo-voc, which is cause of a few undesirable effects:

- the performance of the algorithm is not optimal

- it does not use current, state-of-the-art technology

This is largely due to the following reasons:

- At the time I developed ICARUS, I was a student at the University of Bern, Switzerland.
Students don't usually have a gaming rig outfitted with 50 GTX TitanX graphics cards. My setup included a GTX 760 (2Gb of VRAM), which could only handle the 
smallest of workloads.

- I decided to use some version of yolo, for its [fast detection speeds](https://pjreddie.com/darknet/yolo/) of up to 30 FPS. The drawback of this is a potential sacrifice of accuracy. Yolo is known to be lightning quick, 
but not necessarily always as the most accurate image classifier.

- My training dataset included 5000 images. I had to lable all of my training images myself, which kind of put a constraint on how many I could do.

- I started this project as a complete novice in both the field of programming as well as image classification and machine learning.

Enough with the excuses, though. Let's also highlight a few of the more benefitial insights this project could provide me with.
There are a number of interesting points that were raised with the implementation of ICARUS.

- Big Data for Sustainability (Potentials and Shortcomings)

- Privacy & Consumer Security (also from a geographical perspective)

- Corporate Responsibility (Do global corporations with access to vast amounts of data have a responsibility in helping improve sustainability?)


### ICARUS

explain history (ICARUS & ICARUSv2), how to use and implement

### ICARUSaver
ICARUSaver was designed to save the output of ICARUS as images including prediction bounding boxes with labels. You can provide a custom value for thresh (the yolo threshold).
This allows you to filter out predictions that do not meet your required confidence values.

### ICARUStream
ICARUStream is a standalone version of ICARUS that integrates a steam-listener for the twitter API.
It can be used just like ICARUS.

### ICARUStreetview
ICARUStreetview was used to help validate ICARUS. It is another standalone version of ICARUS which integrates the Google Street View API.
To use IARUStreetview you need to provide a Bounding Box. You then need to provide the variables lat_step and long_step.
These variables are used to create a grid within your Bounding Box. Each cell in this grid has the size lat_step x long_step.
At each intersection in the grid, a call is sent to the Google Street View API, requesting a Street View image from the location at these specific coordinates.
This is what is finally assessed by ICARUS.

### ICARUSValidation
ICARUSValidation was used to determine the quality of checkpoint files during training of ICARUS.
I used it to assess a validation dataset of 200 images that all contained all-season roads. ICARUSViewer saves detailed statistics of each validation
run to a seperate ouptut file (validationStatistics.txt).

### ICARUSViewer
ICARUSViewer works just like ICARUSaver. But instead of saving output files, they are directly displayed on screen. This functionality can be useful if you just want to
quickly check what ICARUS is outputting.

----

## Acknowledgements

True to the scientific method, this project would not have been possible without being able to
'stand on the shoulders of giants'. Many of the components used were already available freely.
Most notably inspiration came from...


   ...the very instructive [pythonprogramming.net](https://pythonprogramming.net/machine-learning-tutorial-python-introduction/), 
   
   ...the ingenious [Mark Jay's YOLO Series](https://github.com/markjay4k/YOLO-series),
   
   ...as well as [the official YOLO Webpage](https://pjreddie.com/darknet/yolo/).


----


## Thank You!
Special thanks go to everyone who helped me along the way. In particular to my mentors who helped
me achieve my ambitious goals. Furthermore I owe a very special thank you to Melanie.
