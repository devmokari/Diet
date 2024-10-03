from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from meals import *

app = Flask(__name__)

# Index route to display the meals page
@app.route('/')
def index():
    meals = load("meals")
    types = load("types")
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date
    return render_template('index.html', meals=meals, types=types, current_date=current_date)

@app.route('/edit')
def edit():
    meals = load("meals")
    return render_template('edit.html', meals=meals)

# Route to save selections for a specific date
@app.route('/save-selections/<date>', methods=['POST'])
def save_selections(date):
    selections = request.get_json()  # Get the JSON data from the request
    update_or_insert_report('Sam',date, selections)  # Save meals for the selected date
    return jsonify({'status': 'success'})

# Route to load selections for a specific date
@app.route('/load-selections/<date>', methods=['GET'])
def load_selections(date):
    data = get_user_date('Sam')
    reports = data.get('report', {})
    report=  reports.get(date,"{}")
    meals = json.loads(report)
    return jsonify(meals)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
