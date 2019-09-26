import os
from datetime import datetime

def fromScratch():
    print("ATTENTION")

    print("You are about to START CONSOLIDATING FROM SCRATCH, please\nBACK UP EXISTING CONSOLIDATIONS BEFORE PROCEEDING!\nTo proceed, press any key + Enter")
    input("Press any key + Enter...")

    print("Are you sure?")
    print("If so, press any key + Enter again")

    # infile setup
    in_path = "twitterstreamRASPBERRY/harvests/"
    harvests = os.listdir(in_path)
    outfile_name = "consolidatedHarvests{}.csv".format(str(datetime.now())[:10])
    outfile_path = "twitterstreamRASPBERRY/" + outfile_name

    with open(outfile_path, 'w') as file:
        file.write("lon, lat, URL, datetime, UUID\n")
        file.close()

    for file in harvests:

        with open(in_path + str(file)) as fp:

            print("Working on file: ", str(file), "...")

            for line in fp:
                try:
                    with open(outfile_path, 'a') as outfile:
                        outfile.write(line)


                except:
                    pass
            outfile.close()

        fp.close()
        print("Re-writing of file {} completed.".format(str(file)))

def addToExisting():
    # infile setup

    print("ATTENTION")

    print("You are about to ADD to an EXISTING consolidated file, please\ndouble-check that no used files are used again!\nTo proceed, press any key + Enter")
    input("Press any key + Enter...")

    print("Are you sure?")
    print("If so, input the date of the existing file you would like to append stuff to (YYYY-MM-DD).")
    date = input("Append to: ")

    in_path = "twitterstreamRASPBERRY/harvests/"
    harvests = os.listdir(in_path)
    outfile_name = "consolidatedHarvests{}.csv".format(str(date))
    outfile_path = "twitterstreamRASPBERRY/" + outfile_name

    for file in harvests:

        with open(in_path + str(file)) as fp:

            print("Working on file: ", str(file), "...")

            for line in fp:
                try:
                    with open(outfile_path, 'a') as outfile:
                        outfile.write(line)


                except:
                    pass
            outfile.close()

        fp.close()
        print("Re-writing of file {} completed.".format(str(file)))


addToExisting()