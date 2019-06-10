import matplotlib.pyplot as plt
import os
import numpy as np


icarus_version = 2
thresh = 0.5
data = {}

colors = {"grey":"#494a4c", "black":"#0c0c0c"}


def plotAssessment():
    with open("icarusOUTPUT/ICARUS{}/output.csv".format(icarus_version)) as s_file:

        while True:
            try:
                # read line and separate values
                line = s_file.readline().split(";")
                day = line[3].split(" ")[1]
                hour = line[3].split(" ")[2]

                # if the day is not already in the list,
                if not day in data:
                    data[day] = 1

                else:
                    data[day] += 1


            except IndexError:
                break

    s_file.close()

    # plotting stuff now
    fig, ax = plt.subplots()
    plt.scatter(data.keys(), data.values(), color=colors["black"], marker=".")

    # label the figure
    plt.title("Detections with ICARUSv{},\nthreshold set at {}".format(icarus_version, thresh))
    plt.xlabel("Date")
    plt.ylabel("Detections")

    # customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()
    print("plotAssessment done!")

def plotHarvests():
    # infile setup
    in_path = "twitterstreamRASPBERRY/harvests/"
    harvests = os.listdir(in_path)

    for file in harvests:
        with open(in_path + str(file)) as infile:

            while True:
                try:
                    # read line and separate values
                    line = infile.readline().split(",")
                    day = line[3].split(" ")[1]
                    hour = line[3].split(" ")[2]


                    # if the day is not already in the list,
                    if not day in data:
                        data[day] = 1

                    else:
                        data[day] += 1


                except IndexError:
                    break

            infile.close()

    keys = data.keys()
    x = []
    for entry in keys:
        date = entry.split("-")[2]
        x.append(date)
    y = data.values()

    # plotting stuff now
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    plt.plot(keys, y, color=colors["black"], marker=".")

    # label the figure
    plt.suptitle("TWEETS WITH GEOTAG AND MEDIA APPENDED\n")
    plt.title("MAY 03 - JUNE 05 2019", color=colors["grey"])
    plt.xlabel("DATE", color=colors["black"])
    plt.ylabel("TWEETS", color=colors["black"])
    ax.set_xticklabels(x)

    plt.annotate(
        " RasPi down", xy=("2019-05-16",2000),
        xytext=("2019-05-16", 3000), color=colors["grey"])
    plt.annotate(
        " RasPi down", xy=("2019-06-02", 2000),
        xytext=("2019-06-02", 5000), color=colors["grey"])


    # customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_color("grey")
    #ax.spines['left'].set_color("grey")
    ax.tick_params(axis='x', colors=colors["grey"])
    ax.tick_params(axis='y', colors=colors["grey"])



    plt.show()


plotAssessment()