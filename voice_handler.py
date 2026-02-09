# voice_handler.py

import speech_recognition as sr
from io import BytesIO

def transcribe_audio(audio_file) -> str:
    """
    Transcribes audio file to text using Google Speech Recognition
    """
    try:
        recognizer = sr.Recognizer()
        
        # Read audio file
        audio_data = sr.AudioFile(audio_file)
        
        with audio_data as source:
            audio = recognizer.record(source)
        
        # Transcribe
        text = recognizer.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {str(e)}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"


def transcribe_audio_bytes(audio_bytes, language="en-US") -> str:
    """
    Transcribes audio bytes to text
    """
    try:
        recognizer = sr.Recognizer()
        
        # Convert bytes to audio
        audio_file = BytesIO(audio_bytes)
        audio_data = sr.AudioFile(audio_file)
        
        with audio_data as source:
            audio = recognizer.record(source)
        
        # Map language codes
        lang_map = {
            "🇬🇧 English": "en-US",
            "🇮🇳 हिंदी": "hi-IN",
            "🇮🇳 தமிழ்": "ta-IN"
        }
        
        lang_code = lang_map.get(language, "en-US")
        
        # Transcribe with language
        text = recognizer.recognize_google(audio, language=lang_code)
        return text
        
    except Exception as e:
        return f"Error: {str(e)}"
