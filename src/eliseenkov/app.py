from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Секретный ключ обязателен для работы сессий
app.secret_key = 'super_secret_key_change_me_in_production_12345'

# --- Настройка Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'  # Куда редиректить, если не авторизован
login_manager.login_message = "Пожалуйста, войдите в систему, чтобы получить доступ к этой странице."

# --- Класс пользователя для Flask-Login ---
class User(UserMixin):
    def __init__(self, id, username, email, balance):
        self.id = id
        self.username = username
        self.email = email
        self.balance = balance

# --- Функция, которую Flask-Login использует для загрузки пользователя из сессии ---
@login_manager.user_loader
def load_user(user_id):
    try:
        cnx = connection()
        cur = cnx.cursor(dictionary=True)
        cur.execute('SELECT id, username, email, balance FROM users WHERE id = %s', (user_id,))
        row = cur.fetchone()
        cur.close()
        cnx.close()
        if row:
            return User(row['id'], row['username'], row['email'], row['balance'])
    except Exception as e:
        print("Ошибка загрузки пользователя:", e)
    return None

def connection():
    return mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123"
    )

# --- РЕГИСТРАЦИЯ ---
@app.route('/user_register', methods=['POST'])
def user_register():
    try:
        req = request.get_json(force=True)
        name = req.get('name', '').strip()
        login = req.get('email', '').strip()
        password = req.get('password', '').strip()

        if not name or not login or not password:
            return jsonify({"success": False, "message": "Все поля должны быть заполнены!"}), 400

        hashed_password = generate_password_hash(password)
        
        cnx = connection()
        cur = cnx.cursor()
        
        # Проверка на дубликат email
        cur.execute('SELECT id FROM users WHERE email=%s', (login,))
        if cur.fetchone():
            cur.close(); cnx.close()
            return jsonify({"success": False, "message": "Пользователь с таким email уже существует!"}), 400

        # Вставляем нового пользователя (balance подставится как 0 по умолчанию)
        cur.execute(
            'INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', 
            (name, login, hashed_password)
        )
        cnx.commit()
        cur.close()
        cnx.close()
        
        return jsonify({"success": True, "message": "Регистрация прошла успешно! Теперь войдите."})
        
    except Exception as e:
        print("❌ Ошибка регистрации:", e)
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"}), 500

# --- АВТОРИЗАЦИЯ ---
@app.route('/user_login', methods=['POST'])
def user_login_route():
    try:
        req = request.get_json(force=True)
        login = req.get('email', '').strip()
        password = req.get('password', '').strip()

        if not login or not password:
            return jsonify({"success": False, "message": "Введите email и пароль"}), 400
        
        cnx = connection()
        cur = cnx.cursor(dictionary=True)
        cur.execute('SELECT id, username, email, password_hash, balance FROM users WHERE email=%s', (login,))
        row = cur.fetchone()
        cur.close()
        cnx.close()
        
        if row and check_password_hash(row['password_hash'], password):
            # Создаём объект пользователя и "логиним" его через Flask-Login
            user = User(row['id'], row['username'], row['email'], row['balance'])
            login_user(user)
            return jsonify({"success": True, "message": "Вход выполнен успешно!"})
        else:
            return jsonify({"success": False, "message": "Неверный email или пароль"}), 401
            
    except Exception as e:
        print("❌ Ошибка входа:", e)
        return jsonify({"success": False, "message": "Ошибка сервера"}), 500

# --- СТРАНИЦА ПРОФИЛЯ (доступна только авторизованным) ---
@app.route("/profile")
@login_required  # 🔒 Магия Flask-Login: если пользователь не вошёл — редирект на /login
def profile():
    # current_user - это глобальный объект текущего авторизованного пользователя
    return render_template('profile.html', user=current_user)

# --- ВЫХОД ---
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

# --- СТРАНИЦЫ ---
@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)