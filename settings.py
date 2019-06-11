#More information about languages could be found in;
#https://www.science.co.il/language/Locale-codes.php
language_out = "ES" #"IT" #"ES" #"EN" #"DE"
language_in = 'es-PE'   #'en-GB' #de-DE #en-US #ja-JP #it-IT #es-PE  #see http://www.lingoes.net/en/translator/langcode.htm
language_list = ["IT","ES","EN","DE"]

gender = "m"

#initial state
#state = "standby"#
state = "enquiry"


#must be the same
recordingTime = 15
sox_time = "15"
cantidad_de_veces_mas_rapido = 2

#El ruido en el ambiente debe superar threshold dB para ser considerado como una voz, caso contrario se considera silencio
threshold = 0.08

#Si hay SECONDS_IN_SILENCE segundos seguidos de silencio se detiene de grabar
seconds_in_silence = 1.5 #3

maxWaitingCycles = 5 #the total waiting time is given by maxWaitingCycles*recordingTime

speech_lock = False

import time
timeInfo = time.localtime(time.time())
year = timeInfo[0]
month = timeInfo[1]
day = timeInfo[2]
smonth = str(month)
sday = str(day)
hour = timeInfo[3]
minute = timeInfo[4]
shour = str(hour)
sminute = str(minute)


import os
my_key_api = os.getenv("MY_OWN_KEY")


