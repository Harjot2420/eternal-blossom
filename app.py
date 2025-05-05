from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
import random
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['2420'] = 'your_very_secret_key_here'
app.config['SECRET_MESSAGE_PASSWORD'] = generate_password_hash('forever')  # Change password

# Special dates database
special_dates = {
    "anniversary": "05-11-2023",
    "birthday": "20-04-2005",
    "first_kiss": "22-08-2024",
}

# Love messages database
love_messages = [
    {"title": "Our First Meeting", "content": "The moment our stars aligned..."},
    {"title": "Your Smile", "content": "It brightens my darkest days..."},
    {"title": "Your Touch", "content": "Electricity courses through me..."},
    {"title": "Our Future", "content": "I see endless possibilities with you..."}
]

# Secret messages database
secret_messages = [
    {"date": "2025-02-14", "content": "My dearest, this is our first Valentine's together..."},
    {"date": "2024-08-22", "content": "Our first kisssss..."}
]

# Love letters database
love_letters = [
    {"title": "My Promise", "date": "2023-01-01", "content": "I promise to love you..."},
    {"title": "When We're Apart", "date": "2023-03-15", "content": "The days without you..."}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_message')
def get_message():
    today = datetime.now().strftime("%Y-%m-%d")
    special_message = None
    
    for event, date_str in special_dates.items():
        if today == date_str:
            special_message = {
                'type': 'special',
                'title': f"Happy {event.replace('_', ' ').title()}!",
                'content': f"On this day {event.replace('_', ' ')}..."
            }
            break
    
    if not special_message:
        message = random.choice(love_messages)
        message['type'] = 'regular'
        special_message = message
    
    return jsonify(special_message)

@app.route('/check_secret_message', methods=['POST'])
def check_secret_message():
    data = request.json
    if check_password_hash(app.config['SECRET_MESSAGE_PASSWORD'], data.get('password', '')):
        session['authenticated'] = True
        return jsonify({
            "status": "success", 
            "messages": secret_messages,
            "letters": love_letters
        })
    return jsonify({"status": "error", "message": "Incorrect password"}), 401

@app.route('/add_secret_message', methods=['POST'])
def add_secret_message():
    if not session.get('authenticated'):
        return jsonify({"status": "error", "message": "Not authenticated"}), 403
    
    new_message = request.json
    secret_messages.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": new_message.get('content')
    })
    return jsonify({"status": "success", "message": "Secret message added!"})

@app.route('/add_love_letter', methods=['POST'])
def add_love_letter():
    if not session.get('authenticated'):
        return jsonify({"status": "error", "message": "Not authenticated"}), 403
    
    new_letter = request.json
    love_letters.append({
        "title": new_letter.get('title'),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": new_letter.get('content')
    })
    return jsonify({"status": "success", "message": "Love letter added!"})

@app.route('/get_weather')
def get_weather():
    # This would ideally connect to a weather API
    # For demo purposes, we'll return romantic weather
    weather_types = [
        {"type": "sunny", "message": "The sun shines as brightly as my love for you"},
        {"type": "rainy", "message": "Even the raindrops whisper your name"},
        {"type": "cloudy", "message": "The clouds part when you smile"},
        {"type": "starry", "message": "The stars dance for you tonight"}
    ]
    return jsonify(random.choice(weather_types))

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/audio', exist_ok=True)
    app.run(debug=True, port=5000)