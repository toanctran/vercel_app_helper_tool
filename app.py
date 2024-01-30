from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

@app.get("/")
async def root():
  return{"message":"Created by Tran Chi Toan - chitoantran@gmail.com"}

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


class SpeakingData(BaseModel):
    speaking_rate: int
    text_length: int

def calculate_speaking_time(speaking_rate: int, text_length: int):
    """
    Use to calculate speaking time in second based on the speaking rate in WPM and the length of text
    """
    speaking_time =  (text_length / speaking_rate) * 60
    return {
        "Speaking time" : round(speaking_time)
    }

@app.post("/words_count/")
def analyze_text_endpoint(text_data: TextData):
    """
    Endpoint use to count the words in provided text.
    """
    return word_count(text_data.text)

@app.post("/get_speaking_time_in_seconds/")
def analyze_speaking_time(request_data: SpeakingData):
    """
    Endpoint use to calculate the speaking time in second using the speaking rate in WPM and the total word numbers of the text.
    """
    return calculate_speaking_time(request_data.speaking_rate, request_data.text_length)


