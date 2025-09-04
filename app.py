from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session security

# ---- In-memory user storage (later replace with DB) ----
users = {"admin": "password123"}   # default admin user
user_workouts = {"admin": []}      # workouts per user

@app.route("/")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("home.html", username=username)
    else:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            user_workouts.setdefault(username, [])
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            flash("Username already exists!", "danger")
        elif not username or not password:
            flash("Please fill in all fields", "warning")
        else:
            # add new user
            users[username] = password
            user_workouts[username] = []  # each user has own workout list
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/add_workout", methods=["POST"])
@app.route("/add_workout", methods=["POST"])
def add_workout():
    if "username" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    workout = request.form.get("workout")
    duration = request.form.get("duration")
    username = session["username"]

    if not workout or not duration:
        flash("Please enter both workout and duration.", "danger")
    else:
        try:
            duration = int(duration)

            # check for duplicate workout name (case-insensitive)
            existing = [w["workout"].lower() for w in user_workouts.get(username, [])]
            if workout.lower() in existing:
                flash(f"Workout '{workout}' already exists!", "danger")
            else:
                user_workouts.setdefault(username, []).append(
                    {"workout": workout, "duration": duration}
                )
                flash(f"Workout '{workout}' added successfully!", "success")

        except ValueError:
            flash("Duration must be a number.", "danger")

    return redirect(url_for("home"))


@app.route("/workouts")
def view_workouts():
    if "username" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    username = session["username"]
    workouts = user_workouts.get(username, [])
    return render_template("workouts.html", username=username, workouts=workouts)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
