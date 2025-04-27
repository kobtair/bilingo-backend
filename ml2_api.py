import requests
import jieba
from pypinyin import pinyin, Style
import warnings
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance
import os
import tempfile

warnings.filterwarnings('ignore')

WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"
API_KEY = os.getenv("OPENAI_API")  # Replace with your actual API key

def download_file_from_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download file from URL: {response.status_code} - {response.text}")

def transcribe_audio_api(audio_source):
    if audio_source.startswith("http://") or audio_source.startswith("https://"):
        tmp_path = os.path.join(tempfile.gettempdir(), "temp_audio_file.wav")
        download_file_from_url(audio_source, tmp_path)
        audio_source = tmp_path

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    files = {
        "file": open(audio_source, "rb"),
        "model": (None, "whisper-1"),
        "language": (None, "zh")
    }
    response = requests.post(WHISPER_API_URL, headers=headers, files=files)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        raise Exception(f"Whisper API error: {response.status_code} - {response.text}")

def segment_language(text):
    return " ".join(jieba.cut(text))

def text_to_phonetics(text):
    words = segment_language(text)
    pinyin_transcription = pinyin(words, style=Style.TONE3, heteronym=False)
    return " ".join([syllable[0] for syllable in pinyin_transcription])

def text_to_plain_phonetics(text):
    words = segment_language(text)
    pinyin_transcription = pinyin(words, style=Style.NORMAL, heteronym=False)
    return " ".join([syllable[0] for syllable in pinyin_transcription])

def compare_phonetics(phonetics1, phonetics2):
    ratio = SequenceMatcher(None, phonetics1, phonetics2).ratio()
    lev_dist = levenshtein_distance(phonetics1, phonetics2)
    return {
        "similarity_ratio": ratio,
        "levenshtein_distance": lev_dist
    }
