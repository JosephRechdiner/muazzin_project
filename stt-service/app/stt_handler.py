from speech_recognition import Recognizer
import speech_recognition as sr

def get_text_from_speach(sr: sr, recognizer: Recognizer, file_path: str):
    """
    Supposed to extract text from audio
    """
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio_data=audio)
        return text
    except Exception as e:
        raise Exception(f"Could not get text from speach, Error: {str(e)}")