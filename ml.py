#Deprecated: Use ml2.py logic instead.

import whisper
import jieba
from pypinyin import pinyin, Style
import warnings
warnings.filterwarnings('ignore')

from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance

def transcribe_audio(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file, language="zh")
    return result["text"]

def segment_mandarin(text):
    return " ".join(jieba.cut(text))

def text_to_pinyin(text):
    words = segment_mandarin(text)
    pinyin_transcription = pinyin(words, style=Style.TONE3, heteronym=False)
    return " ".join([syllable[0] for syllable in pinyin_transcription])

def simplify_pinyin(pinyin_text):
    pinyin_mapping = {
        "1": "1", "2": "2", "3": "3", "4": "4", "5": "",
        "ā": "a1", "á": "a2", "ǎ": "a3", "à": "a4",
        "ē": "e1", "é": "e2", "ě": "e3", "è": "e4",
        "ī": "i1", "í": "i2", "ǐ": "i3", "ì": "i4",
        "ō": "o1", "ó": "o2", "ǒ": "o3", "ò": "o4",
        "ū": "u1", "ú": "u2", "ǔ": "u3", "ù": "u4",
        "ǖ": "ü1", "ǘ": "ü2", "ǚ": "ü3", "ǜ": "ü4"
    }
    for pinyin_char, simple_char in pinyin_mapping.items():
        pinyin_text = pinyin_text.replace(pinyin_char, simple_char)
    return pinyin_text

def compare_phonetics(phonetics1, phonetics2):
    ratio = SequenceMatcher(None, phonetics1, phonetics2).ratio()
    lev_dist = levenshtein_distance(phonetics1, phonetics2)
    print("\n🔍 **Phonetic Comparison Results** 🔍")
    print(f"🔹 **Similarity Ratio:** {ratio:.2%}")
    print(f"🔹 **Levenshtein Distance:** {lev_dist} changes required")
    print("\n🔹 **Differences Highlighted:**")
    for word1, word2 in zip(phonetics1.split(), phonetics2.split()):
        if word1 != word2:
            print(f" ✅{word1}  →  ❌ {word2}")
