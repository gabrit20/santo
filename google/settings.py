language_out = "EN" #"IT" #"ES" #"EN" #"DE"
language_in = 'en-GB'   #'en-GB' #de-DE #en-US #ja-JP #it-IT #es-PE  #see http://www.lingoes.net/en/translator/langcode.htm

gender = "m"

#initial state
#state = "standby"#
state = "enquiry"


#must be the same
recordingTime = 7
sox_time = "07"

maxWaitingCycles = 15 #the total waiting time is given by maxWaitingCycles*recordingTime

import time
timeInfo = time.localtime(time.time())
month = timeInfo[1]
day = timeInfo[2]




