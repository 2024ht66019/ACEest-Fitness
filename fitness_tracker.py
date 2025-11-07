from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secret-in-prod"

# In-memory storage
workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}
diet_entries = []  # list of dicts: {food, calories, timestamp}

# Helper to compute totals for charts
def workout_totals():
    totals = {k: sum(item["duration"] for item in v) for k, v in workouts.items()}
    return totals

@app.route('/')
def index():
    categories = list(workouts.keys())
    return render_template('index.html', categories=categories, workouts=workouts, diet=diet)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    category = request.form.get('category')
    exercise = request.form.get('exercise', '').strip()
    duration_str = request.form.get('duration', '').strip()

    if not exercise or not duration_str:
        flash("Please enter both exercise and duration.", "error")
        return redirect(url_for('index'))

    try:
        duration = int(duration_str)
        if duration <= 0:
            raise ValueError
    except ValueError:
        flash("Duration must be a positive integer (minutes).", "error")
        return redirect(url_for('index'))

    entry = {
        "exercise": exercise,
        "duration": duration,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    workouts.setdefault(category, []).append(entry)
    flash(f"Added {exercise} ({duration} min) to {category}.", "success")
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    """Tab showing table summary (like your Tkinter summary view)."""
    return render_template('summary.html', workouts=workouts)

@app.route('/charts')
def charts():
    """Page that displays workout and diet charts."""
    return render_template('charts.html')

@app.route('/api/workout_totals')
def api_workout_totals():
    totals = workout_totals()
    return jsonify(totals)

@app.route('/diet')
def diet():
    """Diet page - shows entries and form for diet items."""
    return render_template('diet.html', diet_entries=diet_entries)

@app.route('/add_diet', methods=['POST'])
def add_diet():
    food = request.form.get('food', '').strip()
    calories_str = request.form.get('calories', '').strip()

    if not food or not calories_str:
        flash("Please enter both food and calories.", "error")
        return redirect(url_for('diet'))

    try:
        calories = int(calories_str)
        if calories < 0:
            raise ValueError
    except ValueError:
        flash("Calories must be a non-negative integer.", "error")
        return redirect(url_for('diet'))

    entry = {
        "food": food,
        "calories": calories,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    diet_entries.append(entry)
    flash(f"Added diet item: {food} ({calories} kcal).", "success")
    return redirect(url_for('diet'))

# Simple API to get raw sessions (if needed)
@app.route('/api/sessions')
def api_sessions():
    return jsonify({"workouts": workouts, "diet": diet_entries})

if __name__ == '__main__':
    app.run(debug=True)
