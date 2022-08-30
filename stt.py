import speech_recognition as sr
import ffmpy
import logging
import os

from bot_config import LANG

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def process_audio(audio_file):
    """
    Downloads and converts an audio file and return the text
    """
    audio_path = download_file(audio_file)
    new_audio_path = convert_file(audio_path)
    try:
        result = stt(new_audio_path)
    except Exception as e:
        logger.error(e)
        result = None
    os.remove(audio_path)
    os.remove(new_audio_path)
    return result

def stt(audio_path):
    """
    Speech to text using Google Speech Recognition
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language=LANG)
    return result

def convert_file(audio_path):
    """
    Converts an audio file to a wav file
    """
    output_path = f'{audio_path[:audio_path.rindex(".")]}wav'
    ff = ffmpy.FFmpeg(inputs={audio_path: None}, outputs={output_path: '-y'})
    ff.run()
    return output_path

def download_file(audio_file):
    """
    Downloads a telegram audio file
    """
    extension = audio_file['file_path'][audio_file['file_path'].rindex('.'):]
    new_file_path = f'tmp/{audio_file["file_unique_id"]}.{extension}'
    audio_file.download(new_file_path)
    return new_file_path