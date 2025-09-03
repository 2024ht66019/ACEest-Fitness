# tests/test_app.py
import pytest
from app import app, users, user_workouts

@pytest.fixture
def client():
    app.config.update(TESTING=True, SECRET_KEY="test")
    with app.test_client() as c:
        yield c

def login(client, username="admin", password="password123"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_redirect_home_when_not_logged_in(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (301, 302)
    assert "/login" in r.headers["Location"]

def test_register_new_user_and_login(client):
    # register
    r = client.post("/register",
                    data={"username": "alice", "password": "secret"},
                    follow_redirects=True)
    assert b"Registration successful" in r.data
    assert "alice" in users
    assert "alice" in user_workouts

    # login
    r = login(client, "alice", "secret")
    assert b"Welcome back, alice!" in r.data

def test_login_success_and_fail(client):
    assert b"Welcome back, admin!" in login(client).data  # success
    r = client.post("/login", data={"username": "admin", "password": "wrong"}, follow_redirects=True)
    assert b"Invalid username or password" in r.data

def test_add_workout_success(client):
    login(client)
    r = client.post("/add_workout",
                    data={"workout": "Pushups", "duration": "15"},
                    follow_redirects=True)
    assert b"added successfully" in r.data

def test_add_workout_duplicate_rejected(client):
    # relies on duplicate check you added earlier (case-insensitive)
    login(client)
    client.post("/add_workout", data={"workout": "Plank", "duration": "5"}, follow_redirects=True)
    r = client.post("/add_workout", data={"workout": "plank", "duration": "10"}, follow_redirects=True)
    assert b"already exists" in r.data

def test_add_workout_requires_number_for_duration(client):
    login(client)
    r = client.post("/add_workout", data={"workout": "Yoga", "duration": "ten"}, follow_redirects=True)
    assert b"Duration must be a number" in r.data

def test_view_workouts_requires_login(client):
    r = client.get("/workouts", follow_redirects=False)
    assert r.status_code in (301, 302)
    assert "/login" in r.headers["Location"]

def test_view_workouts_shows_list(client):
    login(client, "admin", "password123")
    client.post("/add_workout", data={"workout": "Run", "duration": "20"}, follow_redirects=True)
    r = client.get("/workouts")
    assert r.status_code == 200
    assert b"Run" in r.data
    assert b"20 minutes" in r.data

