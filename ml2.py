import whisper
import jieba
from pypinyin import pinyin, Style
import warnings
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance

warnings.filterwarnings('ignore')

def transcribe_audio(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file, language="zh")
    return result["text"]

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
    print("\n🔍 **Phonetic Comparison Results** 🔍")
    print(f"🔹 **Similarity Ratio:** {ratio:.2%}")
    print(f"🔹 **Levenshtein Distance:** {lev_dist} changes required")
    print("\n🔹 **Differences Highlighted:**")
    for word1, word2 in zip(phonetics1.split(), phonetics2.split()):
        if word1 != word2:
            print(f" ✅ {word1}  →  ❌ {word2}")

audio_file1 = "aud_1.wav"
audio_file2 = "saq_ch.mp3"


transcription1 = transcribe_audio(audio_file1)
pinyin_phonetics1 = text_to_phonetics(transcription1)
plain_pinyin1 = text_to_plain_phonetics(transcription1)

transcription2 = transcribe_audio(audio_file2)
pinyin_phonetics2 = text_to_phonetics(transcription2)
plain_pinyin2 = text_to_plain_phonetics(transcription2)


print("\n🎙 Audio 1 Transcription: ", transcription1)
print("🔠 Pinyin (with tone numbers): ", pinyin_phonetics1)
print("🧾 Phonetic (plain pinyin): ", plain_pinyin1)


print("\n🎙 Audio 2 Transcription: ", transcription2)
print("🔠 Pinyin (with tone numbers): ", pinyin_phonetics2)
print("🧾 Phonetic: ", plain_pinyin2)

compare_phonetics(plain_pinyin1, plain_pinyin2)
