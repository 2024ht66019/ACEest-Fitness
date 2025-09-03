from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # required for session security

# ---- Dummy credentials (later you can connect DB) ----
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route("/")
def home():
    # if logged in, show welcome page
    if "username" in session:
        return render_template("home.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)