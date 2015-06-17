from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import subprocess

def analyzeCommand(text):
    global tts

    if "open mail" in text:
        subprocess.call( ["google-chrome", "mail.google.com"] )
    elif "open google" in text:
        subprocess.call( ["google-chrome", "www.google.com"] )

    elif "sound down" in text:
        subprocess.call( ["amixer", "-q", "sset", "Master", "10dB-"] )
    elif "sound up" in text:
        subprocess.call( ["amixer", "-q", "sset", "Master", "10dB+"] )

    elif  "music play" in text:
#        tts.say( "My Lord, I will let the music play" )
        subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Play"])
    elif "music stop" in text:
#        tts.say( "My Lord, I will stop the music for you" )
        subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Pause"])
    elif "music next" in text:
#        tts.say( "My Lord, I will skip that song" )
        subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Next"])


class SpeechHandler(ALModule):
    def callback(self, key, value, msg):
        text = value[0]
        conf = value[1]

        if conf > 0.5:
            analyzeCommand(text)
        print str(time.time()) + ": Received " + str(key) + " with data " + str(value[0] + " conf " + str(value[1]))

import sys

IP = 'naobidi.local'
if len(sys.argv) > 1:
    IP = str(sys.argv[1])

print "using robot ip ", IP

asr = ALProxy("ALSpeechRecognition", IP, 9559)
asr.pause(True)

vocabulary = ["music play", "music stop", "music next", "open mail", "open google", "sound down", "sound up"]
asr.setVocabulary(vocabulary, True)

asr.subscribe("NAO_SPEECH")
asr.pause(False)

tts = ALProxy("ALTextToSpeech", IP, 9559)

memory = ALProxy("ALMemory", IP, 9559)
broker = ALBroker("pythonBroker","0.0.0.0", 0, IP, 9559)
naospeech = SpeechHandler("naospeech")
memory.subscribeToEvent("WordRecognized", "naospeech", "callback")

#subprocess.call("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play", shell=True)

import time
while( True ):
    time.sleep(0.1)
