"""
Class adapted from
'THeK3nger' original github upload
to include a "speed" functionality
for the sound played, a blip
for TamuHack 2020 by Jack Wang
"""
import os
import wave
import threading
import sys

# PyAudio Library
import pyaudio

import time

# Pydub for .mp3 to .wav
import pydub
from pydub import AudioSegment


class WavePlayerLoop(threading.Thread):
    """
  A simple class based on PyAudio to play wave loop.
  It's a threading class. You can play audio while your application
  continues to do its stuff. :)
  """

    CHUNK = 1024

    def __init__(self, filepath, loop=True):
        """
    Initialize `WavePlayerLoop` class.
    PARAM:
        -- filepath (String) : File Path to wave file.
        -- loop (boolean)    : True if you want loop playback.
                               False otherwise.
    """
        super(WavePlayerLoop, self).__init__()
        if ".mp3" in os.path.abspath(filepath):
            self.mp3_to_wav(os.path.abspath(filepath))
        self.filepath = os.path.abspath(filepath[:-4]+".wav")
        self.loop = loop
        self.speed = 1.0

    def run(self):
        # Open Wave File and start play!
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()

        # Open Output Stream (basen on PyAudio tutorial)
        stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        # PLAYBACK LOOP
        data = wf.readframes(self.CHUNK)
        # lock = threading.Lock()
        # cv = threading.Condition(lock)
        # cv.acquire()
        while self.loop:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            if data == b'':  # If file is over then rewind.
                wf.rewind()
                data = wf.readframes(self.CHUNK)
                time.sleep(.75*self.speed)
                # cv.wait(timeout=.75 *self.speed)

        stream.close()
        player.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
        """
        Stop playback.
        """
        self.loop = False

    def change_speed(self, speed):
        """"
        changes speed
        """
        self.speed = speed

    def mp3_to_wav(self, file):
        """
        Changes .mp3 file to .wav file
        """
        sound = AudioSegment.from_mp3(file)
        file = file[:-4]
        sound.export(file+".wav", format="wav")