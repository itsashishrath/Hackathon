const CART_KEY = 'cart';
let cart = JSON.parse(localStorage.getItem(CART_KEY)) || {};

export function getCart() { return cart; }

export function saveCart() {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

export function addToCart(id) {
    cart[id] = (cart[id] || 0) + 1;
    saveCart();
}

export function updateCartCount() {
    const count = Object.values(getCart()).reduce((a, b) => a + b, 0);
    document.getElementById('cart-count').innerText = count;
}


export function updateQty(id, qty) {
    if (qty <= 0) delete cart[id];
    else cart[id] = qty;
    saveCart();
}

export function removeFromCart(id) {
    delete cart[id];
    saveCart();
}

export function clearCart() {
    cart = {};
    saveCart();
}

export function getTotal(products) {
    return Object.entries(cart)
        .reduce((total, [id, qty]) => {
            const product = products.find(p => p.id == id);
            return total + product.price * qty;
        }, 0);
}
