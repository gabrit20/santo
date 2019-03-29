#coding: utf-8

import alsaaudio
import pygame
from pygame.mixer import music

import sys
sys.path.insert(0, './vocalware_python')
from vocalware import saveAudio

import alltext



def playDict(language, textID, dictionary):


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
        print(dictionary)
            
        filename = '../audio/' + 'Language'+language+'/'+textID
        
        
        if (language == 'IT'):
            #engineID, languageID, voiceID, effectID, effectStrength
            #Matteo duration longer 2, 7, 8, 'D', 2
            #Luca duration longer 2, 7, 5, 'D', 2
            #Roberto duration longer 3, 7, 2, 'D', 2
            saveAudio(2, 7, 8, 'D', 2, audio_text=dictionary[language], audio_filename=filename)
        elif (language == 'ES'):
            #Francisco duration longer 3 2 2
            #Carlos duration longer 2 2 7  
            #saveAudio(3, 2, 2, 'd', 2, 'Hola señora', audio_filename='Language'+language+'/'+textID)
            saveAudio(2, 2, 7, 'D', 1, audio_text=dictionary[language], audio_filename=filename)
        elif (language == 'EN'):
            #Simon duration longer
            saveAudio(2, 1, 5, 'D', 2, audio_text=dictionary[language], audio_filename=filename)
        elif (language == 'DE'):
            #Tim duration longer
            saveAudio(2, 3, 2, 'D', 2, audio_text=dictionary[language], audio_filename=filename)
        

        pygame.mixer.music.load('../audio/' + 'Language'+language+'/'+textID+'.mp3')
        #pygame.mixer.music.load('new_audio.mp3')
        pygame.mixer.music.play()


    finally:
        #Sprint("finally")
        pygame.mixer.music.set_volume(1.0)
        #if(stop==0):
        while pygame.mixer.music.get_busy()==True:
            continue


#playText('EN', 'text')


def playList(language, textID, archive, row, column):


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
            #engineID, languageID, voiceID, effectID, effectStrength
        if (language == 'IT'):
            #Matteo duration longer 2, 7, 8, 'D', 2
            #Luca duration longer 2, 7, 5, 'D', 2
            #Roberto duration longer 3, 7, 2, 'D', 2
            saveAudio(2, 7, 8, 'D', 2, audio_text=archive[row][column], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'ES'):
            #Francisco duration longer 3 2 2
            #Carlos duration longer 2 2 7  
            #saveAudio(3, 2, 2, 'd', 2, 'Hola señora', audio_filename='Language'+language+'/'+textID)
            saveAudio(2, 2, 7, 'D', 1, audio_text=archive[row][column], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'EN'):
            #Simon duration longer
            saveAudio(2, 1, 5, 'D', 2, audio_text=archive[row][column], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        elif (language == 'DE'):
            #Tim duration longer
            saveAudio(2, 3, 2, 'D', 2, audio_text=archive[row][column], audio_filename='../audio/' + 'Language'+language+'/'+textID)
        

        pygame.mixer.music.load('../audio/' + 'Language'+language+'/'+textID+'.mp3')
        #pygame.mixer.music.load('new_audio.mp3')
        pygame.mixer.music.play()


    finally:
        #Sprint("finally")
        pygame.mixer.music.set_volume(1.0)
        #if(stop==0):
        while pygame.mixer.music.get_busy()==True:
            continue




def playWave(filename):


    #stop=0
    m = alsaaudio.Mixer('PCM')
    m.setvolume(95)
    pygame.mixer.init()

    try:
        pygame.mixer.music.load('../audio/' + filename + '.wav')
        pygame.mixer.music.play()

    except pygame.error:
        print("File not found")
 

    finally:
        pygame.mixer.music.set_volume(1.0)
        #if(stop==0):
        #    while pygame.mixer.music.get_busy()==True:
        #        continue
        while pygame.mixer.music.get_busy()==True:
            continue



        
