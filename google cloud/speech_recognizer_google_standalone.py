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
            if self.recording_process != None:
                try:
                    self.recording_process.kill()
                except Exception as e:
                    print("Cannot kill sound recognition process: {0}".format(e))
            if self.recog_thread.is_alive():
                self.recog_thread.join()
            print("gspeech recognizer stopped")
        else:
            print("gspeech is already stopped")


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

    def do_new_recognition(self):

        try:
            # Loads the audio into memory
            with io.open(self.file_name, 'rb') as audio_file:
                content = audio_file.read()
                audio_sample = self._speech_client.sample(
                    content,
                    source_uri=None,
                    encoding='FLAC',
                    sample_rate_hertz=48000)

                self.on_recognition_started()

                try:
                    alternatives = self._speech_client.speech_api.recognize(
                        audio_sample, language_code=language_in) 

                    if len(alternatives) > 0:
                        alternative = alternatives[0]

                        print('Transcript: {}'.format(alternative.transcript))
                        print('Confidence: {}'.format(alternative.confidence))

                        confidence = alternative.confidence
                        confidence = confidence * 100

                        self.publish_message(alternative.transcript)    
                except Exception as e:
                    print("Cannot obtain speech: {0}".format(e))
        except Exception as e:
            raise
        finally:
            self.on_recognition_finished()

    def do_recognition(self):
        """Do speech recognition"""
        while self.started:
            # Need to keep self.recording_process actual at every moment of time
            # because of multithreading
            # self.recording_process = subprocess.call(self.sox_args)
            self.recording_process = subprocess.Popen(self.sox_args)

            self.recording_process.communicate()

            self.recording_process = None

            if not self.started:
                continue

            self.do_new_recognition()

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
