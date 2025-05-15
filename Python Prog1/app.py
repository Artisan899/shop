from flask import Flask, render_template, request, redirect, url_for, flash
from user.services import UserService
from models.build_factory import BuildFactory
from models.gpu_factory import GPUFactory
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
    cart = session.get('cart', {})
    cart_items = []

    # Загружаем все товары
    all_gpus = GPUFactory.load_gpus_from_json('data/gpus.json')
    all_builds = BuildFactory.load_builds_from_json('data/builds.json')

    # Собираем информацию о товарах в корзине
    for key, quantity in cart.items():
        product_type, product_id = key.split('_', 1)

        if product_type == 'gpu':
            product = next((g for g in all_gpus if g.id == product_id), None)
        elif product_type == 'build':
            product = next((b for b in all_builds if b.id == product_id), None)

        if product:
            cart_items.append({
                'id': key,
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })

    # Считаем общую сумму
    total = sum(item['total_price'] for item in cart_items)

    return render_template('cart.html',
                           cart_items=cart_items,
                           total=total)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}  # Полностью очищаем корзину
    session.modified = True  # Гарантируем сохранение изменений
    return jsonify({'success': True, 'cart_count': 0})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product_type = request.form.get('product_type')  # 'gpu' или 'build'

    # Получаем текущую корзину из сессии или создаём новую
    cart = session.get('cart', {})

    # Добавляем/обновляем товар в корзине
    key = f"{product_type}_{product_id}"
    cart[key] = cart.get(key, 0) + 1

    # Сохраняем обновлённую корзину в сессию
    session['cart'] = cart

    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })

@app.route('/get_cart_count')
def get_cart_count():
    cart = session.get('cart', {})
    return jsonify({
        'cart_count': sum(cart.values())
    })


@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    product_type = request.form.get('product_type')
    quantity = int(request.form.get('quantity', 1))

    cart = session.get('cart', {})
    key = f"{product_type}_{product_id}"

    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity

    session['cart'] = cart
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })


@app.route('/builds')
def builds():
    builds = BuildFactory.load_builds_from_json('data/builds.json')
    cart = session.get('cart', {})
    cart_build_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('build_')]
    return render_template('builds.html', builds=builds, cart_ids=cart_build_ids)

@app.route('/gpus')
def gpus():
    gpus = GPUFactory.load_gpus_from_json('data/gpus.json')
    cart = session.get('cart', {})
    cart_gpu_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('gpu_')]
    return render_template('gpus.html', gpus=gpus, cart_ids=cart_gpu_ids)




if __name__ == '__main__':
    app.run(debug=True, port=8080)