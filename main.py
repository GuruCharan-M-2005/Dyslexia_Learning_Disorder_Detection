from flask import Flask, render_template, jsonify, request
import random
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)


# AI BASED SUGGESTION FOR ASSESSMENT RESULT PAGE
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


questions = [
    {"image":"https://tse1.mm.bing.net/th?id=OIP.iKEdZsVGxxPHhKA9pJ1gHgHaHZ&pid=Api&P=0&h=180","question": "What color is the sun?", "choice1": "Yellow", "choice2": "Blue", "choice3": "Green", "choice4": "Red", "answer": "Yellow"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.TzP2op3lkhlTh6oOHamacAHaHa&pid=Api&P=0&h=180","question": "What sound does a cat make?", "choice1": "Woof", "choice2": "Meow", "choice3": "Moo", "choice4": "Quack", "answer": "Meow"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.gJq0aSbv2Gxu7mtckG3PfgHaFX&pid=Api&P=0&h=180","question": "Which is a fruit?", "choice1": "Apple", "choice2": "Carrot", "choice3": "Broccoli", "choice4": "Potato", "answer": "Apple"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.jln6a9t6OfNrNJWVlQiS9gHaHa&pid=Api&P=0&h=180","question": "What number comes after 2?", "choice1": "1", "choice2": "3", "choice3": "5", "choice4": "0", "answer": "3"},
    {"image":"https://tse1.mm.bing.net/th?id=OIP.ESnKED-YaJF652_mDB7pgwHaIC&pid=Api&P=0&h=180","question": "How many eyes do you have?", "choice1": "1", "choice2": "2", "choice3": "3", "choice4": "4", "answer": "2"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.suufGLOuyD8Ge6iYG_2xHwHaEe&pid=Api&P=0&h=180","question": "Which animal barks?", "choice1": "Cat", "choice2": "Dog", "choice3": "Cow", "choice4": "Duck", "answer": "Dog"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.yldbxZVxOCK5KIDbQhmIGgHaJR&pid=Api&P=0&h=180","question": "What color are bananas?", "choice1": "Red", "choice2": "Blue", "choice3": "Yellow", "choice4": "Green", "answer": "Yellow"},
    {"image":"https://easydrawingart.com/wp-content/uploads/2019/08/How-to-draw-a-human-2.jpg","question": "How many hands do you have?", "choice1": "2", "choice2": "4", "choice3": "6", "choice4": "1", "answer": "2"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.8-k5MhblTFcab2B44CrL6gHaEK&pid=Api&P=0&h=180","question": "Which is bigger, an elephant or a mouse?", "choice1": "Elephant", "choice2": "Mouse", "choice3": "Same size", "choice4": "Fish", "answer": "Elephant"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.yfeFjc5iO5yC6A_sQ2Xm7AAAAA&pid=Api&P=0&h=180","question": "Where do fish live?", "choice1": "Sky", "choice2": "Water", "choice3": "Land", "choice4": "Tree", "answer": "Water"},
    {"image":"https://tse1.mm.bing.net/th?id=OIP.zN_vo1rdpxYUM1MrvfEeuAHaHa&pid=Api&P=0&h=180","question": "What sound does a cow make?", "choice1": "Moo", "choice2": "Meow", "choice3": "Woof", "choice4": "Quack", "answer": "Moo"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.pFKRhQ-BV60LU6FUBu6_AQHaHa&pid=Api&P=0&h=180","question": "What color is grass?", "choice1": "Green", "choice2": "Blue", "choice3": "Purple", "choice4": "Red", "answer": "Green"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.6iV7cFgtEGCDYJ50I5n61wHaF9&pid=Api&P=0&h=180","question": "Which is a vegetable?", "choice1": "Apple", "choice2": "Carrot", "choice3": "Banana", "choice4": "Orange", "answer": "Carrot"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.YBPQgHYo0blhl-Y_cs37qQHaE7&pid=Api&P=0&h=180","question": "What do you use to eat soup?", "choice1": "Fork", "choice2": "Spoon", "choice3": "Knife", "choice4": "Plate", "answer": "Spoon"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.oX4TFbay100bTuNNjhdQ6gHaHa&pid=Api&P=0&h=180","question": "What shape is a ball?", "choice1": "Square", "choice2": "Triangle", "choice3": "Circle", "choice4": "Rectangle", "answer": "Circle"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.T544Qdf-lY8u-zm_69RyDwAAAA&pid=Api&P=0&h=180","question": "What do you wear on your feet?", "choice1": "Hat", "choice2": "Shoes", "choice3": "Gloves", "choice4": "Socks", "answer": "Shoes"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.UgsQBApUUtGAhdgt-WIfQgHaHa&pid=Api&P=0&h=180","question": "Which is a color?", "choice1": "Table", "choice2": "Red", "choice3": "House", "choice4": "Toy", "answer": "Red"},
    {"image":"https://tse1.mm.bing.net/th?id=OIP.Ib6DOQ3PoqdYhFw85J_TrgHaEW&pid=Api&P=0&h=180","question": "What animal says 'Moo'?", "choice1": "Sheep", "choice2": "Cat", "choice3": "Cow", "choice4": "Dog", "answer": "Cow"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.SGCPAwcc6yudCZC2-SB_ywHaHw&pid=Api&P=0&h=180","question": "What do you use to brush your teeth?", "choice1": "Comb", "choice2": "Toothbrush", "choice3": "Spoon", "choice4": "Shampoo", "answer": "Toothbrush"},
    {"image":"https://tse4.mm.bing.net/th?id=OIP.CIac5BAbYhrvBddLTcoNxAHaEW&pid=Api&P=0&h=180","question": "How many wheels does a car have?", "choice1": "2", "choice2": "3", "choice3": "4", "choice4": "5", "answer": "4"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.Or3DuhEPAGJVUH5jPbnsgQHaFV&pid=Api&P=0&h=180","question": "What is the opposite of 'Up'?", "choice1": "Down", "choice2": "Left", "choice3": "Right", "choice4": "Straight", "answer": "Down"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.7kUDPX3-LPUlLWdHElG1GAHaF7&pid=Api&P=0&h=180","question": "What is 1 + 1?", "choice1": "1", "choice2": "2", "choice3": "3", "choice4": "4", "answer": "2"},
    {"image":"https://helpingwithmath.com/wp-content/uploads/2022/03/image-109.png","question": "Which shape has four equal sides?", "choice1": "Triangle", "choice2": "Rectangle", "choice3": "Circle", "choice4": "Square", "answer": "Square"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.ZfuC4RnPRyyKHJ9co6w-PQHaFS&pid=Api&P=0&h=180","question": "How many legs does a dog have?", "choice1": "2", "choice2": "4", "choice3": "6", "choice4": "8", "answer": "4"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.7kUDPX3-LPUlLWdHElG1GAHaF7&pid=Api&P=0&h=180","question": "What number comes after 5?", "choice1": "3", "choice2": "6", "choice3": "7", "choice4": "8", "answer": "6"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.2_9yJhkcUr2y9KkFhlHJ-wHaEx&pid=Api&P=0&h=180","question": "What is the opposite of 'Hot'?", "choice1": "Cold", "choice2": "Warm", "choice3": "Soft", "choice4": "Hard", "answer": "Cold"},
    {"image":"https://tse3.mm.bing.net/th?id=OIP.7kUDPX3-LPUlLWdHElG1GAHaF7&pid=Api&P=0&h=180","question": "What is 10 - 3?", "choice1": "5", "choice2": "7", "choice3": "8", "choice4": "6", "answer": "7"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.OPmWmIwjFejQUyTwfiMkyAHaD4&pid=Api&P=0&h=180","question": "Which is a primary color?", "choice1": "Purple", "choice2": "Red", "choice3": "Brown", "choice4": "Pink", "answer": "Red"},
    {"image":"https://tse2.mm.bing.net/th?id=OIP.wOTei2g-Ch2wuzPScyyu5wHaLH&pid=Api&P=0&h=180","question": "What is the capital of France?", "choice1": "Berlin", "choice2": "Madrid", "choice3": "Paris", "choice4": "Rome", "answer": "Paris"},
    {"image":"https://tse1.mm.bing.net/th?id=OIP.CvEbtxW39FjKR7jdNICIUwAAAA&pid=Api&P=0&h=180","question": "Which month has 28 or 29 days?", "choice1": "January", "choice2": "February", "choice3": "March", "choice4": "April", "answer": "February"}
]



patterns = [
   {"question": "Select the next pattern in the sequence:", "sequence": ["⬛", "⚫", "⬛", "?"], "options": {"square": "⬛ Square", "circle": "⚫ Circle"}, "answer": "circle"},
    {"question": "Which shape comes next?", "sequence": ["🔺", "🔵", "🔺", "?"], "options": {"triangle": "🔺 Triangle", "circle": "🔵 Circle"}, "answer": "circle"},
    {"question": "Pick the correct pattern:", "sequence": ["🟢", "🟡", "🟢", "?"], "options": {"green": "🟢 Green", "yellow": "🟡 Yellow"}, "answer": "yellow"},
    {"question": "What comes next?", "sequence": ["🟥", "🟨", "🟥", "?"], "options": {"red": "🟥 Red", "yellow": "🟨 Yellow"}, "answer": "yellow"},
    {"question": "Identify the pattern:", "sequence": ["🔶", "🔷", "🔶", "?"], "options": {"diamond": "🔷 Diamond", "hexagon": "🔶 Hexagon"}, "answer": "diamond"},
    {"question": "Next shape?", "sequence": ["🔵", "🔴", "🔵", "?"], "options": {"blue": "🔵 Blue", "red": "🔴 Red"}, "answer": "red"},
    {"question": "Complete the sequence:", "sequence": ["⬜", "⬛", "⬜", "?"], "options": {"white": "⬜ White", "black": "⬛ Black"}, "answer": "black"},
    {"question": "What follows?", "sequence": ["🟧", "🟦", "🟧", "?"], "options": {"orange": "🟧 Orange", "blue": "🟦 Blue"}, "answer": "blue"},
    {"question": "Guess the missing shape:", "sequence": ["🟠", "🟣", "🟠", "?"], "options": {"purple": "🟣 Purple", "orange": "🟠 Orange"}, "answer": "purple"},
    {"question": "Find the next pattern:", "sequence": ["⬜", "⬛", "⬛", "⬜", "⬜", "?"], "options": {"black": "⬛ Black", "white": "⬜ White"}, "answer": "black"},
    {"question": "What is the missing shape?", "sequence": ["🔺", "🔻", "🔺", "?"], "options": {"up": "🔺 Up Triangle", "down": "🔻 Down Triangle"}, "answer": "down"},
    {"question": "Choose the correct pattern:", "sequence": ["🟥", "🟩", "🟦", "?"], "options": {"blue": "🟦 Blue", "green": "🟩 Green"}, "answer": "green"},
    {"question": "Complete the set:", "sequence": ["🟤", "⚪", "🟤", "?"], "options": {"white": "⚪ White", "brown": "🟤 Brown"}, "answer": "white"},
    {"question": "Identify the missing pattern:", "sequence": ["🟪", "🟨", "🟪", "?"], "options": {"yellow": "🟨 Yellow", "purple": "🟪 Purple"}, "answer": "yellow"},
    {"question": "Which shape continues the pattern?", "sequence": ["🟢", "🟠", "🟢", "?"], "options": {"green": "🟢 Green", "orange": "🟠 Orange"}, "answer": "orange"}
]


users = [
    {
        "username": "spacece",
        "email": "spacece@gmail.com",
        "password": "spacece"
    },
]

def get_suggestions(score):
    print("RUNNING API GEMINI------------------------------------------------------------------------------")
    prompt = f"""
    A user has taken a dyslexia assessment and scored {score}. 
    Based on their score, provide three personalized suggestions to help them improve learning and reading.
    Example:
    - If the score is low, suggest simple reading exercises.
    - If the score is high, suggest professional intervention.
    Return the response in three lines without bulletin and just add \n in each line.
    """
    model = genai.GenerativeModel()
    response = model.generate_content(prompt)
    suggestions = response.text.strip().split("\n")[:3] 
    print(suggestions)
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
    return jsonify(questions)

@app.route('/get_patterns')
def get_paterns():
    shuffled_questions = random.sample(patterns, 5)
    return jsonify(shuffled_questions)

@app.route('/get_suggestions', methods=['GET'])
def fetch_suggestions():
    score = int(request.args.get('score', 0))  
    suggestions = get_suggestions(score)
    return jsonify({"suggestions": suggestions})



@app.route("/registerapi", methods=["POST"])
def registerapi():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    if email in users:
        return jsonify({"message": "Email already registered"}), 400
    # users[email] = {"username": username, "password": password}  # to save data when connected with DB for future purpose
    return jsonify({"message": "Registration successful"}), 201

@app.route("/loginapi", methods=["POST"])
def loginapi():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email not in users or users[email]["password"] != password:
        return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"message": "Login successful", "username": users[email]["username"]}), 200



if __name__ == '__main__':
    app.run(debug=True)

