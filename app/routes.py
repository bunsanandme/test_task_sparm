from app import app, db
from app.models import *
from flask import jsonify, request, abort
from flask_login import current_user, login_user, logout_user, login_required
import json

@app.errorhandler(401)
def page_not_found(e):
    return {"error": "Unauthorized"}

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}

@app.errorhandler(405)
def method_not_allowed(e):
    return {"error": "Method not allowed"}



@app.route('/api/login/', methods=["POST"])
def signup_user():
    if current_user.is_authenticated:
        return {"error": "User already logged in"}, 400
    login = request.get_json().get('login')
    password = request.get_json().get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user is None or not user.check_password(password):
            return {"error": "Invalid data"}, 400
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
        return {"error": "User already logged in"}, 400
    
    raw_data = request.get_json()
    password = request.get_json().get('password')
    del raw_data["password"]

    # 4:39. Сейчас я считаю это лучшей фильтрацией полей по пересечению множеств полей модели и полей JSON
    data = {key: raw_data[key] for key in set(raw_data.keys()) & set(get_fields_names(User))}

    if User.query.filter_by(login=data["login"]).first():
        return {"error" : "User with this login already exists"}, 400

    new_user = User(**data)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()



@app.route('/api/user/', methods=["GET"])
@login_required
def get_current_user():
    return current_user.to_dict()

@app.route('/api/user/<user_id>/', methods=["GET", "PUT", "DELETE"])
@login_required
def get_or_change_user(user_id):
    user = User.query.get(user_id)
    user_documents = Document.query.filter_by(user_id=user_id)

    if not user:
        abort(404)

    if request.method == "GET":
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
    
    if request.method == "DELETE":
        Document.query.filter_by(user_id=user_id).delete(synchronize_session="fetch")
        db.session.delete(user)
        db.session.commit()
        return {"info": "Succesfully deleted"}, 204


@app.route('/api/all_users/', methods=["GET"])
@login_required
def get_all_users():
    if current_user.type_id != 2:
         return {"error": "Access denied"}, 403
    
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

@app.route('/api/document/<document_id>/', methods=["GET", "PUT", "DELETE"])
@login_required
def get_or_change_document(document_id):
    document = Document.query.get(document_id)

    if not document:
        abort(404)

    if request.method == "GET":
        response = document.to_dict()
        return response
    
    if request.method == "PUT":
        raw_data = request.get_json()
        document.type_id = raw_data.pop("documentType_id")
        if id in raw_data:
            document.id = raw_data.pop("id")

        detail_data = json.loads(document.data.replace("'", '"').replace("None", "null"))
        print(detail_data)
        for key, value in raw_data.items():
            detail_data[key] = value
        document.data = str(detail_data)
        db.session.commit()

        return document.to_dict()
    
    if request.method == "DELETE":
        db.session.delete(document)
        db.session.commit()
        return {"info": "Succesfully deleted"}, 204
    
@app.route('/api/procces_request/', methods=["POST"])
@login_required
def procces_request():
    for data_first_step in request.get_json():
        for data_second_step in data_first_step["Data"]:
            for data_third_step in data_second_step["Users"]:
                
                user_data = dict()

                credentials = data_third_step["Credentials"]
                user_data["login"] = credentials["username"]
                new_password = credentials["pass"]

                for key in set(data_third_step.keys()) & set(get_fields_names(User)):
                    user_data[key] = data_third_step[key]

                if User.query.filter_by(login=user_data["login"]).first():
                    return {"error" : "User with this login already exists"}, 400

                new_user = User(**user_data)
                new_user.set_password(new_password)
                
                db.session.add(new_user)
                db.session.commit()

                documents_data = data_third_step["Documents"]
                for document in documents_data:
                    document_type = document.pop("documentType_id")
                    document_id = document.pop("id")

                    new_document = Document(id=document_id, type_id=document_type, data=str(document), user_id = new_user.id)
                    db.session.add(new_document)
                    db.session.commit()

                user_data.clear()
    response = new_user.to_dict()
    response["documents"] = [document.to_dict() for document in Document.query.filter_by(user_id=new_user.id)]
    return response
