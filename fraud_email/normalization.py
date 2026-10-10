import re
import unicodedata

# NFKC alone does not normalize all cross-script homoglyphs.
CONFUSABLES = str.maketrans({"а":"a", "е":"e", "о":"o", "р":"p", "с":"c", "і":"i", "Α":"A", "Ο":"O", "Ｅ":"E"})

def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "").translate(CONFUSABLES)
    value = re.sub(r"[\\u200b-\\u200f\\ufeff]", "", value)
    return re.sub(r"\\s+", " ", value).strip().casefold()
