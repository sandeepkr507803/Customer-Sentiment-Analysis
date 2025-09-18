# Customer Sentiment Analysis Tool
A Flask web application that analyzes customer call transcripts using the Groq API.

## Features
- Accepts customer call transcripts via a web interface
- Uses Groq API to:
  - Summarize the conversation in 2-3 sentences
  - Extract customer sentiment (positive/neutral/negative)
- Displays the original transcript, summary, and sentiment
- Saves results to a CSV file

## Setup
1. Clone or download this project
2. Install dependencies:
   - pip install -r requirements.txt
3. Set your Groq API key as an environment variable:
   - create a `.env` file in the project root:
   - Add GROQ_API_KEY="your_api_key_here" and replace your_api_key_here with your Groq API Key

## Usage
1. Run the application:
   - python app.py
2. Open your browser and go to `http://localhost:5000`
3. Paste a customer call transcript into the text area
4. Click "Analyze Transcript"
5. View the results and check `call_analysis.csv` for the saved analysis
