import os
import cv2
from datetime import datetime

"""The BatchBoi200 allows you to store image files in batches of a given size, separately in folders within the same root folder """


folder = "fullTrainingDataset/"

file_list = os.listdir(folder)
begin = datetime.now()

n = 0
m = 0
batch = 0
batch_size = 200
stop = 0

#set up first batch subfolder batch1
os.mkdir("fullTrainingDataset/batch" + str(batch + 1))

print("BatchBoi2000 initializing...")
print("BatchBoi2000 begin...")
print("__"*10)
print("BatchBoi2000 running at full speed")

for number in range(0, len(file_list)):
    photo_name = str(file_list[n+m])
    file_path = folder + photo_name

    # load image
    image = cv2.imread(file_path)

    #scaling folder number
    subfolder_batch = "fullTrainingDataset/" + "batch{}".format(batch+1)

    cv2.imwrite(subfolder_batch + "/" + photo_name, image)


    n += 1
    stop +=1

    if n == batch_size:
        batch += 1
        print("batch ", batch, " finished")
        n = 0
        m += batch_size
        os.mkdir("fullTrainingDataset/batch" + str(batch + 1))
        print("folder for batch " + str(batch + 1)+ " created")



end = datetime.now()
time_elapsed = end - begin
print("\ntotal time elapsed: ", time_elapsed)