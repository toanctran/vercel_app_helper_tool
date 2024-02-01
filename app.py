from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from pydantic import Field
import os

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

class GoogleSearchData(BaseModel):
    query: str
    num_results: int
    lang: str

@app.post("/get_google_search")
def get_google_search(request_data: GoogleSearchData):
    """
    Endpoint to perform Google searches and retrieving search results.
    """
     # Perform the Google search
    search_results = search(request_data.query, num_results=request_data.num_results, lang=request_data.lang, advanced=True)
    return {
        "search_results" : search_results
    }


class ScrapeRequestData(BaseModel):
    url: str

@app.post("/scrape_site")
def get_website_content(request_data: ScrapeRequestData):
    """
    Endpoint to get the website content.
    """
    response = requests.get(request_data.url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        content = str(text_content)
        return {"content":content}
    else:
        return {"error":  str(f"Failed to fetch the URL {request_data.url}")}
    

class GoogleSearchData(BaseModel):
    query: str
    num_results: int
    lang: str

@app.post("/get_google_search")
def get_google_search(request_data: GoogleSearchData):
    """
    Endpoint to perform Google searches and retrieving search results.
    """
     # Perform the Google search
    search_results = search(request_data.query, num_results=request_data.num_results, lang=request_data.lang, advanced=True)
    for result in search_results:
        result['content'] = get_website_content(result['url'])
    return {
        "search_results" : search_results
    }