from app import app, db
from app.models import *
from flask import jsonify, request, session
from flask_login import current_user, login_user, logout_user


@app.route('/api/hello', methods=["GET"])
def hello():
    response = {
        'message': 'Hello, World!'
    }
    return jsonify(response)

@app.route('/api/login/', methods=["POST"])
def signup_user():
    if current_user.is_authenticated:
        return {"error": "User already logged in"}
    login = request.get_json().get('login')
    password = request.get_json().get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user is None or not user.check_password(password):
            return {"error": "Invalid data"}
        login_user(user)
        
        return user.to_dict(), 200

@app.route('/api/logout/')
def logout():
    logout_user()
    return {"info": "Logged out. Good bye!"}
