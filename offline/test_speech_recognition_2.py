import sys
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
  audio = r.listen(source)
  try:
    text = r.recognize_google(audio, language = "en-US")
    print("From Google you said : {}".format(text))
    sys.stdout.flush()

    text = r.recognize_sphinx(audio, language = "en-US")
    print("From Sphinx you said : {}".format(text))
    sys.stdout.flush()
  except sr.UnknownValueError:
    print("Sorry could not recognize your voice")
    sys.stdout.flush()
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    sys.stdout.flush()
