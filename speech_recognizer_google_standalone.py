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
#from google.cloud import speech
import shlex,subprocess,os
cmd1='sox -r 16000 -t alsa hw:1,0 recording.flac silence 1 0.1 1% 1 1.5 1%'
cmd2='wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-ru&key=yourkey"'

from settings import *
RECORD_SECONDS = recordingTime
setting_language = str(language_in)
THRESHOLD = threshold
SECONDS_IN_SILENCE = seconds_in_silence
speech_lock = False

from ctypes import *
# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# $ grep -rn snd_lib_error_handler_t
# include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# Define our error handler type
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

import os
import sys

devnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)
def ignore_stderr():
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

def attend_stderr():
    os.dup2(old_stderr, 2)
    os.close(old_stderr)
    
        
class GSpeech(object):
    """Speech Recogniser using Google Speech API"""

    def __init__(self, _api_key):
        """Constructor"""
        ## configure system commands
        #self._use_old_api = False

        #if not self._use_old_api:
        #    self._speech_client = speech.Client()

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

    def is_in_recognition(self):
        global speech_lock
        return speech_lock

    def force_stop(self):
        """Stop speech recognition"""
        if self.started:
            self.started = False
##            if self.recording_process != None:
##                try:
##                    self.recog_thread.kill()
##                except Exception as e:
##                    print("Cannot kill sound recognition process: {0}".format(e))
            if self.recog_thread.is_alive():
                self.recog_thread.join()
                #self.recog_thread.kill() #none of them work
            print("gspeech recognizer force stopped")
        else:
            print("gspeech is already force stopped")
            
        speech_lock = False
        #print("speech_lock google force_stop", speech_lock)


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
        #speech_lock = False   #does not work here
        #print("speech_lock google finished", speech_lock)

    def publish_message(self, message):
        if self.callback is not None:
            self.callback(message)


    def do_recognition(self):
        """Do speech recognition"""

        if self.started:
            self.recording_process = True
            self.is_recognized = False

            #Grabar audio y guardar en wav

            import pyaudio
            import math
            import struct
            import wave
            import sys

                        
            asound = cdll.LoadLibrary('libasound.so')
            # Set error handler
            asound.snd_lib_error_set_handler(c_error_handler)

            print("*"*65)
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            print("*"*65)

            # Reset to default error handler
            asound.snd_lib_error_set_handler(None)

            #ignore_stderr()
            # Initialize PyAudio
            #audio = pyaudio.PyAudio()
            #attend_stderr()

            cantidad_canales = 0
            indice = 0
            sys.stdout.flush()
