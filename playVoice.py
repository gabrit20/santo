#coding: utf-8

import alsaaudio
import pygame
from pygame.mixer import music

import sys
sys.path.insert(0, './vocalware_python')
from vocalware import saveAudio

import alltext



def playVoice(language, textID):


    #stop=0
    m = alsaaudio.Mixer('PCM')
    m.setvolume(100) #95
    pygame.mixer.init()

    try:
        pygame.mixer.music.load('../audio/' + 'Language'+language+'/'+textID+'.mp3') #.wav
        pygame.mixer.music.play()
        #print("play")

    except pygame.error:
        print("Calling TTS")
        riga = alltext.text[textID]
        print(riga)
        print(alltext.text[textID][0])
            #engineID, languageID, voiceID, effectID, effectStrength
        if (language == 'IT'):
            #Matteo duration longer 2, 7, 8, 'D', 2
            #Luca duration longer 2, 7, 5, 'D', 2
            #Roberto duration longer 3, 7, 2, 'D', 2
            saveAudio(2, 7, 8, 'D', 2, audio_text=alltext.text[textID][0], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'ES'):
            #Francisco duration longer 3 2 2
            #Carlos duration longer 2 2 7  
            #saveAudio(3, 2, 2, 'd', 2, 'Hola señora', audio_filename='Language'+language+'/'+textID)
            saveAudio(3, 2, 2, 'D', 1, audio_text=alltext.text[textID][1], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'EN'):
            #Simon duration longer
            saveAudio(2, 1, 5, 'D', 2, audio_text=alltext.text[textID][2], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'DE'):
            #Tim duration longer
            saveAudio(2, 3, 2, 'D', 2, audio_text=alltext.text[textID][3], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        

        pygame.mixer.music.load('../audio/' + 'Language'+language+'/'+textID+'.mp3')
        #pygame.mixer.music.load('new_audio.mp3')
        pygame.mixer.music.play()


    finally:
        #Sprint("finally")
        pygame.mixer.music.set_volume(1.0)
        #if(stop==0):
        while pygame.mixer.music.get_busy()==True:
            continue


#playVoice('EN', 'text')







        
