from flask import Flask, render_template, jsonify
import time
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Path to the JSON file for storing button appearance times
json_file_path = 'button_times.json'

# Function to load data from JSON file
def load_json_data():
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"next_2min_button": 0, "next_date_button": "2024-09-06"}

# Function to save data to JSON file
def save_json_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# Check if the first button should appear (every 2 minutes)
@app.route('/check-2min-button', methods=['GET'])
def check_2min_button():
    data = load_json_data()
    current_time = time.time()

    if current_time >= data['next_2min_button']:
        return jsonify({'show_button': True})
    else:
        return jsonify({'show_button': False})

# Check if the second button should appear (on or after 9/6/2024)
@app.route('/check-date-button', methods=['GET'])
def check_date_button():
    data = load_json_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if today >= data['next_date_button']:
        return jsonify({'show_button': True})
    else:
        return jsonify({'show_button': False})

# Handle the first button click (set next appearance after 2 minutes)
@app.route('/first-button-click', methods=['POST'])
def first_button_click():
    data = load_json_data()
    current_time = time.time()

    # Set the next appearance time to 2 minutes from now
    data['next_2min_button'] = current_time + 120  # 120 seconds = 2 minutes
    save_json_data(data)

    return jsonify({'message': 'Button will appear again in 2 minutes.'})

# Handle the second button click (set next appearance after 3 days)
@app.route('/second-button-click', methods=['POST'])
def second_button_click():
    data = load_json_data()
    current_date = datetime.now()

    # Set the next appearance date to 3 days from now
    next_appearance = current_date + timedelta(days=3)
    data['next_date_button'] = next_appearance.strftime("%Y-%m-%d")
    save_json_data(data)

    return jsonify({'message': 'Button will appear again in 3 days.'})

if __name__ == '__main__':
    app.run(debug=True)
