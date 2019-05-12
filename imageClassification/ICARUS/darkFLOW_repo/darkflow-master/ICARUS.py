from darkflow.net.build import TFNet
import cv2
import numpy as np
import requests
from datetime import datetime
import smtplib
import ssl


#---------------------------------------------------------
"""
ICARUS1 (Image Classification Application for Road Utility Status)

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



ICARUS1 was authored by

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
[gpu] specifies whether yolo should run on cpu or gpu - keep in mind for running on gpu you'll need additional software by nvidia
'''
#yolo setup
options = {"model": "cfg/tiny-yolo-ICARUS.cfg", "load": 21000, "threshold": 0.5, "gpu": 0.6}
tfnet = TFNet(options)



# global variables
icarus_version = 1
n1 = 0
n2 = 0
l = 0
found = 0
start = datetime.now()
gmail_account = "taetschericarus@gmail.com"
password = eval(open("gmail_credentials.txt").read())

# let user know that they should watch out which icarus version they use
print("ICARUS Running with following options parameters:\n")
print(options)
input("\nPlease be aware that you are using savefile directory for ICARUS version {}. If this is not correct, exit immediately. Continue [Y/n]?.\n".format(icarus_version))

# add or remove accounts that should recieve an email when ICARUS is done
reciever_accounts = ["beni.schuepbach@hispeed.ch", "auteblauwau@hotmail.com", "ch.schuepbach@swissonline.ch"]

# infile setup
in_path = "twitterstreamRASPBERRY/"
raspi_file = "CONSOLIDATED_georefMediaTweets.txt"
in_file = in_path + raspi_file
now = str(datetime.now())[:10]


# check how many images are to be processed
print("Calculating time ICARUS will need...")
with open(in_file) as infile:
    line = infile.readline()

    while line:
        if l >50000:
            l = 0
            print("...")

        else:
            n1 += 1
            line = infile.readline()
            l += 1

#calculate approximate time to finish task
app_time = n1*0.5/60/60
print("Infile contains {} links to images. It will take approximately {} hours for ICARUS to assess all images.\n(Calculation based on approximately 2 Images/s)\n".format(n1,app_time))

#get info for sending email when ICARUS is done
print("-"*30, "\n")
print("ICARUS will send an email to {} when its done.\n".format(reciever_accounts))
print("-"*30)


print("ICARUS Initiated\n")

with open(in_file) as fp:
    line = fp.readline()

    while line:
        try:
            # read in lines as arrays
            array = line.split(", ")

            # extract coordinate information (lat/long), link to media, timestamp, uuid
            coord_x = array[0]
            coord_y = array[1]
            medurl = array[2]
            timestamp = array[-2]
            indi_id = array[-1]

            print(str(medurl))

            # download image, if this fails, go with next one
            try:
                img_data = requests.get(medurl).content
                temp_name = 'temp_img.jpg'

                with open('images/temp/' + temp_name, 'wb') as handler:
                    # save image data from URL
                    handler.write(img_data)
                    handler.close()

                # pass image to yolo
                imgcv = cv2.imread('images/temp/' + temp_name)

                # assess image with yolo
                result = tfnet.return_predict(imgcv)

                # count how many images were actually assessed
                n2 += 1

                if len(result) > 0:
                    # count how many AllSeasonRoads were predicted
                    found += 1

                    # prepare yolo output to be saved in csv
                    a = range(0, len(result))
                    confidence_list = []
                    for element in a:
                        confidence = result[element]['confidence']
                        confidence_list.append(confidence)

                    avr_confidence = np.mean(confidence_list)

                    # basically, if anything was detected (if any all_Season_Roads were found), save data
                    with open("icarusOUTPUT/ICARUS{}/{}.csv".format(icarus_version, raspi_file[:-4]), 'a') as outfile:
                        outfile.write(
                            "{}; {}; {}; {}; {}; {}\n".format(coord_x, coord_y, medurl, timestamp, avr_confidence,
                                                              result))


                else:
                    # elso continue to the next tweet
                    pass

                print(result)

            #if any of the above fail, pass and continue with next one.
            except:
                print("Error occured, proceeding to next entry.")
                pass





        except AssertionError:
            # this catches errors of type 'image is not of type np.ndarray'
            print("numpy fucked up")
            pass



        # go to next line
        line = fp.readline()


        print("assessing image {}/{}".format(n2,n1))

#prepare to save metadata of run
stop = datetime.now()
percentage = 100*(found/n2)

with open("icarusOUTPUT/MetaData.txt", 'a') as logger:
    logger.write("-" * 90)
    logger.write("\nNEW RUN at {}\n".format(start))
    logger.write("-" * 90)
    logger.write("\nRan ICARUS1 on: {}\n".format(in_file))
    logger.write("-" * (17 + len(in_file)))
    logger.write("\nICARUS1 running with the following options")
    logger.write("\nYOLO-Options: {}".format(options))
    logger.write("\nNumber of Images assessed: {}".format(n2))
    logger.write("\nAllSeasonRoads detected: {}, as percentage: {}%".format(found, percentage))
    logger.write("\nDuration: [HH:MM:SS.MS] {}".format(stop - start))
    logger.write("\nConfirmation Email sent from {} to: {}\n".format(gmail_account,reciever_accounts))
    logger.write("-" * 90)
    logger.write("\n\n\n")
    logger.close()

print("Statistics of run saved...")

#set up email to send
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
message = """ICARUS1 finished run at {}\n{}\nRan on: {}\nNumber of Images Assessed: {}\nAllSeasonRoads detected: {}\nDuration: {}\n\n""".format(str(start)[:10], "-"*33 ,in_file, n1, found, stop-start)


context = ssl.create_default_context()

for account in reciever_accounts:
    print("Sending confirmation Email to {}".format(account))
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(gmail_account, password)
        server.sendmail(gmail_account, account, message)




print("-"*30)
print("\nEmail notification sent to {}".format(reciever_accounts))
print("See icarusOUTPUT/MetaData.txt for statistics of run.")