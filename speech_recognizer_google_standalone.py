#!/usr/bin/env python
# encoding=utf8

#########################################################################################
#                                    _                                                  #
#      __ _ ___ _ __   ___  ___  ___| |__                                               #
#     / _` / __| '_ \ / _ \/ _ \/ __| '_ \                                              #
#    | (_| \__ \ |_) |  __/  __/ (__| | | |                                             #
#     \__, |___/ .__/ \___|\___|\___|_| |_|                                             #
#     |___/    |_|                                                                      #
#                                                                                       #
# ros package for speech recognition using Google Speech API                            #
# run using 'rosrun gspeech gspeech.py'                                                 #
# it creats and runs a node named gspeech                                               #
# the node gspeech publishes two topics- /speech and /confidence                        #
# the topic /speech contains the reconized speech string                                #
# the topic /confidence contains the confidence level in percentage of the recognization#
#                                                                                       #
#                                                                                       #
# UPDATE: for key generation look http://www.chromium.org/developers/how-tos/api-keys   #
#         at the revision date, each key allows your node to make up to 50 request      #
#         change in the cmd2 at the end of the string "yourkey" for your key            #
#                                                                                       #
# written by achuwilson                                                                 #
# revision by pexison                                                                   #
#                                                                                       #
# 30-06-2012 , 3.00pm                                                                   #
# achu@achuwilson.in                                                                    #
# 01-04-2015 , 11:00am                                                                  #
# pexison@gmail.com                                                                     #
#########################################################################################

from __future__ import unicode_literals

import json, shlex, socket, subprocess, sys, threading
import io
from google.cloud import speech
import shlex,subprocess,os
cmd1='sox -r 16000 -t alsa hw:1,0 recording.flac silence 1 0.1 1% 1 1.5 1%'
cmd2='wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-ru&key=yourkey"'

from settings import *
RECORD_SECONDS = recordingTime

import os
f = open(os.devnull, 'w')

from ctypes import *
# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# $ grep -rn snd_lib_error_handler_t
# include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# Define our error handler type
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

import contextlib
import os
import sys

