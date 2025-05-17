from flask import Flask, render_template, request, redirect, url_for, flash

from user.services import UserService

# Все вкладки
from models.build_factory import BuildFactory
from models.gpu_factory import GPUFactory
from models.cpu_factory import CPUFactory
from models.motherboard_factory import MotherboardFactory


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
        return redirect(url_for('register_page'))

    # Проверка на занятость email
    if user_service.is_email_taken(email):
        flash("Пользователь с таким email уже существует", 'danger')
        return redirect(url_for('register_page'))

    # Регистрация пользователя
    try:
        user_service.add_user(username, email, password)
        flash("Регистрация успешна! Вам начислено 1000 бонусных баллов.", 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash(f"Ошибка при регистрации: {str(e)}", 'danger')
        return redirect(url_for('register_page'))


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
            session['username'] = user['username']  # Сохраняем имя пользователя в сессии
            flash("Вход успешен!", 'success')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Удаляем имя пользователя из сессии
    flash("Вы успешно вышли из системы", 'success')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    try:
        # Загружаем хиты продаж из JSON
        with open('data/hit_products.json', 'r') as f:
            hit_list = json.load(f)['hit_products']

        # Загружаем все товары через фабрики
        gpus = GPUFactory.load_gpus_from_json('data/gpus.json')
        builds = BuildFactory.load_builds_from_json('data/builds.json')
        cpus = CPUFactory.load_cpus_from_json('data/cpus.json')

        # Собираем хиты продаж в унифицированном формате
        hit_products = []
        for item in hit_list:
            product = None
            product_type = None

            if item['type'] == 'PC':
                product = next((b for b in builds if b.id == item['id']), None)
                product_type = 'build'
            elif item['type'] == 'GPU':
                product = next((g for g in gpus if g.id == item['id']), None)
                product_type = 'gpu'
            elif item['type'] == 'CPU':
                product = next((c for c in cpus if c.id == item['id']), None)
                product_type = 'cpu'

            if product:
                hit_products.append({
                    'product': product,
                    'type': product_type
                })

        # Получаем текущую корзину из сессии
        cart = session.get('cart', {})

        return render_template('home.html',
                               hit_products=hit_products,
                               cart=cart)

    except Exception as e:
        print(f"Error loading hit products: {str(e)}")
        return render_template('home.html',
                               hit_products=[],
                               cart={})


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []

    # Загружаем все товары как объекты
    all_gpus = GPUFactory.load_gpus_from_json('data/gpus.json')
    all_builds = BuildFactory.load_builds_from_json('data/builds.json')
    all_cpus = CPUFactory.load_cpus_from_json('data/cpus.json')
    all_motherboards = MotherboardFactory.load_motherboards_from_json('data/motherboards.json')

    # Собираем информацию о товарах в корзине
    for key, quantity in cart.items():
        product_type, product_id = key.split('_', 1)

        product = None
        if product_type == 'gpu':
            product = next((g for g in all_gpus if g.id == product_id), None)
        elif product_type == 'build':
            product = next((b for b in all_builds if b.id == product_id), None)
        elif product_type == 'cpu':
            product = next((c for c in all_cpus if c.id == product_id), None)
        elif product_type == 'motherboard':
            product = next((m for m in all_motherboards if m.id == product_id), None)

        if product:
            cart_items.append({
                'id': key,
                'product': product.to_dict(),
                'quantity': quantity,
                'total_price': product.price * quantity
            })

    total = sum(item['total_price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    try:
        # Полностью очищаем корзину
        session['cart'] = {}
        session.modified = True

        # Логируем действие
        print("Корзина полностью очищена")

        return jsonify({
            'success': True,
            'cart_count': 0,
            'message': 'Корзина очищена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        product_type = request.form.get('product_type')

        if not product_id or not product_type:
            return jsonify({'success': False, 'error': 'Missing product data'}), 400

        cart = session.get('cart', {})
        key = f"{product_type}_{product_id}"
        cart[key] = cart.get(key, 0) + 1
        session['cart'] = cart
        session.modified = True

        return jsonify({
            'success': True,
            'cart_count': sum(cart.values())
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500




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
    session.modified = True
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })

@app.route('/get_cart_count')
def get_cart_count():
    cart = session.get('cart', {})
    print(f"Cart contents: {cart}")  # Отладочный вывод
    return jsonify({
        'cart_count': sum(cart.values())
    })


@app.route('/builds')
def builds():
    builds = BuildFactory.load_builds_from_json('data/builds.json')
    cart = session.get('cart', {})
    cart_build_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('build_')]
    return render_template('builds.html',
                         builds=builds,
                         cart=cart,
                         product_type='build',
                         cart_ids=cart_build_ids)

@app.route('/gpus')
def gpus():
    gpus = GPUFactory.load_gpus_from_json('data/gpus.json')
    cart = session.get('cart', {})
    cart_gpu_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('gpu_')]
    return render_template('gpus.html',
                         gpus=gpus,
                         cart=cart,
                         product_type='gpu',
                         cart_ids=cart_gpu_ids)


@app.route('/cpus')
def cpus():
    cpus = CPUFactory.load_cpus_from_json('data/cpus.json')
    cart = session.get('cart', {})
    cart_cpu_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('cpu_')]
    return render_template('cpus.html',
                         cpus=cpus,
                         cart=cart,
                         product_type='cpu',
                         cart_ids=cart_cpu_ids)

@app.route('/motherboards')
def motherboards():
    motherboards = MotherboardFactory.load_motherboards_from_json('data/motherboards.json')
    cart = session.get('cart', {})
    cart_mb_ids = [key.split('_')[1] for key in cart.keys() if key.startswith('motherboard_')]
    return render_template('motherboards.html',
                         motherboards=motherboards,
                         cart=cart,
                         product_type='motherboard',
                         cart_ids=cart_mb_ids)



if __name__ == '__main__':
    app.run(debug=True, port=8080)