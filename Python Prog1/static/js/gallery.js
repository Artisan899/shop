function changeImage(element, productId) {
    const gallery = element.closest('.product-gallery');
    const index = element.dataset.index;

    gallery.querySelectorAll('.thumbnail-indicator').forEach(ind => {
        ind.classList.remove('active');
    });
    element.classList.add('active');

    gallery.querySelectorAll('.main-image img').forEach(img => {
        img.classList.add('d-none');
        img.classList.remove('active');
        if (img.dataset.index === index) {
            img.classList.remove('d-none');
            img.classList.add('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.thumbnail-indicator').forEach(indicator => {
        indicator.addEventListener('click', function() {
            const productId = this.closest('.card').querySelector('.btn-add-to-cart')
                .getAttribute('onclick').match(/'([^']+)'/)[1];
            changeImage(this, productId);
        });
    });
});