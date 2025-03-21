# 🧠 Child Learning Disorder & Dyslexia Assessment  

This project is a **Flask-based web application** designed to determine whether a child has **learning disorders** such as **dyslexia**. It includes **four assessments** to analyze different cognitive abilities:  

1️⃣ **General Assessment** – Basic cognitive and learning capability test.  
2️⃣ **Pattern Recognition** – Evaluates a child's ability to recognize patterns.  
3️⃣ **Reading Ability** – Assesses reading fluency and comprehension.  
4️⃣ **Eye Tracking** – Uses AI-powered analysis to track reading difficulties.  

The app integrates **Google Gemini AI** to generate questions and provide insights based on assessment results.  

---

## 🚀 Getting Started  

### 1️⃣ Clone the Repository  
To get started, clone the repository:  
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2️⃣ Install Dependencies  
Ensure Python is installed, then run:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Database

#### Install MongoDB
Download and install MongoDB from [MongoDB Official Website](https://www.mongodb.com/try/download/community).

#### Create Database and Collections
*Open the **MongoDB Compass** and Create the **`Dyslexia` database**.*

#### Collections Overview
- **Assessment**: Stores assessment-related data.
- **Pattern**: Contains patterns for analysis.

``` 
 Download json files from github repo and add them in MongoDB database.
```


### 4️⃣  Set Up API Key  
Create a `.env` file in the project directory and add your Google Gemini API key:  
```env
GEMINI_API_KEY=your-api-key-here
```


### 5️⃣ Download Face Detection Landmark for Eye Tracking
Run this command in terminal of your current project folder.
```bash
python -c "import urllib.request; urllib.request.urlretrieve('http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2', 'shape_predictor_68_face_landmarks.dat.bz2')"
python -c "import bz2, shutil; with bz2.BZ2File('shape_predictor_68_face_landmarks.dat.bz2') as fr, open('shape_predictor_68_face_landmarks.dat', 'wb') as fw: shutil.copyfileobj(fr, fw)"
```


### 6️⃣ Run the Flask App  
Start the application by running:  
```bash
python main.py
```
The app will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## 📂 Project Structure  
```bash
/your-repo-name
│── /static                # Static assets (CSS, images, JS)
│── /templates             # HTML templates
│── main.py                # Flask backend
│── requirements.txt       # Dependencies
│── .env                   # API key (not committed)
│── README.md              # Project documentation
```

---

## ✅ Features  
✔ **AI-Powered Assessments** – Uses Gemini AI for intelligent question generation.  
✔ **User-Friendly UI** – Simple and interactive assessment process.  
✔ **Dynamic Evaluations** – Different tests for various cognitive skills.  
✔ **Insights & Recommendations** – AI-based suggestions for improvement.  

---

## 📌 Notes  
🔹 Ensure you add `.env` to `.gitignore` to keep API keys safe.  
🔹 If you face module errors, run `pip install -r requirements.txt` again.  
🔹 Extend the project by integrating machine learning for enhanced analysis.  

---

## 💡 Future Improvements  
🔍 **More AI-Powered Analysis** for better diagnosis.  
🎥 **Video-Based Eye Tracking** for more precise results.  
📊 **Dashboard for Progress Tracking** to monitor a child’s learning development.  

💙 Made for early detection & support! 🧑‍🎓🚀

