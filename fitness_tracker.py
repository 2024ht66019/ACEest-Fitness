from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage (same structure as in Tkinter app)
workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

@app.route('/')
def home():
    """Home page with form to add workouts."""
    return render_template('index.html', categories=list(workouts.keys()))

@app.route('/add', methods=['POST'])
def add_workout():
    """Add a workout entry."""
    category = request.form.get('category')
    workout = request.form.get('exercise', '').strip()
    duration_str = request.form.get('duration', '').strip()

    if not workout or not duration_str:
        return render_template('index.html',
                               categories=list(workouts.keys()),
                               error="Please enter both exercise and duration.")

    try:
        duration = int(duration_str)
    except ValueError:
        return render_template('index.html',
                               categories=list(workouts.keys()),
                               error="Duration must be a number.")

    entry = {
        "exercise": workout,
        "duration": duration,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    workouts[category].append(entry)
    message = f"Added {workout} ({duration} min) to {category}!"

    return render_template('index.html',
                           categories=list(workouts.keys()),
                           message=message)

@app.route('/summary')
def summary():
    """Display a categorized summary of all sessions."""
    return render_template('summary.html', workouts=workouts)

if __name__ == '__main__':
    app.run(debug=True)

