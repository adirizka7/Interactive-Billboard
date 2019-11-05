import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)
    while True:
        try:
            audio = r.listen(source)
            transcript = r.recognize_google(audio, language='id')
            print(transcript)
        except sr.UnknownValueError:
            print("Value Error")