##            print(audio.get_device_info_by_index(0)['defaultSampleRate'])
##            sys.stdout.flush()
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
            #Debe mantenerse en 48000 (Hz) para que funcione bien
            #Lo normal es que deberia ser 44100 acorde al comando audio.get_device_info_by_index(0)['defaultSampleRate']
            RATE = 48000
            #Si hay un error de Input Overflow se debe aumentar el valor de
            #CHUNK, su valor siempre debe ser una potencia de 2
            CHUNK = 8192
            global RECORD_SECONDS
            TIME_OUT = int(RATE / CHUNK * RECORD_SECONDS)
            AMPLIFICACION_DE_SEGUNDOS_EN_TIME_OUT = int(TIME_OUT/RECORD_SECONDS)
            global THRESHOLD
            global SECONDS_IN_SILENCE
            SECONDS_IN_SILENCE_AUX = SECONDS_IN_SILENCE * AMPLIFICACION_DE_SEGUNDOS_EN_TIME_OUT
            WAVE_OUTPUT_FILENAME = "grabacion.wav"

            SHORT_NORMALIZE = (1.0/32768.0)
            SIGNAL_WIDTH = 2

            global speech_lock
            speech_lock = True
            

            def root_mean_square(frame):
                cantidad = len(frame)/SIGNAL_WIDTH
                formato = "%dh"%(cantidad)
                muestras = struct.unpack(formato, frame) #frame is a string. unpack return values unpacked according to the given format

                suma_de_cuadrados = 0.0
                for muestra in muestras:
                    muestra_normalizada = muestra * SHORT_NORMALIZE
                    suma_de_cuadrados += muestra_normalizada*muestra_normalizada
                    media_cuadratica = math.pow(suma_de_cuadrados/cantidad,0.5)
                    return media_cuadratica * 1000


            # start Recording
            
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                input_device_index = DEVICE_INDEX,
                            rate=RATE, input=True, output=False,
                            frames_per_buffer=CHUNK)
            print("-"*20 + "recording for " + str(RECORD_SECONDS) + " seconds" + "-"*20)
            

            import time
            global cantidad_de_veces_mas_rapido
            
            factor = 5
            toolbar_width = int(RECORD_SECONDS/cantidad_de_veces_mas_rapido) * factor * cantidad_de_veces_mas_rapido
            # setup toolbar
            sys.stdout.write("[%s]" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

            cantidad_a_actualizar = int(RECORD_SECONDS/cantidad_de_veces_mas_rapido)
            #momento_de_actualizar = int(RATE / CHUNK * RECORD_SECONDS / factor / cantidad_de_veces_mas_rapido)
            momento_de_actualizar = int(RATE / CHUNK * RECORD_SECONDS) / float(int(toolbar_width / cantidad_a_actualizar))
            frames = []
            contador = 1
            hubo_una_voz = 0
            segundos_en_silencio = 0
            for i in range(0, TIME_OUT):
                try:
                    data = stream.read(CHUNK)
                    valor_del_rms = root_mean_square(data)
                    #print(valor_del_rms)
                    #if valor_del_rms > THRESHOLD:
                    #    print(valor_del_rms, "VOICE")
                    #else:
                    #    print(valor_del_rms, "NO VOICE")

                    #Check if exist a voice
                    if (hubo_una_voz == 0) and (valor_del_rms > THRESHOLD):
                        #print("voz detectada")
                        hubo_una_voz = 1
                        #print("comienza a grabar")
                    
                    #print("appending data")
                    frames.append(data)
                        
                    #If someone is talking then set SECONDS_IN_SILENCE to zero
                    if (hubo_una_voz == 1) and (valor_del_rms > THRESHOLD):
                        #print("volvio a hablar")
                        segundos_en_silencio = 0
                    
                    if i < momento_de_actualizar*contador <= (i+1):
                        # update the bar
                        contador += 1
                        sys.stdout.write("-"*cantidad_a_actualizar)
                        sys.stdout.flush()

                    #If someone talked and now exist silence start counting SECONDS_IN_SILENCE
                    #print("seconds in silence", segundos_en_silencio, SECONDS_IN_SILENCE_AUX)
                    if (hubo_una_voz == 1) and (valor_del_rms <= THRESHOLD):
                        #print("silencio detectado")
                        segundos_en_silencio += 1
                        
                        if segundos_en_silencio >= SECONDS_IN_SILENCE_AUX:
                            #print("break")
                            break
                except:
                    continue

            sys.stdout.write("\n")
            sys.stdout.flush()
            print("-"*20 + "finished recording" + "-"*20)
            
            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            

            if hubo_una_voz == 0:
                print("No voice detected")
            else:
            
                #Save to a file
                waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(audio.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(frames))
                waveFile.close()


                import speech_recognition as sr
                import sys
                global my_key_api
                global setting_language
                self.is_recognized = False

                audio_grabado = sr.AudioFile("grabacion.wav")
                r = sr.Recognizer()
                with audio_grabado as source:
                  audio = r.record(source)
                  try:
                    text = r.recognize_google(audio,language=setting_language)
                    print("From Google you said : {}".format(text))
                    sys.stdout.flush()
                    print("flushed")
                    self.publish_message(text)
                    print("publish_message called")
                    self.is_recognized = True
                  except sr.UnknownValueError:
                    print("Speech not recognised")
                    sys.stdout.flush()
                  except Exception as e: 
                    print("Could not request results from Google Speech Recognition service (1)")
                    print(e)
                    sys.stdout.flush()
                    
                    try:
                      text = r.recognize_google(audio,language=setting_language,key=my_key_api)
                      print("From Google you said : {}".format(text))
                      sys.stdout.flush()
                      self.publish_message(text)
                      self.is_recognized = True
                    except sr.UnknownValueError:
                      print("Speech not recognised")
                      sys.stdout.flush()
                    except:
                      print("Could not request results from Google Speech Recognition service (2)")
                      sys.stdout.flush()
                      
                      try:
                        text = r.recognize_sphinx(audio,language=setting_language)
                        print("From Sphinx you said : {}".format(text))
                        sys.stdout.flush()
                        self.publish_message(text)
                        self.is_recognized = True
                      except sr.UnknownValueError:
                        print("Speech not recognised")
                        sys.stdout.flush()
                      except:
                        print("Could not request results from Sphinx")
                        sys.stdout.flush()


            self.on_recognition_finished()
            #print("speech_lock google before", speech_lock)
            speech_lock = False
            #print("speech_lock google after", speech_lock)


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
