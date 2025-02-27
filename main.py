from flask import Flask, render_template, jsonify, request
import random
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["Dyslexia"]  # Database name
questions_collection = db["Assessment"]
patterns_collection = db["Pattern"]
users_collection = db["User"]

# AI SUGGESTIONS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_suggestions(score):
    prompt = f"""
    A user has taken a dyslexia assessment and scored {score}. 
    Based on their score, provide three personalized suggestions to help them improve learning and reading.
    Example:
    - If the score is low, suggest simple reading exercises.
    - If the score is high, suggest professional intervention.
    Return the response in three lines without bullet points, using \n as a separator.
    """
    model = genai.GenerativeModel()
    response = model.generate_content(prompt)
    suggestions = response.text.strip().split("\n")[:3] 
    return suggestions

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/pattern')
def pattern():
    return render_template("pattern.html")

@app.route('/reading')
def reading():
    return render_template('reading.html')

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get_questions')
def get_questions():
    questions = list(questions_collection.find({}, {"_id": 0}))  
    return jsonify(questions)

@app.route('/get_patterns')
def get_patterns():
    all_patterns = list(patterns_collection.find({}, {"_id": 0}))
    shuffled_patterns = random.sample(all_patterns, min(5, len(all_patterns)))  
    return jsonify(shuffled_patterns)

@app.route('/get_suggestions', methods=['GET'])
def fetch_suggestions():
    score = int(request.args.get('score', 0))  
    suggestions = get_suggestions(score)
    return jsonify({"suggestions": suggestions})

@app.route("/registerapi", methods=["POST"])
def registerapi():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    placeofbirth = data.get("placeofbirth")

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered"}), 400

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "name": name,
        "age": age,
        "gender": gender,
        "placeofbirth": placeofbirth
    }
    
    users_collection.insert_one(user_data)
    return jsonify({"message": "Registration successful"}), 201

@app.route("/loginapi", methods=["POST"])
def loginapi():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user or user["password"] != password:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "username": user["username"]}), 200

if __name__ == '__main__':
    app.run(debug=True)
