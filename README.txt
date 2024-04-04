Настройка вирутального окружения

python -m venv .env
.\.env\Scripts\activate
pip install -r requirements.txt

НАСТРОЙКА БАЗЫ ДАННЫХ

Проверить переменную SQLALCHEMY_DATABASE_URI 
Формат для БД MySQL "mysql://username:password@localhost:port/test"

flask db init
flask db migrate
flask db upgrade

ЗАГРУЗКА НАЧАЛЬНЫХ ДАННЫХ

flask shell

d1 = DocumentType(id=1, name="Паспорт")
d2 = DocumentType(id=2, name="Полис")
d3 = DocumentType(id=3, name="СНИЛС")
d4 = DocumentType(id=4, name="ИНН")
g1 = GenderType(id=1, name="Мужчина")
g2 = GenderType(id=2, name="Женщина")
db.session.add(d1)
db.session.add(d2)
db.session.add(d3)
db.session.add(d4)
db.session.add(g1)
db.session.add(g2)
db.session.commit()

РАБОТА C API

Создание пользователя посредством POST-запрос http://localhost:5000/api/register/ с телом 

{
	"login": "root",
	"password": "root"	
}

Для посылки JSON-запроса POST http://localhost:5000/api/procces_request/

