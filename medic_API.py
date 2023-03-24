import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

class MySQLHandler:
    def __init__(self, host='localhost', user='root', password='root', database='mysql'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def select(self, table, columns, conditions=None):
        query = f"SELECT {','.join(columns)} FROM {table}"
        if conditions:
            query += f" WHERE {conditions}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, table, data):
        columns = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()

    def update(self, table, data, conditions=None):
        query = f"UPDATE {table} SET "
        query += ','.join([f"{column}=%s" for column in data.keys()])
        if conditions:
            query += f" WHERE {conditions}"
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()

    def delete(self, table, conditions=None):
        query = f"DELETE FROM {table}"
        if conditions:
            query += f" WHERE {conditions}"
        self.cursor.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)
class PromptHistory():
    history = {
        "Brené Brown": "In my experience, vulnerability is the key to growth and connection. What does vulnerability mean to you?",
        "Tony Robbins": "You have the power to change your life. What's one small step you can take today to move closer to your goals?",
        "Nancy Kline": "What assumptions are you making about yourself or the situation? Could they be holding you back?",
        "The Buddha": "The path to enlightenment begins with awareness. What are you becoming more aware of in this moment?",
        "Simon Sinek": "Start with why. What's the underlying motivation or purpose behind your goal?"
    }
# Define function to generate chatgpt4 response
def generate_response(coach, user_input):
    # Select the appropriate API key based on the coach
    if coach == "Brené Brown":
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY_BRENE_BROWN")
    elif coach == "Tony Robbins":
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY_TONY_ROBBINS")
    elif coach == "Nancy Kline":
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY_NANCY_KLINE")
    elif coach == "The Buddha":
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY_THE_BUDDHA")
    elif coach == "Simon Sinek":
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY_SIMON_SINEK")
    else:
        return "Invalid coach selected."
    # Define prompt based on the coach
    prompt = PromptHistory.history[coach] + "\nUser: " + user_input
    # Generate response using XLNet or GPT-3
    print(prompt)
    if coach in ["The Buddha", "Nancy Kline"]:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    else:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5
        )
    # Extract text from response
    text = response.choices[0].text.strip()
    PromptHistory.history[coach] = prompt + f"\n AI: " + response.choices[0].text.strip()
    return text

# Create an instance of the Flask class
app = Flask(__name__)

# Define the route for the chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    # Get user input and coach selection from the request
    data = request.json
    user_input = data["user_input"]
    coach = data["coach"]
    
    # Generate a response using XLNet or GPT-3 and the selected coach
    response = generate_response(coach, user_input)
    
    # Return the response as JSON
    return jsonify({"response": response})


# Define the route for the email transcript API
@app.route("/email", methods=["POST"])
def email():
    # Get user input, coach selection, and transcript from the request
    data = request.json
    user_input = data["user_input"]
    coach = data["coach"]
    transcript = data["transcript"]
    
    # Send an email with the transcript
    # ...
    
    # Return a success message as JSON
    return jsonify({"message": "Transcript sent successfully."})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            password = request.form.get('password')
            newsletter = request.form.get('newsletter')
            print(fname, lname, email, password, newsletter)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route("/register/add/", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        newsletter = request.form.get('newsletter')
        print(fname, lname, email, password, newsletter)
    return redirect(url_for('index'))
@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')

# Start the Flask application only if this file is being run directly
if __name__ == "__main__":
    app.run(debug=True, port=5000)

