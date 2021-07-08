import RPi.GPIO as GPIO 
import subprocess 
import os 
import signal
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
#signal = os.system("cd /home/pi/pifm; sudo ./pifm record.wav 87.9 210000 mono")
cmd = "(sudo nice --10 rtl_fm -f 93.3e6 -s 200000 -r 48000 | ffmpeg -y -f s16le -ar 23000 -ac 2 -i - recieve.wav &)"
playback = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

#playback = subprocess.call("(sudo nice --10 rtl_fm -f 87.9e6 -s 200000 -r 48000 | ffmpeg -y -f s16le -ar 23000 -ac 2 -i - record.wav &)", shell=True, preexec_fn=os.setsid)

#playback = os.system("(sudo nice --10 rtl_fm -f 87.9e6 -s 200000 -r 48000 | ffmpeg -y -f s16le -ar 23000 -ac 2 -i - record.wav)")
#play = subprocess.Popen(["nice", "--10", "rtl_fm", "-f", "93.3e6", "-s", "200000", "-r", "48000", "|", "ffmpeg", "-y", "-f", "s16le", "-ar", "23000", "ac", "2", "-i", "-", "record.wav", "&"], shell=True, stdout = subprocess.PIPE)
#print(play)
while True:
	if not (GPIO.input(18)):
		print("playing back message")
		os.killpg(os.getpgid(playback.pid), signal.SIGTERM)
		os.system("sudo sox recieve.wav recieveReverse.wav reverse")
		os.system("sudo sox recieveReverse.wav recieveReverseB.wav speed 0.5")
		time.sleep(5)
		os.system("sudo aplay recieve.wav")
		
		print("recording message")
		record = os.system("cd /home/pi/pifm; arecord -d 10 -f cd -t wav record.wav")
		
		time.sleep(3)
		print("encrypted")
		encrypt = os.system("sox record.wav record2.wav speed 2; sox record2.wav recordReverse.wav reverse;")
		print("transmitting message")
		transmit = os.system("sudo cd /home/pi/pifm; sudo ./pifm recordReverse.wav 87.9 48000 mono")

