from flask import Flask, request, jsonify
from utils import get_news_links, get_sentiment, summarize_text, extract_topics, text_to_speech_hindi

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_news():
    data = request.get_json()
    company = data.get('company')
    articles = get_news_links(company)

    report = {"Company": company, "Articles": []}
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        summary = summarize_text(article['summary'])
        sentiment = get_sentiment(article['summary'])
        topics = extract_topics(article['summary'])

        sentiment_distribution[sentiment] += 1

        report["Articles"].append({
            "Title": article['title'],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topics
        })

    # Comparative analysis (simple)
    report["Comparative Sentiment Score"] = {
        "Sentiment Distribution": sentiment_distribution
    }

    final_text = f"{company} की समाचार कवरेज इस प्रकार है। सकारात्मक: {sentiment_distribution['Positive']}, नकारात्मक: {sentiment_distribution['Negative']}, तटस्थ: {sentiment_distribution['Neutral']}।"
    audio_file = text_to_speech_hindi(final_text)
    report["Audio"] = audio_file

    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)
