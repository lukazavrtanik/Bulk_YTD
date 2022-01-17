import re #RegEx
import pytube #Dwonloading from YouTube
import os #Getting current folder
from datetime import datetime #Getting current date and time
from moviepy.editor import * #Converting mp4 to mp3
import glob  #For getting the latest file name

#Download only videos containing one of these words - INPUT
word1 = "mix"
word2 = "Mix"
word3 = "set"
word4 = "Set"
word5 = "techno"
word6 = "Techno"

#Videos default format is mp4. Convert to mp3? (0=NO, 1=YES)
mp3 = 1

#Set to 1: Dowmload, Set to 0: prerview video names only
dp = 1

#Open and read the file
f = open('links.txt', 'r', errors="ignore")
contents = f.read()

#Move text into lines - not necessary
#contents = contents.replace('\t','\n')

#Filter only videos using RegEx
pattern = re.compile('https://www.youtube.com/wa.*')
matches = pattern.findall(contents)

#Removes duplicates
matches = set(matches)

#Save path for downloading - creates new folder in current directory for each run
currentfolder = os.getcwd()                                 #Get current folder
currentdate = datetime.now()                                #Get current date and time - for naming the new folder
currentdate = str(currentdate)                              #Make the date nad time into a string
folderpat = re.compile(r":")                                #Remove colons - otherwise Windows complains
foldername= folderpat.sub("-", currentdate)                 #Remove colons - otherwise Windows complains
os.mkdir(foldername)                                        #Create a new folder
SAVE_PATH = os.path.abspath(os.getcwd()+"\\"+foldername)    #Set the save path
os.chdir(SAVE_PATH)                                         #Move working dir to the new folder

#Go through the whole list one video by one
for match in matches:
    #Check video name
    yt = pytube.YouTube(match)
    name = yt.title
    #Check if the video title contains the set words
    if (word1 in name) or (word2 in name) or (word3 in name) or (word4 in name) or (word5 in name) or (word6 in name):
        if dp==1:
            #print(name)
            filtername = re.sub('[^0-9a-zA-Z\s]', '', name)  # Remove special characters - otherwise there might be an error
            print(filtername)
            yt.streams.get_highest_resolution().download(SAVE_PATH, filename=filtername+".mp4")
            #Converts to mp3
            if mp3 == 1:
                oldname = filtername + ".mp4"
                newname = filtername + ".mp3"
                videoclip = VideoFileClip(oldname)
                audioclip = videoclip.audio
                audioclip.write_audiofile(newname)
                audioclip.close()
                videoclip.close()
        if dp==0:
            print(name)


f.close()

