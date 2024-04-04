from app import app, db
from app.models import *
from flask import jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
import json

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


@app.route('/api/logout/', methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"info": "Logged out. Good bye!"}


@app.route('/api/register/', methods=["POST"])
def register():
    if current_user.is_authenticated:
        return {"error": "User already logged in"}
    
    raw_data = request.get_json()
    password = request.get_json().get('password')
    del raw_data["password"]

    # 4:39. Сейчас я считаю это лучшей фильтрацией полей по пересечению множеств полей модели и полей JSON
    data = {key: raw_data[key] for key in set(raw_data.keys()) & set(get_fields_names(User))}

    if User.query.filter_by(login=data["login"]).first():
        return {"error" : "User with this login already exists"}

    new_user = User(**data)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()



@app.route('/api/user/', methods=["GET"])
@login_required
def get_current_user():
    return current_user.to_dict()

@app.route('/api/user/<user_id>/', methods=["GET", "PUT"])
@login_required
def get_or_change_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.method == "GET":
        user_documents = Document.query.filter_by(user_id=user_id)

        response = user.to_dict()
        response["documents"] = [document.to_dict() for document in user_documents]
        return response
    
    if request.method == "PUT":
        raw_data = request.get_json()

        if "password" in raw_data.keys():
            new_password = raw_data.pop("password")
            user.set_password(new_password)

        data = {key: raw_data[key] for key in set(raw_data.keys()) & set(get_fields_names(User))}

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()
        return user.to_dict()

@app.route('/api/all_users/', methods=["GET"])
@login_required
def get_all_users():
    if current_user.type_id != 2:
         return {"error": "Access denied"}
    
    users = User.query.all()
    response = [user.to_dict() for user in users]
    for user in response:
        user["documents"] = [document.to_dict() for document in Document.query.filter_by(user_id=user["id"])]
    return response




@app.route('/api/new_document/', methods=["POST"])
@login_required
def create_document():
    raw_data = request.get_json()
    document_type = raw_data.pop("documentType_id")
    document_id = raw_data.pop("id")
    document = Document(id=document_id, type_id=document_type, data=str(raw_data))

    db.session.add(document)
    db.session.commit()
    return document.to_dict()