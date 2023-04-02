import csv
from datetime import datetime
def main():
    fileName = "tweetData27-03-2023-20-54-04.csv"
    videos = []
    with open(fileName, "r") as file:
        count = 0
        reader = csv.reader(file)
        for row in reader:
            if row[5] == "True":
                count += 1
                videos.append(row[6].replace("?s=20", "/video/1"))
        print(videos)
        print(count)
        vidFileName = "tweetVideos"
        curDate = datetime.now()
        curDate = curDate.strftime("%d-%m-%Y-%H-%M-%S")
        vidFileName = vidFileName + curDate + ".txt"
    with open(vidFileName, "w", newline="") as file:
        for vid in videos:
            file.write(vid + "\n")

main()