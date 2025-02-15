from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# JSON data for assessment questions
questions = [
    {"question": "What is 2 + 2?", "choice1": "3", "choice2": "4", "choice3": "5", "choice4": "6", "answer": "4"},
    {"question": "Which is a fruit?", "choice1": "Carrot", "choice2": "Apple", "choice3": "Cabbage", "choice4": "Potato", "answer": "Apple"},
    {"question": "What color is the sky?", "choice1": "Red", "choice2": "Blue", "choice3": "Green", "choice4": "Yellow", "answer": "Blue"},
    {"question": "How many legs does a dog have?", "choice1": "2", "choice2": "4", "choice3": "6", "choice4": "8", "answer": "4"},
    {"question": "What is the capital of France?", "choice1": "Berlin", "choice2": "Madrid", "choice3": "Paris", "choice4": "Rome", "answer": "Paris"},
    {"question": "Which is a primary color?", "choice1": "Purple", "choice2": "Red", "choice3": "Brown", "choice4": "Pink", "answer": "Red"},
    {"question": "What animal says 'Meow'?", "choice1": "Dog", "choice2": "Cat", "choice3": "Bird", "choice4": "Cow", "answer": "Cat"},
    {"question": "How many days are in a week?", "choice1": "5", "choice2": "6", "choice3": "7", "choice4": "8", "answer": "7"},
    {"question": "What is 10 - 3?", "choice1": "5", "choice2": "7", "choice3": "8", "choice4": "6", "answer": "7"},
    {"question": "What do bees make?", "choice1": "Milk", "choice2": "Honey", "choice3": "Jam", "choice4": "Cheese", "answer": "Honey"},
    {"question": "How many sides does a triangle have?", "choice1": "2", "choice2": "3", "choice3": "4", "choice4": "5", "answer": "3"},
    {"question": "Which is a domestic animal?", "choice1": "Tiger", "choice2": "Lion", "choice3": "Dog", "choice4": "Elephant", "answer": "Dog"},
    {"question": "How many fingers are on one hand?", "choice1": "3", "choice2": "4", "choice3": "5", "choice4": "6", "answer": "5"},
    {"question": "Which shape has four equal sides?", "choice1": "Rectangle", "choice2": "Square", "choice3": "Triangle", "choice4": "Circle", "answer": "Square"},
    {"question": "What is the opposite of 'Hot'?", "choice1": "Cold", "choice2": "Warm", "choice3": "Soft", "choice4": "Hard", "answer": "Cold"},
    {"question": "How many wheels does a bicycle have?", "choice1": "1", "choice2": "2", "choice3": "3", "choice4": "4", "answer": "2"},
    {"question": "Which is a mode of transport?", "choice1": "Apple", "choice2": "Car", "choice3": "Chair", "choice4": "Spoon", "answer": "Car"},
    {"question": "Which month has 28 or 29 days?", "choice1": "January", "choice2": "February", "choice3": "March", "choice4": "April", "answer": "February"},
    {"question": "Which is a farm animal?", "choice1": "Shark", "choice2": "Cow", "choice3": "Whale", "choice4": "Snake", "answer": "Cow"},
    {"question": "What is 5 + 3?", "choice1": "6", "choice2": "7", "choice3": "8", "choice4": "9", "answer": "8"}
]


# JSON data for pattern recognition
patterns = [
    {"sequence": ["square", "circle", "square", "dash"], "answer": "square"},
    {"sequence": ["circle", "square", "circle", "square"], "answer": "circle"},
    {"sequence": ["triangle", "square", "triangle", "circle"], "answer": "triangle"},
    {"sequence": ["dash", "dash", "circle", "dash"], "answer": "circle"},
    {"sequence": ["square", "square", "circle", "square"], "answer": "circle"}
]

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json  # Get answers from frontend
    user_answers = data.get("answers", [])

    score = 0
    for i, user_answer in enumerate(user_answers):
        if user_answer == questions[i]["answer"]:  # Ensure exact match
            score += 1

    # Determine dyslexia level
    if score <= 4:
        result = "High Dyslexia - Treatment Required"
    elif score <= 7:
        result = "Low Dyslexia (Early Stage)"
    else:
        result = "No Dyslexia"

    return jsonify({"score": score, "result": result})


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/pattern_recognition')
def pattern_recognition():
    return render_template('pattern.html')

@app.route('/get_questions')
def get_questions():
    shuffled_questions = random.sample(questions, 10)
    return jsonify(shuffled_questions)

@app.route('/get_patterns')
def get_patterns():
    selected_pattern = random.choice(patterns)
    return jsonify(selected_pattern)

if __name__ == '__main__':
    app.run(debug=True)
