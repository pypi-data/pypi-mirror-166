from textblob import TextBlob

from .errors import ArgumentError


def correction(data):
    if not isinstance(data, str):
        raise ArgumentError("No text input provided!")
    text = TextBlob(data)
    text = text.correct()
    return text
