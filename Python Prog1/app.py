from flask import Flask, render_template, request, redirect, url_for, flash
from user.services import UserService
from models.build_factory import BuildFactory
from flask import jsonify
from flask import session



import json


app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Добавьте секретный ключ для работы с flash-сообщениями
user_service = UserService("data/users.json")


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Проверка на совпадение паролей
    if password != confirm_password:
        flash("Пароли не совпадают", 'danger')
        return redirect(url_for('index'))

    # Регистрация пользователя
    try:
        user_service.add_user(username, email, password)
        flash("Регистрация успешна!", 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = user_service.get_user(username)

        if not user:
            flash("Пользователь с таким именем не найден", 'danger')
        elif not user_service.check_password(user['password'], password):
            flash("Неверный пароль", 'danger')
        else:
            flash("Вход успешен!", 'success')
            return redirect(url_for('home'))  # Переход на домашнюю страницу (пока пустую)

    return render_template('login.html')


@app.route('/home')
def home():
    with open('data/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    return render_template('home.html', products=products)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)


def load_builds():
    with open('data/builds.json', 'r', encoding='utf-8') as f:
        return json.load(f)






@app.route('/builds')
def builds():
    builds = BuildFactory.load_builds_from_json('data/builds.json')
    cart = session.get('cart', [])
    cart_ids = [item['id'] for item in cart]
    return render_template('builds.html', builds=builds, cart_ids=cart_ids)




if __name__ == '__main__':
    app.run(debug=True, port=8080)
