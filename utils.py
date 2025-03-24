import requests
from bs4 import BeautifulSoup

def get_news_links(company, max_articles=10):
    search_query = company.replace(' ', '+')
    url = f"https://www.google.com/search?q={search_query}+news&tbm=nws"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    results = soup.select('div.dbsr')  # For Google News search results
    count = 0

    for result in results:
        if count >= max_articles:
            break
        title = result.select_one('div.JheGif.nDgy9d').text
        link = result.a['href']
        snippet = result.select_one('div.Y3v8qd').text if result.select_one('div.Y3v8qd') else ""
        articles.append({
            'title': title,
            'link': link,
            'summary': snippet
        })
        count += 1

    return articles


from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def get_sentiment(text):
    result = sentiment_model(text[:512])  # Keep text short for fast inference
    label = result[0]['label']
    if label == 'POSITIVE':
        return 'Positive'
    elif label == 'NEGATIVE':
        return 'Negative'
    else:
        return 'Neutral'


from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    if len(text.split()) < 30:
        return text  # Skip short texts
    summary = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']


from keybert import KeyBERT

kw_model = KeyBERT()

def extract_topics(text, top_n=5):
    keywords = kw_model.extract_keywords(text, top_n=top_n)
    return [kw[0] for kw in keywords]


from gtts import gTTS
import os

def text_to_speech_hindi(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang='hi')
    tts.save(output_file)
    return output_file
