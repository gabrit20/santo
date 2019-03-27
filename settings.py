#More information about languages could be found in;
#https://www.science.co.il/language/Locale-codes.php
language_out = "ES" #"IT" #"ES" #"EN" #"DE"
language_in = 'es-PE'   #'en-GB' #de-DE #en-US #ja-JP #it-IT #es-PE  #see http://www.lingoes.net/en/translator/langcode.htm

gender = "m"

#initial state
#state = "standby"#
state = "enquiry"


#must be the same
recordingTime = 5
sox_time = "05"
cantidad_de_veces_mas_rapido = 2

maxWaitingCycles = 15 #the total waiting time is given by maxWaitingCycles*recordingTime

import time
timeInfo = time.localtime(time.time())
month = timeInfo[1]
day = timeInfo[2]

import os
my_key_api = os.getenv("MY_OWN_KEY")


