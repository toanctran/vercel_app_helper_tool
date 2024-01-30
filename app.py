from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

class TextData(BaseModel):
    text: str

def word_count(text: str):
    sentences = re.split(r'[.!?]', text)
    word_counts = [len(sentence.split()) for sentence in sentences if sentence]

    total_words = sum(word_counts)
    average_words_per_sentence = total_words / len(word_counts) if word_counts else 0
    words_in_longest_sentence = max(word_counts, default=0)

    return {
        "Total words": total_words,
        "Average words per sentence": average_words_per_sentence,
        "Number of words in Longest sentence": words_in_longest_sentence
    }

@app.post("/word-count/")
def analyze_text_endpoint(text_data: TextData):
    return word_count(text_data.text)
