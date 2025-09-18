import os
import csv
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

def analyze_transcript(transcript):
    """Analyze transcript using Groq API"""
    if not client:
        return None, "Error: Groq client not initialized"
    
    try:
        # Create a specific prompt for summarization and sentiment analysis
        prompt = f"""
        Analyze this customer service transcript and provide:
        1. A concise 2-3 sentence summary
        2. The customer's sentiment (positive, neutral, or negative)
        
        Format your response exactly as:
        SUMMARY: [summary here]
        SENTIMENT: [sentiment here]
        
        Only use "positive", "neutral", or "negative" for the sentiment.
        
        Transcript:
        {transcript}
        """
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.3,
            max_tokens=300,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Parse the response more robustly
        summary = None
        sentiment = None
        
        # Split response by lines
        lines = response.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if line_lower.startswith("summary:"):
                summary = line.split(":", 1)[1].strip()
            elif line_lower.startswith("sentiment:"):
                sentiment_text = line.split(":", 1)[1].strip().lower()
                
                if "positive" in sentiment_text:
                    sentiment = "positive"
                elif "neutral" in sentiment_text:
                    sentiment = "neutral"
                elif "negative" in sentiment_text:
                    sentiment = "negative"
        
        # If we couldn't parse sentiment, try to find it in the entire response
        if not sentiment:
            if "positive" in response.lower():
                sentiment = "positive"
            elif "neutral" in response.lower():
                sentiment = "neutral"
            elif "negative" in response.lower():
                sentiment = "negative"
            else:
                sentiment = "unknown"
        
        return summary, sentiment
        
    except Exception as e:
        return None, f"Error analyzing transcript: {str(e)}"

def save_to_csv(transcript, summary, sentiment):
    """Save analysis results to CSV file"""
    file_exists = os.path.isfile('call_analysis.csv')
    
    with open('call_analysis.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Transcript', 'Summary', 'Sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Transcript': transcript,
            'Summary': summary,
            'Sentiment': sentiment
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    transcript = request.form.get('transcript', '')
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'})
    
    summary, sentiment = analyze_transcript(transcript)
    
    if summary is None:
        return jsonify({'error': sentiment})
    
    # Save to CSV
    save_to_csv(transcript, summary, sentiment)
    
    return jsonify({
        'transcript': transcript,
        'summary': summary,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)