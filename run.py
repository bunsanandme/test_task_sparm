from app import app, db
from app.models import User

# Менеджер контекста Для Flask Shell
# Удобство для редактирования пользователей
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}