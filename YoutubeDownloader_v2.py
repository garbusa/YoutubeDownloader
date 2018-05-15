from pytube import YouTube
import os
import configparser
import subprocess
import sys

clear = lambda: os.system('cls')
toolbar_width = 100

#Refreshing Progressbar
def progress_bar(stream = None, chunk = None, file_handle = None, remaining = None):
	percent = (100*(file_size-remaining))/file_size #Calculating actuall percentage
	print("Downloading: %s" % default_filename)
	print("{:00.0f}% downloaded".format(percent))
	sys.stdout.write("[%s]" % (" " * toolbar_width)) # [                              ...]
	sys.stdout.flush()
	sys.stdout.write("\b" * (101)) #Starting after [ instead of ]
	sys.stdout.write("-"*int(percent))
	sys.stdout.write("\n")
	clear()

#Load Config
config = configparser.ConfigParser()
config.read('config.ini')
download_dir = config['Paths']['download_dir']

#Creating new dir if doesnt exist
if not os.path.exists(download_dir):
    print("\nFolder does not exists... Creating...")
    os.makedirs(download_dir)
else:
    print("\nFolder found! Script starting...")

#link = input("Enter Youtube Video Link (exit if you want to leave): ")

numberOf = int(input("Please enter the amount of Downloads in this session: "))

links = []

for i in range(1, numberOf+1):
	print("Enter the",i,". YouTube Link:")
	link = input()
	links.append(link)

for j in range(0, numberOf):
	try:
		yt = YouTube(links[j], on_progress_callback=progress_bar)
		vids = yt.streams.filter(only_audio=True).all() # catch only audio streams

		global file_size
		file_size = vids[0].filesize #get filesize for progressbar

		default_filename = vids[0].default_filename
		print("Downloading %s. Video: %s" % (str(j), default_filename))
		vids[0].download(download_dir)

		print("Converting",default_filename,"to mp3...")

		# using ffmpeg.exe for converting to mp3
		subprocess.call([
		    "ffmpeg", "-i",
		    os.path.join(download_dir, default_filename),
		    os.path.join(download_dir, '%s.mp3' % default_filename[:-4]),
			"-loglevel", "quiet"
		    ])

		os.remove(download_dir+default_filename) #remove old mp4 file
	except:
		if link == "exit":
			sys.exit("Bye Bye")
		print("This is not a YouTube link. Restarting the script...")
		os.execv(sys.executable, ['python'] + sys.argv)
