import alsaaudio
import pygame
from pygame.mixer import music


def playWave(filename):


    #stop=0
    m = alsaaudio.Mixer('PCM')
    m.setvolume(95)
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(filename + '.wav')
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







        
