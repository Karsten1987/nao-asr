from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import subprocess

def analyzeCommand(text):
    global tts
    global command_dict

    command_key = [x.strip() for x in text.split("<...>")][1]
    if command_dict.has_key(command_key):
        subprocess.call( command_dict[command_key] )
        return

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

command_dict = {"open mail": ["google-chrome", "mail.google.com"],
                "open google": ["google-chrome", "www.google.com"],
                "open agenda": ["google-chrome", "www.google.com/calendar"],
                "open drive": ["google-chrome", "drive.google.com"],
                "new terminal": ["terminator", "--new-tab"],
                "music play": ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.PlayPause"],
                "music pause": ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.PlayPause"],
                "music stop": ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Stop"],
                "music next": ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Next"],
                "sound down": ["amixer", "-q", "sset", "Master", "10dB-"],
                "sound up": ["amixer", "-q", "sset", "Master", "10dB+"],
                "good morning": ["google-chrome", "www.bonjourmadame.fr/random"],
                "hello chef": ["google-chrome", "wiki.ros.org"]
}

asr.setVocabulary(command_dict.keys(), True)

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
