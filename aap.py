import gradio as gr
from utils import get_news_links, get_sentiment, summarize_text, extract_topics, text_to_speech_hindi

def process_company_news(company):
    articles = get_news_links(company)
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    report_text = f"Company: {company}\n\n"
    report_data = []

    for idx, article in enumerate(articles, 1):
        summary = summarize_text(article['summary'])
        sentiment = get_sentiment(article['summary'])
        topics = extract_topics(article['summary'])

        sentiment_distribution[sentiment] += 1
        report_text += f"{idx}. {article['title']}\nSummary: {summary}\nSentiment: {sentiment}\nTopics: {', '.join(topics)}\n\n"

        report_data.append([article['title'], summary, sentiment, ', '.join(topics)])

    final_summary = f"{company} की समाचार कवरेज इस प्रकार है:\nसकारात्मक: {sentiment_distribution['Positive']}, नकारात्मक: {sentiment_distribution['Negative']}, तटस्थ: {sentiment_distribution['Neutral']}।"
    audio_path = text_to_speech_hindi(final_summary, output_file="assets/summary_hi.mp3")

    return report_data, sentiment_distribution, final_summary, audio_path

with gr.Blocks() as demo:
    gr.Markdown("# 📊 News Summarization + Sentiment + Hindi TTS App")
    company_input = gr.Textbox(label="Enter Company Name", placeholder="e.g., Tesla")

    btn = gr.Button("Analyze News")
    output_table = gr.Dataframe(headers=["Title", "Summary", "Sentiment", "Topics"], label="Article Analysis")
    sentiment_output = gr.Label(label="Sentiment Distribution")
    final_summary_output = gr.Textbox(label="Hindi Summary")
    audio_output = gr.Audio(label="Hindi Audio Summary")

    btn.click(fn=process_company_news,
              inputs=[company_input],
              outputs=[output_table, sentiment_output, final_summary_output, audio_output])

if __name__ == "__main__":
    demo.launch()