@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        
class GSpeech(object):
    """Speech Recogniser using Google Speech API"""

    def __init__(self, _api_key):
        """Constructor"""
        # configure system commands
        self._use_old_api = False

        if not self._use_old_api:
            self._speech_client = speech.Client()

        self.recording_process = None
        self.callback = None

        self.api_key = _api_key
        self.file_name = "recording.flac"
        #self.sox_cmd = "sox -r 48000 -t alsa hw:1,0 {file_name} silence 1 0.1 1% 1 0.5 1% trim 00:00 =00:08".format(file_name=self.file_name) #must be the same as recordingTime
        sox_string = "sox -r 48000 -t alsa hw:1,0 {file_name} silence 1 0.1 1% 1 0.5 1% trim 00:00 =00:"+sox_time
        self.sox_cmd = sox_string.format(file_name=self.file_name)
        self.wget_cmd = ("wget -q -U \"Mozilla/5.0\" ") + \
                ("--post-file {file_name} ") + \
                ("--header=\"Content-Type: audio/x-flac; rate=48000\" -O - ") + \
                ("\"https://www.google.com/speech-api/v2/recognize") + \
                ("?output=json&lang=it-it&key={api_key}\"")
        self.wget_cmd = self.wget_cmd.format(api_key=self.api_key, file_name=self.file_name)
        self.sox_args = shlex.split(self.sox_cmd)
        self.wget_args = shlex.split(self.wget_cmd)

        self.use_json_param = "~use_json"

        self._use_json = False

        # run speech recognition
        self.started = False
        self.recog_thread = threading.Thread(target=self.do_recognition, args=())
        # self.recog_thread.start()
        self.is_recognized = False

    def register_callback(self, _callback):
        self.callback = _callback

    def speech_cmd_process(self, message):
        if message.data == "started":
            self.stop(None)
        elif message.data == "ended":
            self.start(None)

    def start(self):
        """Start speech recognition"""
        if not self.started:
            self.started = True
            if not self.recog_thread.is_alive():
                self.recog_thread = threading.Thread(target=self.do_recognition, args=())
                self.recog_thread.start()
            print("gspeech recognizer started")
        else:
            print("gspeech is already running")
    
    def stop(self):
        """Stop speech recognition"""
        if self.started:
            self.started = False
            if self.recog_thread.is_alive():
                self.recog_thread.join()
            print("gspeech recognizer stopped")
        else:
            print("gspeech is already stopped")

    def force_stop(self):
        """Stop speech recognition"""
        if self.started:
            self.started = False
            if self.recording_process != None:
                try:
                    self.recog_thread.kill()
                except Exception as e:
                    print("Cannot kill sound recognition process: {0}".format(e))
            if self.recog_thread.is_alive():
                self.recog_thread.join()
            print("gspeech recognizer force stopped")
        else:
            print("gspeech is already force stopped")


    def isStarted(self):
        return self.started


    def shutdown(self):
        """Stop all system process before killing node"""
        self.started = False
        if self.recog_thread.is_alive():
            self.recog_thread.join()
        self.srv_start.shutdown()
        self.srv_stop.shutdown()

    def on_recognition_started(self):
        self.loginfo("Recognition started")

    def on_recognition_finished(self):
        self.loginfo("Recognition finished")

    def publish_message(self, message):
        if self.callback is not None:
            self.callback(message)


    def do_recognition(self):
        """Do speech recognition"""

        if self.started:
            self.recording_process = True
            self.is_recognized = False

            
            import sys
            global f
            stderr_original = sys.stderr
            sys.stderr = f
            #Grabar audio y guardar en wav

            import pyaudio
            import wave

            

            asound = cdll.LoadLibrary('libasound.so')
            # Set error handler
            asound.snd_lib_error_set_handler(c_error_handler)

            print("*"*65)
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            print("*"*65)


            # Reset to default error handler
            asound.snd_lib_error_set_handler(None)

                

            cantidad_canales = 0
            indice = 0
            sys.stdout.flush()
            for i in range(audio.get_device_count()):
              dev = audio.get_device_info_by_index(i)
              if "USB Audio Device" in dev['name']:
                  indice = i
                  cantidad_canales = dev['maxInputChannels']
                  break
              #print((i,dev['name'],dev['maxInputChannels']))

            FORMAT = pyaudio.paInt16
            CHANNELS = cantidad_canales
            DEVICE_INDEX = indice
            RATE = 48000
            CHUNK = 1024
            global RECORD_SECONDS
            WAVE_OUTPUT_FILENAME = "grabacion.wav"

            # start Recording
            
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                input_device_index = DEVICE_INDEX,
                            rate=RATE, input=True, output=False,
                            frames_per_buffer=CHUNK)
            print("-"*20 + "recording for " + str(RECORD_SECONDS) + " seconds" + "-"*20)
            
            frames = []
             
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            print("-"*20 + "finished recording" + "-"*20)
            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
             
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()


            import speech_recognition as sr
            import sys

            audio_grabado = sr.AudioFile("grabacion.wav")
            r = sr.Recognizer()
            with audio_grabado as source:
              audio = r.record(source)
              try:
                text = r.recognize_google(audio)
                print("From Google you said : {}".format(text))
                sys.stdout.flush()
                self.publish_message(text)
                self.is_recognized = True
              except sr.UnknownValueError:
                print("Sorry could not hear your voice")
                sys.stdout.flush()
                self.is_recognized = False
              except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                sys.stdout.flush()
                try:
                    #text = r.recognize_sphinx(audio, language = "en-US")
                    text = r.recognize_sphinx(audio)
                    print("From Sphinx you said : {}".format(text))
                    sys.stdout.flush()
                    self.publish_message(text)
                    self.is_recognized = True
                except sr.UnknownValueError:
                    print("Sorry could not hear your voice")
                    sys.stdout.flush()
                    self.is_recognized = False

              self.on_recognition_finished()
                 
            sys.stderr = stderr_original

    def loginfo(self, message):
        print("Speech rec (google) :: " + message)



def is_connected():
    """Check if connected to Internet"""
    try:
        # check if DNS can resolve hostname
        remote_host = socket.gethostbyname("www.google.com")
        # check if host is reachable
        tmp_socket = socket.create_connection(address=(remote_host, 80), timeout=5)
        return True
    except:
        pass
    return False


def usage():
    """Print Usage"""
    print("Usage:")
    print("rosrun gspeech gspeech.py <API_KEY>")


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit("No API_KEY provided")
    if not is_connected():
        sys.exit("No Internet connection available")
    api_key = str(sys.argv[1])
    speech = GSpeech(api_key)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
