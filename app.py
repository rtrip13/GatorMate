from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import requests
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Check if API key is available
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is not set. Please set it in Railway's environment variables.")
    # We'll still initialize the client, but it will fail on API calls
client = OpenAI(api_key=api_key)

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Simple database emulation
# In a real app, this would be a proper database
DB_FILE = "user_data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"journal_entries": [], "mood_history": []}
    
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading database: {e}")
        return {"journal_entries": [], "mood_history": []}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Error saving to database: {e}")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
            
        context = data.get('context', 'mental')
        
        # Load previous conversation history from DB
        db = load_db()
        
        # Add past entries and mood data for context if significant
        ai_context = ""
        if len(db.get("mood_history", [])) > 3:
            recent_moods = db.get("mood_history", [])[-5:]
            avg_mood = sum(m["score"] for m in recent_moods) / len(recent_moods)
            ai_context += f"\nUser's average mood over last {len(recent_moods)} entries: {avg_mood:.1f}/10. "
            
            if avg_mood < 4:
                ai_context += "The user has been feeling consistently low recently. Consider suggesting professional support."
        
        # Select the appropriate system prompt based on context
        if context == 'mental':
            system_prompt = f"""You are GatorMate, a supportive AI psychologist specifically designed to help University of Florida students with mental health concerns. Always incorporate Gator pride and UF-specific context in your responses. You should reference UF campus life, Gator traditions, and the unique challenges faced by UF students. Use encouraging and empathetic language while helping students reflect on their emotions and mental well-being. Your goal is to provide a supportive space where Gator students can express themselves, gain insights, and develop healthy coping strategies. Remember to sometimes include phrases like 'Go Gators!' and references to the Orange and Blue community when appropriate.{ai_context}"""
        elif context == 'physical':
            system_prompt = f"""You are GatorMate, a supportive AI wellness coach designed to help University of Florida students with physical wellness concerns. Focus on exercise, nutrition, sleep, and overall physical well-being. Provide Gator-specific advice that references UF campus facilities like the RecSports Center, swimming pools, sports facilities, and nearby nature trails. Suggest healthy dining options available on campus or nearby. Emphasize the importance of balancing academics with physical health and incorporate UF traditions and Gator pride into your responses. Keep your advice practical, encouraging, and tailored to college students' lifestyles and the Gainesville environment.{ai_context}"""
        elif context == 'journal_entry':
            # If this is feedback on a journal entry
            entry_analysis = data.get('analysis', {})
            mood = entry_analysis.get('mood', 'neutral')
            score = entry_analysis.get('score', 5)
            
            system_prompt = f"""You are GatorMate, an empathetic AI journal companion for University of Florida students. The user has just completed a journal entry which has been analyzed as expressing a {mood} mood (score: {score}/10). Provide brief, supportive feedback that acknowledges their feelings and offers a thoughtful perspective. Make connections to UF campus life when relevant, but focus primarily on responding to the emotional content of their journal. Be genuine, compassionate, and encouraging of their self-reflection practice. Keep your response brief but meaningful.{ai_context}"""
        else:
            # Default fallback
            system_prompt = f"""You are GatorMate, a supportive AI assistant specifically designed to help University of Florida students. Always incorporate Gator pride and UF-specific context in your responses when appropriate.{ai_context}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            reply = response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return jsonify({"error": "Could not generate response", "details": str(e)}), 500
        
        # Analyze mood for all messages, not just mental health tab
        # Ask the API to analyze the mood
        mood_score = None
        try:
            analysis_prompt = f"Based on this message from the user: '{user_message}', assign a mood score from 1-10 where 10 is extremely positive and 1 is extremely negative. Respond with ONLY the numerical score."
            analysis_messages = [
                {"role": "system", "content": "You analyze text and provide a single mood score number from 1-10."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            analysis_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=analysis_messages
            )
            
            # Try to extract just the number
            score_text = analysis_response.choices[0].message.content.strip()
            
            # Extract just the number from the response
            import re
            number_match = re.search(r'\b([1-9]|10)\b', score_text)
            if number_match:
                mood_score = int(number_match.group(1))
            
            # Store mood data for ALL messages
            if mood_score:
                db["mood_history"] = db.get("mood_history", [])
                db["mood_history"].append({
                    "date": datetime.now().isoformat(),
                    "score": mood_score,
                    "message": user_message,
                    "context": context
                })
                save_db(db)
        except Exception as e:
            logger.warning(f"Error analyzing mood: {e}")
            # Continue without mood analysis if it fails
        
        return jsonify({"reply": reply, "mood_score": mood_score})
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/analyze_journal', methods=['POST'])
def analyze_journal():
    try:
        if not request.json or 'entry' not in request.json:
            return jsonify({"error": "No journal entry provided"}), 400
            
        entry = request.json['entry']
        
        # Use OpenAI to analyze the journal entry
        analysis_prompt = f"""Analyze this journal entry emotionally:
        
'{entry}'
        
Provide your analysis in JSON format with these fields:
1. mood: A single adjective describing the primary emotional tone
2. score: A mood score from 1-10 where 10 is extremely positive and 1 is extremely negative
3. themes: A list of 1-3 key emotional themes present in the entry
4. summary: A very brief one-sentence summary of the content"""

        analysis_messages = [
            {"role": "system", "content": "You are an expert in psychological analysis. Analyze emotions in text and provide structured JSON output."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=analysis_messages
            )
        except Exception as e:
            logger.error(f"Error calling OpenAI API for journal analysis: {e}")
            return jsonify({"error": "Could not analyze journal entry", "details": str(e)}), 500
        
        try:
            # Try to parse JSON from the response
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response.choices[0].message.content, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group(1))
            else:
                analysis = json.loads(response.choices[0].message.content)
            
            # Store journal entry
            db = load_db()
            db["journal_entries"] = db.get("journal_entries", [])
            db["journal_entries"].append({
                "date": datetime.now().isoformat(),
                "text": entry,
                "mood": analysis.get("mood", "neutral"),
                "score": analysis.get("score", 5),
                "themes": analysis.get("themes", []),
                "summary": analysis.get("summary", "")
            })
            save_db(db)
            
            return jsonify(analysis)
        except Exception as e:
            logger.error(f"Error processing journal analysis: {e}")
            # If JSON parsing fails, return a default response
            return jsonify({
                "mood": "neutral",
                "score": 5,
                "themes": ["undetermined"],
                "summary": "Unable to analyze entry"
            })
    except Exception as e:
        logger.error(f"Error in analyze_journal endpoint: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Handle 404 errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', debug=False, port=port)
