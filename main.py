from flask import Flask, render_template, jsonify, request, send_file
import random
import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["Dyslexia"] 

def get_or_create_collection(db, collection_name):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    return db[collection_name]

questions_collection = get_or_create_collection(db, "Assessment")
patterns_collection = get_or_create_collection(db, "Pattern")
users_collection = get_or_create_collection(db, "User")
scores_collection = get_or_create_collection(db,"Scores")


# AI SUGGESTIONS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def generate_graph(scores):
    plt.figure(figsize=(6, 4))
    numeric_scores = {k: v for k, v in scores.items() if isinstance(v, (int, float))}
    categories = list(numeric_scores.keys())
    values = list(numeric_scores.values())
    plt.bar(categories, values, color=['blue', 'green', 'red'])
    plt.xlabel("Assessment Types")
    plt.ylabel("Scores")
    plt.title("Dyslexia Assessment Scores")
    graph_path = "temp_graph.png" 
    plt.savefig(graph_path, format="png")
    plt.close()  
    return graph_path 

def generate_ai_suggestion(scores):
    prompt = f"""
    Given the following dyslexia assessment scores:
    - Assessment: {scores['assessment']}
    - Pattern: {scores['pattern']}
    - Reading: {scores['reading']}
    Provide a detailed report including analysis and recommendations.
    """
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_pdf(scores, ai_suggestion):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=15)
    pdf.cell(200, 10, "Dyslexia Detection Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Assessment Scores:", ln=True)
    pdf.set_font("Arial", size=10)
    for key, value in scores.items():
        if value!="abc123":
            pdf.cell(0, 10, f"{key}: {str(value)}", ln=True)
    pdf.ln(10)
    markdown_lines = ai_suggestion.split("\n")
    for line in markdown_lines:
        if line.startswith("# "): 
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, line[2:], ln=True)
        elif line.startswith("## "): 
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, line[3:], ln=True)
        else:
            font_style = ""
            if "***" in line: 
                font_style = "BI"
                line = line.replace("***", "")
            elif "**" in line: 
                font_style = "B"
                line = line.replace("**", "")
            elif "*" in line:  
                font_style = "I"
                line = line.replace("*", "")
            
            pdf.set_font("Arial", font_style, 10)
            pdf.multi_cell(0, 10, line)
        pdf.ln(2)
    pdf.ln(10)
    pdf.image(generate_graph(scores), x=10, y=None, w=150)
    pdf_path = "dyslexia_report.pdf"
    pdf.output(pdf_path)
    return pdf_path



@app.route("/generate-report", methods=["GET"])
def generate_report():
    scores_data = scores_collection.find_one({"id": "abc123"}, {"_id": 0})
    if not scores_data:
        return jsonify({"error": "No scores found"}), 404
    ai_suggestion = generate_ai_suggestion(scores_data)
    pdf_path = generate_pdf(scores_data, ai_suggestion)
    return send_file(pdf_path, as_attachment=True)

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
    questions_collection = list(db.Assessment.find({}, {"_id": 0})) 
    shuffled_questions = random.sample(questions_collection, min(2, len(questions_collection)))  
    return jsonify(shuffled_questions)

@app.route('/get_patterns')
def get_patterns():
    patterns_collection = list(db.Pattern.find({}, {"_id": 0})) 
    shuffled_patterns = random.sample(patterns_collection, min(2, len(patterns_collection)))
    return jsonify(shuffled_patterns)

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


@app.route("/submit_scores", methods=["POST"])
def submit_scores():
    data = request.json
    assessment = data.get("assessment", 0)
    pattern = data.get("pattern", 0)
    reading = data.get("reading", 0)
    existing_scores = scores_collection.find_one({"id": "abc123"})

    if existing_scores:
        updated_scores = {
            "assessment": max(existing_scores["assessment"], assessment),
            "pattern": max(existing_scores["pattern"], pattern),
            "reading": max(existing_scores["reading"], reading)
        }
        scores_collection.update_one({"id": "abc123"}, {"$set": updated_scores})
    else:
        scores_collection.insert_one({
            "id": "abc123",
            "assessment": assessment,
            "pattern": pattern,
            "reading": reading
        })

    return jsonify({"message": "Scores updated successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
