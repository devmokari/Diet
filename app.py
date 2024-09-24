from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

SAVE_DIR = 'daily_files'

# Ensure the save directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Load meals from the JSON file
def load_meals():
    try:
        with open('meals.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if meals.json does not exist

# Load types from the JSON file
def load_types():
    try:
        with open('types.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if types.json does not exist

# Save meals for a specific date
def save_meals_for_date(date_str, meals):
    file_path = os.path.join(SAVE_DIR, f'{date_str}.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(meals, file, ensure_ascii=False, indent=4)

# Load meals for a specific date
def load_meals_for_date(date_str):
    file_path = os.path.join(SAVE_DIR, f'{date_str}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}  # Return an empty dict if the file does not exist

# Index route to display the meals page
@app.route('/')
def index():
    meals = load_meals()
    types = load_types()
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date
    return render_template('index.html', meals=meals, types=types, current_date=current_date)

# Route to save selections for a specific date
@app.route('/save-selections/<date>', methods=['POST'])
def save_selections(date):
    selections = request.get_json()  # Get the JSON data from the request
    save_meals_for_date(date, selections)  # Save meals for the selected date
    return jsonify({'status': 'success'})

# Route to load selections for a specific date
@app.route('/load-selections/<date>', methods=['GET'])
def load_selections(date):
    meals = load_meals_for_date(date)  # Load meals for the selected date
    if meals:
        return jsonify(meals)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
