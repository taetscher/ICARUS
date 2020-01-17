import matplotlib.pyplot as plt
import os
import numpy as np




icarus_version = 2
trainer = "RMSPROP"
thresh = 0.8
data = {}
detects = {}

colors = {"grey":"#494a4c", "black":"#0c0c0c", "blue":"#000856", "purple":"#8c0289", "pink":"#ef47ff"}


def plotDetection(thresh = thresh):
    """Plots Detections made with ICARUS"""

    data = {}
    detects = {}

    with open("icarusOUTPUT/ICARUS{}/output_12_12.csv".format(icarus_version)) as s_file:

        while True:
            try:
                # read line and separate values
                line = s_file.readline().split(";")
                day = line[3].split(" ")[1]
                hour = line[3].split(" ")[2]
                predictions = eval(line[5])

                d = 0
                #count on how many bilder detections were made
                if not day in detects:
                    detects[day] = 1

                else:
                    detects[day] += 1

                #count how many predictions in total
                if any(prediction['confidence'] > thresh for prediction in predictions):
                    # if the day is not already in the list,
                    if not day in data:
                        data[day] = 1

                    else:
                        data[day] += 1


            except IndexError:
                break

    s_file.close()

    print(predictions)
    keys = data.keys()
    x = []
    for entry in keys:
        date = entry.split("-")[2]
        x.append(date)
    y = data.values()

    # plotting stuff now
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    plt.plot(data.keys(), data.values(),color=colors["purple"], marker="x" , label="Total Images with Prediction at threshold {}".format(thresh))
    plt.plot(detects.keys(), detects.values(), color=colors["black"], marker="." , label="Total Images with Detections")

    # label the figure
    plt.suptitle("DETECTIONS OF ALL SEASON ROADS WITH ICARUSv{}".format(icarus_version))
    plt.title("TRESHOLD SET AT {}, RAN MAY 12 - JUNE 12".format(thresh), color=colors["grey"])
    plt.xlabel("May                                    DATE                                    June", color=colors["black"])
    plt.ylabel("DETECTIONS")
    ax.set_xticklabels(x, fontsize=5)
    ax.legend(loc="upper center")

    # annotations
    plt.annotate(
        " RasPi down", xy=("2019-05-16", 2000),
        xytext=("2019-05-16", 500), color=colors["grey"])
    plt.annotate(
        " RasPi down", xy=("2019-06-02", 2000),
        xytext=("2019-06-02", 500), color=colors["grey"])

    # customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(colors["grey"])
    ax.spines['left'].set_color(colors["grey"])
    ax.tick_params(axis='x', colors=colors["grey"])
    ax.tick_params(axis='y', colors=colors["grey"])

    #save and show
    plt.savefig("Plots/detections_thresh{}.png".format(round(thresh*100)))
    #plt.show()

def plotHarvests():
    """Plots Input data (number of tweets saved)"""

    months = []

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
                    month = line[3].split(" ")[1][:-3]

                    # if the day is not already in the list,
                    if not day in data:
                        data[day] = 1

                    else:
                        data[day] += 1


                    months.append(month)


                except IndexError:
                    break

            infile.close()


    keys = data.keys()


    x = []
    for entry in keys:
        date = entry
        x.append(date)

    y = list(data.values())
    ave = np.average(y)
    average_list = []

    print(ave)

    for element in range(len(y)):
        average_list.append(ave)

    #finding labels
    xticks = []

    for element in x:
        if int(element.split('-')[2]) == 22:
            xticks.append(element)
        else:
            pass


    # plotting stuff now
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    plt.plot(keys, y, color=colors["black"], marker=".", label="Tweets streamed by Twitter streaming API")
    plt.plot(keys, average_list, label="Average", color=colors["purple"], alpha=0.8)

    # label the figure
    plt.suptitle("TWEETS WITH GEOTAG AND MEDIA APPENDED\n")
    plt.title("MAY 12th - SEPTEMBER 23rd 2019", color=colors["grey"])
    plt.xlabel("DATE", color=colors["black"])
    plt.ylabel("NUMBER OF TWEETS", color=colors["black"])
    ax.set_xticks(xticks)
    ax.set_xticklabels(['May 20th','June 20th','July 20th','August 20th','September 20th'],    fontsize = 8)


    plt.legend(loc="upper center", fontsize=8)



    # customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_color("grey")
    #ax.spines['left'].set_color("grey")
    ax.tick_params(axis='x', colors=colors["grey"])
    ax.tick_params(axis='y', colors=colors["grey"])

    ###not needed anymore###
    #every_nth = 2
    #for n, label in enumerate(ax.xaxis.get_ticklabels()):
        #if n % every_nth != 0:
            #label.set_visible(False)

    # save and show
    plt.savefig("Plots/harvests_may_september.png")
    plt.show()

def plotLearning():
    """Plots Learning of ICARUS"""

    step_list = []
    loss_list = []
    maveloss_list = []

    with open("training_stats.csv") as infile:
        while True:
            line = infile.readline().split(", ")
            try:
                step = int(line[0])
                loss = round(float(line[1]), 2)
                maveloss = round(float(line[2]),2)

                step_list.append(step)
                loss_list.append(loss)
                maveloss_list.append(maveloss)

            except:
                break

    # calculate the trendline for moving average loss (least squares polynomial fit)
    z = np.polyfit(step_list, maveloss_list, deg=1)
    p = np.poly1d(z)


    # plotting stuff now
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    plt.plot(step_list, loss_list, color=colors["black"], marker=".", label="Loss")
    plt.plot(step_list, maveloss_list, color=colors["purple"], marker="x", label="Moving Average Loss", linewidth=1)
    plt.plot(step_list, p(step_list),"-", color=colors["pink"], label="MAL Trendline")

    # label the figure
    plt.suptitle("    LEARNING PROGRESS OF ICARUSv{}".format(icarus_version), horizontalalignment="center")
    plt.title("TRAINED WITH {} OPTIMIZER".format(trainer), color=colors["grey"], horizontalalignment="center")
    plt.xlabel("STEP")
    plt.ylabel("LOSS")
    ax.legend(loc="upper center")

    # customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(colors["grey"])
    ax.spines['left'].set_color(colors["grey"])

    # save and show
    plt.savefig("Plots/learning.png")
    plt.show()


#threshololo=[0.6,0.7,0.8,0.85,0.9]

#for element in threshololo:
    #plotDetection(thresh=element)

plotHarvests()