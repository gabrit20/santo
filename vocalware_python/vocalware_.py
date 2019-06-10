#coding: utf-8
from collections import namedtuple
import hashlib
import requests
import urllib


def generateURLNaive(engine_id, language_id, voice_id, effect_type, effect_level, audio_text):
	url = 'https://www.vocalware.com/support/rest-api-example'

	data = {
		'EID': engine_id,
		'LID': language_id,
		'VID': voice_id,
		'FX_TYPE': effect_type,
		'FX_LEVEL': effect_level,
		'TXT': audio_text,
		'ACC': 6962334,
		'API': 2646659,
		'SECRET': 'c8b4c03589f1502cfeb9b9aa05d3ec54'
	}

	headers = {
		'cookie': 'PHPSESSID=60637c5371bed0eda930f0b19632d640; __utmc=102778375; __utmz=102778375.1551757900.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=102778375.2119135101.1551757900.1551759864.1552182660.3; __utmt=1; VW=userId%3D7355614%7Cemail%3Djavier.cerna%40pucp.pe%7Crole%3D2%7CaccId%3D6962334%7Cfname%3DJavier%7Clname%3DCerna%7CphpSessId%3Df9a1c3911b6efac476d33ba72525bf92%7CtmpPass%3D25a3a31cc62257078198b454222ac3d9%7CdailyAvg%3D0%7CCurrentStreams%3D926; sdmenu_my_menu=0010; __utmb=102778375.6.10.1552182660',
		'cache-control': 'no-cache',
	}

	response = requests.request("POST", url, data=data, headers=headers)
	
	return str(response.json()['DATA'])


def generateChecksum(data):
	m = hashlib.md5()
	m.update(''.join([str(d.value) for d in data]))
	return m.hexdigest()


def generateURL(engine_id, language_id, voice_id, effect_type, effect_level, audio_text):
	OrderedDict = namedtuple('OrderedDict', ['key', 'value'])

	data = [
		OrderedDict('EID', engine_id),
		OrderedDict('LID', language_id),
		OrderedDict('VID', voice_id),
		OrderedDict('TXT', audio_text),
		OrderedDict('EXT', 'mp3'),
		OrderedDict('FX_TYPE', effect_type),
		OrderedDict('FX_LEVEL', effect_level),
		OrderedDict('ACC', 6969626),
		OrderedDict('API', 2647432),
                OrderedDict('HTTP_ERR', 1),
		OrderedDict('SECRET', '8ce1aa6ea1c5ab9214313cd9d41d76b3')
                #Javier
                #OrderedDict('ACC', 6962334),
		#OrderedDict('API', 2646659),
		#OrderedDict('SECRET', 'c8b4c03589f1502cfeb9b9aa05d3ec54')
                
		
	]

	checksum = OrderedDict('CS', generateChecksum(data))
	
	url = 'https://www.vocalware.com/tts/gen.php?' + ''.join(['%s=%s&' % (d.key, d.value) for d in data])
	return url + '%s=%s' % (checksum.key, checksum.value)


def saveAudio(engine_id, language_id, voice_id, effect_type, effect_level, 
				audio_text='Hello, this is a new audio', audio_filename='audio'):

##        engine_id = 3
##        language_id = 1
##        voice_id = 5
##        effect_type = 'D'
##        effect_level = 2
##        
##        
##        audio_text = "I'm sorry, I could not hear you" #fails
##        audio_text = "I`m really really sorry" #works
##        audio_text = "I'm sorry, I could not hear" #works
##        audio_text = "Today, it's the sixtheenth of May" #fails
##        audio_text = "Today, it's the sixth of May" #works
##        audio_text = "I'm sorry, I could not hear you" #fails
##
	print("TEXT", audio_text)
	#audio_text = urllib.quote_plus(audio_text)
	#print("urllib.quote_plus", audio_text)
	audio_url = generateURL(engine_id, language_id, voice_id, effect_type, effect_level, audio_text)
	#print("audio_url", audio_url)
	#audio_url = urllib.urlencode(audio_url)
	print("audio_url", audio_url)
	audio_file = requests.get(audio_url)

	with open(audio_filename + '.mp3', 'wb') as f:
		f.write(audio_file.content)
	
	print('New audio "' + audio_filename + '.mp3" saved successfully')


#def main():        
if __name__ == '__main__':
#	saveAudio(engine_id=3, language_id=2, voice_id=3, effect_type='P', effect_level=1,
#				audio_text='Hola señora', audio_filename='new_audio')
	saveAudio(engine_id=2, language_id=7, voice_id=8, effect_type='P', effect_level=2,
				audio_text='Vieni bello', audio_filename='new_audio')





