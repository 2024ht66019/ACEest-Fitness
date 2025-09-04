ACEest Fitness & Gym

A simple Flask-based web application for tracking user workouts, with support for user registration, login, workout addition, and viewing workout history.
The project is containerized using Docker and includes a CI/CD pipeline with automated testing.

Table of Contents
	[Features](#features)  
	[Prerequisites](#prerequisites)  
	[Setup and Run (Local)](#setup-and-run-local)  
	[Running Tests](#running-tests)  
	[Docker](#docker)  
	[CI/CD Pipeline](#cicd-pipeline)  
	[Future Enhancements](#future-enhancements)  
	[License](#license)

Features
	Multi-user registration and login  
	Session-based authentication  
	Add new workouts (with duplicate name validation)  
	View workout history per user  
	Flash messaging with visual highlighting  
	Fully automated testing with pytest
	Containerization via Docker  
	GitHub Actions for CI/CD

Branches used
	main 
	topic/new_features  - Developed new features and merged into main branch
	topic/bug_fixes - Worked on bug fixes and merged into main branch

Prerequisites
	Python 3.10+  
	Git  
	Optional: Docker (to build and run the container)

Setup and Run (Local)
	Clone the repository:
	bash
	git clone https://github.com/Dharmalakshmi/ACEest-Fitness.git
	cd ACEest-Fitness
	Install dependencies:
	pip install --upgrade pip
	pip install -r requirements.txt
	Run the Flask application:
	python app.py
	Open http://localhost:5000 in your browser.
	You can register as a new user and use login, add workout and view workouts options.

Running Tests
	To execute the unit tests: pytest
	Tests cover login/registration, workout addition, duplicate validation, and route access control.

Docker
	To build and run the application inside a Docker container:
	Then access the application at http://localhost:5000

CI/CD Pipeline
This repository includes a GitHub Actions workflow that triggers on every push or pull request. It performs:
	Python-based unit testing using pytest
	Docker image build
	Running tests inside the container to verify environment parity
	You can find the workflow in .github/workflows/tests.yml

Future Enhancements
	Persist workout and user data in a SQLite or other database
	Secure password storage with hashing (e.g., bcrypt)
	Add Logout timer or session expiration


Author: Dharmalakshmi
Contributions, bug reports, and feature requests are welcome!

