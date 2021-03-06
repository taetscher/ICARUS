If you are not looking at this website over on [its own GitHub Pages page](https://taetscher.github.io/ICARUS/), feel free to switch now. 

Also, if you're interested, read my masters thesis [over here](https://github.com/taetscher/MastersThesis/blob/master/BIGGER_IS_BETTER__OR_IS_IT_MastersThesisBS14100564.pdf).

**I**mage **C**lassification **A**pplication for **R**oad **U**tility **S**tatus  

# :bird: :sunny: ICARUS  


<p align="center">
      <img src="imageClassification/RESULTS/illustration/371.jpg">
</p>

This project is mentored by



+ [_PD Dr. Andreas Heinimann_](http://www.geography.unibe.ch/ueber_uns/personen/pd_dr_heinimann_andreas/index_ger.html)  
   from the Institute of Geography / Centre for Development   
   and Environment of the University of Bern  


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


## ABOUT ICARUS 
ICARUS, as the name so adequatly describes, is an image classification algorithm that detects all-season Roads (ASR) in digital images.

Information about the accessibility of rural areas is part of the Rural Access Index (RAI), which is a target indicator of the SDGs (Indicator 9.1.1). RAI is in part calculated using information about roads which people can drive on all year round. Methods of generating such data are currently lacking fast and broad coverage. This project was created to help take a step in the direction of using big data to explore possibilities for faster, more broad coverage in monitoring the SDGs.


ICARUS is part of a masters thesis at the Institute of Geography of the
University of Bern (Switzerland). 

Please keep in mind: 

### ICARUS still has a lot of potential for improvement...

Here you can see ICARUSv2 doing what it is supposed to do (kind of _at least_!):

<p align="center">

<img src="imageClassification/RESULTS/illustration/86.jpg">
</p>

Here is an example where you can see that it still has a lot to learn (it does not detect all areas with asphalt road):

<p align="center">

<img src="imageClassification/RESULTS/illustration/57.jpg">
</p>

**ICARUS is still pretty bad at detecting all of the road sections in an image. As explained in more detail below this is in part due to time and hardware constraints resulting from my comparatively very limited budget as a university student (see table below). 
Basically my hardware could not handle more than tiny-yolo, which as a reference [scores a mean average precision (mAP) of 0.237 (or 23.7%)](https://pjreddie.com/darknet/yolo/) on the COCO dataset.**

<table class="tg">
  <tr>
    <th class="tg-c3ow" colspan="2">Hardware Specs of Copmuter used to train ICARUS</th>
  </tr>
  <tr>
    <td class="tg-0pky">Processor</td>
    <td class="tg-0pky">AMD FX(tm)-6100 @ 3.30 GHz</td>
  </tr>
  <tr>
    <td class="tg-0pky">RAM</td>
    <td class="tg-0pky">8.00 GB</td>
  </tr>
  <tr>
    <td class="tg-0pky">Graphics Card</td>
    <td class="tg-0pky">NVIDIA GeForce GTX 760</td>
  </tr>
  <tr>
    <td class="tg-0pky"></td>
    <td class="tg-0pky">1152 CUDA Cores</td>
  </tr>
  <tr>
    <td class="tg-0pky"></td>
    <td class="tg-0pky">2.00 GB of GDDR5 VRAM</td>
  </tr>
</table>

**ICARUSv2 has a mAP of 0.051 (5.1%) using standard PASCAL Challenge IoU = 0.5. At IoU = 0.3 the mAP improves to around 0.14 (14%). These values were calculated with the incredibly useful tool from fellow github user Cartucho: [mAP](https://github.com/Cartucho/mAP)**





So, the bottom line is: ICARUSv2 still kind of sucks.  
The challenges that remain with implementing a decent version of ICARUS are as follows:

- It would be nice if one could use state-of-the-art neural nets (this for me basically means I need to upgrade my hardware)
- One reason the mAP of ICARUSv2 is so low currently, is that 
drawing rectangular bounding boxes over weirdly shaped bits of asphalt road is tricky - for humans as well as a computer. This means that even if most parts containing ASR are labeled to some degree, mAP scores would still be rather low. Alleviating this would likely mean finding a way to label amorphous shapes for training.
- I had a limited time to train ICARUS as well, on bad hardware this leads to questionable results in the machine learning department of the study. Further improvements could surely be achieved if I could work on it full-time
 (My training dataset included 5000 images. I had to lable all of my training images myself, which put a constraint on how many I could do).
 
- I started this project as a complete novice in both the field of programming as well as image classification and machine learning.


Enough with the excuses, though. Let's also highlight a few of the more benefitial insights this project could provide.
There are a number of interesting points that are touched on with the implementation of ICARUS.

- Big Data for Sustainability (Potentials and Shortcomings)

- Privacy & Consumer Security (also from a geographical perspective)
    - potential(s) of deep learning technologies to infringe on privacy of citizens

- Corporate Responsibility (Do global corporations with access to vast amounts of data have a responsibility in helping improve sustainability?)




## ICARUS SETUP
### Setup
This section walks you through the setup needed to run ICARUS.
While you can run darkflow (yolo) on CPU, it is much more efficient to run it on GPU.
On a NVIDIA GPU you will need the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).

#### Twitter API Access
To access the twitter API, set up an account with the [twitter developer platform](https://developer.twitter.com/) and follow their instructions.

#### Google Street View API Access
To use the Google Street View API, set up an account with the [Google developer platform](https://developers.google.com/streetview/?hl=de). This is not needed to run ICARUS, i just used Streetview to check the viability of what I did along the way.


#### Training ICARUS
Here is a list of the currently top performing checkpoints from training. The best performing checkpoint is highlighted in bold.
Their success is measured as percentage of ASR detections on a validation dataset:

ICARUS v2, RMSPROP standard (with tweaks in learning rate whenever loss plateaus were hit)  
(~~crossed out~~ checkpoints were deleted due to storage space constraints)
 
Checkpoint | % of ASR Detection | Median Confidence
----------|--------------------|------------------
20000     |none                |  none
~~94500~~ |59                  |  0.61
~~96500~~ |67                  |  0.6
~~105000~~|72                  |  0.6
~~108000~~|71                  |  0.61
~~110000~~|69                  |  0.6
~~113250~~|69                  |  0.61
131250    |62                  |  0.62
133250    |69                  |  0.6
135500    |68                  |  0.59
136750    |72                  |  0.59
187500    |66                  |  0.63
256000    |66                  |  0.64
258750    |73                  |  0.61
321950    |59                  |  0.64
**344150**|71                  |  0.62
**344750**|68                 |  0.63
**357450**|80                  |  0.61
364350    |65                  |  0.63
370950    |66                  |  0.63
 

It turned out that checkpoint 344750 had the highest mAP score. It still had quite a lot of false positives, though.

ICARUSv2 was trained using the tiny-yolo-voc.cfg file from [pjreddie.com](https://pjreddie.com/darknet/yolo/).
It was trained using the RMSPROP Optimizer and the following commands:  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --train --annotation training/annotations --dataset training/fullTrainingDataset/0_allTrainingBatches --gpu 0.77 --load -1 --batch 10`

At first I trained it with a batch size of 8 and 4 subdivisions. After stagnating in training I moved to batch size of 8 and 0 subdivisions.
In the third stage I moved batch size up to 10, which saw ICARUS improve a lot. When training stagnates, it sometimes is helpful to increase batch size incrementally.
My hardware setup coulnd't handle more than batch size 10 for some reason.

Whenever a plateau of moving ave loss was hit or whenever random "nan" values would show up, I would lower the learning rate and 
continue training this way.

So at step 362550 for example, I changed to the following:  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --train --annotation training/annotations --dataset training/fullTrainingDataset/0_allTrainingBatches --gpu 0.77 --load 362550 --trainer rmsprop --batch 10 --save 3000 --lr 0.00000005`

Then at step 365850 I changed again to:  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --train --annotation training/annotations --dataset training/fullTrainingDataset/0_allTrainingBatches --batch 10 --gpu 0.77 --save 3000 --trainer rmsprop --load -1 --lr 0.000000008`

At step 369750:  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --train --annotation training/annotations --dataset training/fullTrainingDataset/0_allTrainingBatches --batch 10 --gpu 0.77 --save 3000 --trainer rmsprop --load -1 --lr 0.0000000008`

A _second_ version of ICARUS**v2** was trained, using the ADAM Optimizer  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --train --annotation training/annotations --dataset  training/fullTrainingDataset/0_allTrainingBatches --batch 10 --gpu 0.77 --save 3000 --trainer adam --load -1`


**To log the values for training , I changed flow.py in** `/darkflow/net` **as follows:**  
  
        with open("training_stats.csv", 'a') as logger:
            logger.write("{}, {}, {}{}".format(step_now, loss, loss_mva, "\n"))
            logger.close()
            
This now writes a csv file in the root directory of `/darkflow`.


The moving average loss during training reached about 6 to 8 at 20000 steps...

<p align="center">

<img src="imageClassification/ICARUS/darkFLOW_repo/darkflow-master/Plots/fertige_Plots/learning/I2_RMS/I2_RMSPROP_2.png">

</p>

...and around 3 to 5 at 370000 steps.

<p align="center">

<img src="imageClassification/ICARUS/darkFLOW_repo/darkflow-master/Plots/fertige_Plots/learning/I2_RMS/I2_RMSPROP_4.png">

</p>

If you want to use some version of ICARUS yourself, leave me a message here on GitHub and ask me to send you a .ckpt file. I will gladly do so.

---


## HOW TO ICARUS
ICARUS is based on tiny-yolo-voc, and was developed with darkflow:




### ICARUS

A sensible threshold value for analysis would seem to be upwards of `"thresh" : "0.83"`, as below there are too many false positives.

The checkpoint version of ICARUS which was ultimately used was ckpt#344750.

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
I initially used it to assess a validation dataset of 200 images that all contained all-season roads. ICARUSViewer saves detailed statistics of each validation
run to a seperate ouptut file (validationStatistics.txt). Later I turned to the more significant mAP, which can be calculated from the JSON predictions that darkflow can produce.

### ICARUSViewer
ICARUSViewer works just like ICARUSaver. But instead of saving output files, they are directly displayed on screen. This functionality can be useful if you just want to
quickly check what ICARUS is outputting.

### ICARUSTest
ICARUSTest was used to visualize the performance of different checkpoints on the validation dataset.

### ISStracker  
I had to write a quick program using the [_where the ISS at?_ API](https://wheretheiss.at/w/developer) to track the flight path of
the International Space Station (ISS). It turns out the ISS has its own twitter account - and I believed it showed in my data.
So I deployed the ISS tracker to the Raspberry Pi and compared its flight path with the strange tweets coming from the middle of the ocean.

<p align="center">

<img src="imageClassification/RESULTS/mapping/map_harvests_iss.png">

</p>

Turns out I was half right: these images came from the [Horizon](https://twitter.com/bitsofpluto) and [DSCOVR](https://twitter.com/dscovr_epic?lang=de) spacecrafts.
Neat to see the ISS orbit on a map though lol. I found this out through the Google Chrome feature "search Google for this image".


### PLOTTiBOi
PLOTTiBoi was written to visualize some of the results of this thesis. It has three modes:


- one to plot the total amount of tweets saved per day 
- one to plot the detections made with ICARUS
- one to plot the learning progress of ICARUS


### mappyBoi  
See [GitHub Page for mappyBoi](https://github.com/taetscher/mappyBoi) for the source code.
mappyBoi is used to visualize the input/output data of ICARUS as geographic maps.
It is important to note, that due to the projection (PlateCarrée, EPSG 32662), I decided againts putting a scale bar on the map.
The issues with projected coordinate systems and scalebars are well elaborated in a nice article by user _abuckley_ over at https://www.esri.com/arcgis-blog/products/product/mapping/back-to-the-issue-of-scale-bars/.  

----

VALIDATION
--
As mentioned above, to validate ICARUS I calculated mAP.

I validated ICARUS on a set of 200 images from the initial 5200 images that made up my training set.
From these, I took 200 for validation purposes aside, manually classified them but did not actually train on them.
It's my validation subset.

To get predictions I called:  
>`python flow --model cfg/tiny-yolo-ICARUSv2.cfg --annotation annotations/validation --imgdir bilder/validation --load 344750 --json`

In the aforementioned mAP tool one can set the `minoverlap` parameter. This is defined in the [PASCAL Challenge](http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf) as follows:

`To be considered a correct detection, the overlap ratio ao between the predicted bounding
box Bp and ground truth bounding box Bgt must exceed 0.5`

Given the nature of roads, this means that calculating mAP with `minoverlap` of 0.5 but with a rectangular bounding box is not in every case fair to the algorithm. This is why I decided to do mAP calculations with both `minoverlap` of 0.5 as well as 0.3.



RESULTS
--

Here are the results I got from running ICARUSv2 on tweets from May 12 to June 12 2019.

Over this Period of Time, a total of around 0.5 Million tweets were posted that had a geotag and media appended:

<p align="center">

<img src="imageClassification/RESULTS/Plots/harvests/harvests.png">
</p>

Here is a map of all the above tweets:

<p align="center">

<img src="imageClassification/RESULTS/mapping/map_harvests.png">
</p>

For a better understanding, it is paramount to also look at the density the above visualized tweets:

<p align="center">

<img src="imageClassification/RESULTS/mapping/Densities/map_harvests_density.png">
</p>


**These are the results ICARUSv2 produced...**  

...for a threshold of 0.5:

<p align="center">
<img src="imageClassification/RESULTS/mapping/map_ICARUS_thresh50.png">
</p>


...for a threshold of 0.8:

<p align="center">
<img src="imageClassification/RESULTS/mapping/map_ICARUS_thresh80.png">
</p>


...for a threshold of 0.9:

<p align="center">
<img src="imageClassification/RESULTS/mapping/map_ICARUS_thresh90.png">
</p>

For comparison, here's all of the above as a gif:


<p align="center">
<img src="imageClassification/RESULTS/mapping/ICARUS_output.gif">
</p>

Here you can see how changing the detection threshold (aka improving the results of ICARUS) changed the number of outputs:


<p align="center">
<img src="imageClassification/RESULTS/Plots/detections/threshold_v_ouptut.gif">
</p>

----

## ACKNOWLEDGEMENTS

True to the scientific method and in the undying words of Isaac Newton, this project would not have been possible without being able to
'stand on the shoulders of giants'. Many of the components used were already available freely.
Most notably inspiration came from...


   ...the very instructive [pythonprogramming.net](https://pythonprogramming.net/machine-learning-tutorial-python-introduction/), 
   
   ...the ingenious [Mark Jay's YOLO Series](https://github.com/markjay4k/YOLO-series),
   
   ...[Cartucho's fabulous mAP calculator](https://github.com/Cartucho/mAP),
   
   ...as well as [the official YOLO Webpage](https://pjreddie.com/darknet/yolo/).


----


## THANKS
Special thanks go to everyone who helped me along the way. In particular to my mentors who helped
me achieve my ambitious goals, most notably PD Dr. Andreas Heinimann. Furthermore I owe a very special thank you to Melanie.
