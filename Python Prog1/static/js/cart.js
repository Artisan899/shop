function handleCartError(response) {
    if (response.status === 401) {
        alert('Для работы с корзиной необходимо войти в систему');
        window.location.href = '/login';
        return true;
    }
    return false;
}

function addToCart(button, productId, productType) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${encodeURIComponent(productId)}&product_type=${encodeURIComponent(productType)}`
    })
    .then(response => {
        if (handleCartError(response)) return;
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            button.classList.add('d-none');
            const cardBody = button.closest('.card-body');
            const controls = cardBody.querySelector('.cart-controls');
            controls.classList.remove('d-none');
            const quantityElement = controls.querySelector('.quantity');
            quantityElement.textContent = '1';
            updateCartIcon();
        }
    })
    .catch(error => console.error('Error:', error));
}

function changeQuantity(button, delta, productId, productType) {
    const controls = button.closest('.quantity-controls');
    const quantityElement = controls.querySelector('.quantity');
    const currentQuantity = parseInt(quantityElement.textContent);
    const newQuantity = currentQuantity + delta;

    if (newQuantity > 0) {
        updateCart(productId, productType, newQuantity, quantityElement);
    } else {
        // Если количество стало 0, скрываем контролы и показываем кнопку "В корзину"
        const cardBody = button.closest('.card-body');
        cardBody.querySelector('.btn-add-to-cart').classList.remove('d-none');
        cardBody.querySelector('.cart-controls').classList.add('d-none');
        updateCart(productId, productType, 0);
    }
}

function updateCart(productId, productType, quantity, quantityElement = null) {
    fetch('/update_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${productId}&product_type=${productType}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (quantityElement) {
                quantityElement.textContent = quantity;
            }
            updateCartIcon();

            // Если мы на странице корзины - перезагружаем
            if (window.location.pathname === '/cart') {
                location.reload();
            }
        }
    });
}

// Функция для очистки корзины
function clearCart() {
    if (confirm('Вы точно хотите очистить всю корзину?')) {
        fetch('/clear_cart', {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка очистки корзины');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Обновляем все кнопки на странице
                document.querySelectorAll('.btn-add-to-cart').forEach(btn => {
                    btn.classList.remove('d-none');
                });
                document.querySelectorAll('.cart-controls').forEach(controls => {
                    controls.classList.add('d-none');
                });

                updateCartIcon();

                // Если мы на странице корзины - перезагружаем
                if (window.location.pathname === '/cart') {
                    location.reload();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при очистке корзины: ' + error.message);
        });
    }
}



// Назначаем обработчик на кнопку
document.getElementById('clear-cart-btn')?.addEventListener('click', clearCart);

function updateCartIcon() {
    fetch('/get_cart_count')
        .then(response => response.json())
        .then(data => {
            const cartIcon = document.getElementById('cart-icon');
            if (cartIcon) {
                const count = data.cart_count;
                console.log('Cart count:', count);  // Отладочный вывод

                // Всегда показываем basket.jpg при пустой корзине
                const imageName = count <= 0 ? 'basket.jpg' :
                                count <= 5 ? `basket${count}.jpg` : 'basket55.jpg';
                cartIcon.src = `/static/pin/${imageName}`;
            }
        });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    updateCartIcon();

    // Обновляем состояние всех кнопок на странице
    document.querySelectorAll('.cart-controls').forEach(controls => {
        const cardBody = controls.closest('.card-body');
        const btn = cardBody.querySelector('.btn-add-to-cart');

        if (controls.classList.contains('d-none')) {
            btn.classList.remove('d-none');
        } else {
            btn.classList.add('d-none');
        }
    });
});