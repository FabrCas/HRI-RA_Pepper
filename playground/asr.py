import speech_recognition as sr
import difflib

# Define your vocabulary (one for each type of vocal interaction)
vocab_test= ['hello', 'goodbye', 'yes', 'no']

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        print("You said:", recognized_text)

        # Find the closest matching term from the vocabulary
        best_match = difflib.get_close_matches(recognized_text.lower(), vocab_test, n=1, cutoff=0.6)

        if best_match:
            return best_match[0]
        else:
            return "Unknown"

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)

if __name__ == "__main__":
    while True:
        response = recognize_speech()
        print("Response:", response)
