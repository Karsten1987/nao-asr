import speech_recognition as sr
import subprocess

def callback(recognizer, audio):                          # this is called from the background thread
    try:
        text = recognizer.recognize(audio)
        if  "music play" in text:
            print "gonna play music "
            subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2",  "org.mpris.MediaPlayer2.Player.Play"])
        elif "music stop" in text:
            subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2",  "org.mpris.MediaPlayer2.Player.Pause"])
        elif "music next" in text:
            subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/MediaPlayer2",  "org.mpris.MediaPlayer2.Player.Next"])
        print("You said " + text)  # received audio data, now need to recognize it
    except LookupError:
        print("Oops! Didn't catch that")
r = sr.Recognizer()
r.listen_in_background(sr.Microphone(), callback)

subprocess.call(["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",  "/org/mpris/Me    diaPlayer2",  "org.mpris.MediaPlayer2.Player.Play"])

import time
while True: time.sleep(0.3)                         # we're still listening even though the main thread is blocked
