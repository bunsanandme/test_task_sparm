# Сервис приема JSON-запросов

## Развертывание и запуск
### Настройка вирутального окружения

Склонируйте репозиторий и в корневой папке откройте командную строку.  
Выполните эти команды:

```shell
python -m venv .env
.\.env\Scripts\activate
pip install -r requirements.txt
```
### Настройка БД(на примере MySQL)

Создайте в MySQL БД под названием "test".  
Откройте файл _config.py_ и редактируйте переменную SQLALCHEMY_DATABASE_URI

Формат URI для БД MySQL: "mysql://*username*:*password*@localhost:*port*/test"

Далее, в командной строке выполните эти команды для инициализации БД приложения. 

```shell
flask db init
flask db migrate
flask db upgrade
```

### Загрузка начальных данных

В командной строке запустить оболочку:  

```shell
flask shell
```

Вставьте эти данные:
```python
d1 = DocumentType(id=1, name="Паспорт")
d2 = DocumentType(id=2, name="Полис")
d3 = DocumentType(id=3, name="СНИЛС")
d4 = DocumentType(id=4, name="ИНН")
g1 = GenderType(id=1, name="Мужчина")
g2 = GenderType(id=2, name="Женщина")
u1 = UserType(id=1, name="Администратор")
u2 = UserType(id=2, name="Пользователь")
db.session.add(d1)
db.session.add(d2)
db.session.add(d3)
db.session.add(d4)
db.session.add(g1)
db.session.add(g2)
db.session.add(u1)
db.session.add(u2)
db.session.commit()
exit()
```

Для запуска приложения выполните команду ```flask run```

## Конечные точки

|Endpoint|Methods|Rule|
|---------------------- | ----------------  |----------------------------|
create_document       |  POST              |/api/new_document/
get_all_users          | GET               |/api/all_users/
get_current_user        |GET               |/api/user/
get_or_change_document  |DELETE, GET, PUT  |/api/document/<document_id>/
get_or_change_user      |DELETE, GET, PUT  |/api/user/<user_id>/
logout                  |POST              |/api/logout/
procces_request         |POST              |/api/procces_request/
register                |POST              |/api/register/
signup_user             |POST              |/api/login/

## Работа с API

Создание пользователя посредством POST-запрос http://localhost:5000/api/register/ с телом:

```json
{
	"login": "root",
	"password": "root",
	"type_id": 1	
}
```
Авторизация пользователя посредством POST-запрос http://localhost:5000/api/login/ с телом:

```json
{
	"login": "root",
	"password": "root",	
}
```
Для посылки JSON-запроса POST http://localhost:5000/api/procces_request/

