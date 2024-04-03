from app import db, login_manager
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(255), nullable=True) 
    first_name = db.Column(db.String(255), nullable=True)
    patr_name = db.Column(db.String(255), nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey("genders.id"))
    type_id = db.Column(db.Integer, db.ForeignKey("user_types.id"))
    login = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'id': self.id,
            'login': self.login,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'patr_name': self.patr_name,
            'gender': str(Genders.query.filter_by(id=self.gender_id).first()),
            "type": str(User_types.query.filter_by(id=self.type_id).first()),
        }
        return data

    def __str__(self) -> str:
        return f"<{self.id}:{self.login}>"
    

class Genders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True)

    def __str__(self):
        return f'{self.name}'


class User_types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True)

    def __str__(self):
        return f'{self.name}'


class Document_types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True)

    def __str__(self):
        return f'<Тип документа — {self.name}>'


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(9000))
    user_id = db.Column(db.Integer, )
    type_id = db.Column(db.Integer, )

    def __str__(self):
        return f'<Документ с номером {self.id}>'