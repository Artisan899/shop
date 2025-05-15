// Все функции для работы с корзиной
function updateCartIcon() {
    fetch('/get_cart_count')
        .then(response => response.json())
        .then(data => {
            const cartIcon = document.getElementById('cart-icon');
            let imageName = 'basket.jpg';
            const count = data.cart_count;

            if (count >= 1 && count <= 5) {
                imageName = `basket${count}.jpg`;
            } else if (count > 5) {
                imageName = 'basket55.jpg';
            }

            if (cartIcon) {
                cartIcon.src = `/static/pin/${imageName}`;
            }
        });
}

function addToCart(button, productId, productType) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${productId}&product_type=${productType}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const cardBody = button.closest('.card-body');
            const controls = cardBody.querySelector('.cart-controls');
            button.classList.add('d-none');
            controls.classList.remove('d-none');
            updateCartIcon();
        }
    });
}

// ... остальные функции корзины