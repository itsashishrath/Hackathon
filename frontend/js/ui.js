import { addToCart, getCart, getTotal, updateCartCount } from './cart.js';

export function renderProducts(products) {
    const container = document.getElementById('products');
    container.innerHTML = products.map(p => `
        <div class="product">
            <img src="${p.imageUrl}" alt="${p.name}">
            <h3>${p.name}</h3>
            <p>$${p.price.toFixed(2)}</p>
            <button class="add-to-cart" data-id="${p.id}">Add to Cart</button>
        </div>
    `).join('');
}

export function renderCart(products) {
    const cart = getCart();
    const container = document.getElementById('cart-items');
    container.innerHTML = '';
    for (let id in cart) {
        const product = products.find(p => p.id == id);
        const qty = cart[id];
        const item = document.createElement('div');
        item.className = 'cart-item';
        item.innerHTML = `
            <span>${product.name} ($${product.price.toFixed(2)})</span>
            <input type="number" min="1" value="${qty}" data-id="${id}" class="qty-input">
            <button class="remove-item" data-id="${id}">Remove</button>
        `;
        container.appendChild(item);
    }
    document.getElementById('cart-total').innerText = getTotal(products).toFixed(2);
    updateCartCount();
}

export function toggleCart(show) {
    const modal = document.getElementById('cart-modal');
    modal.style.display = show ? 'flex' : 'none';
}

export function showReceipt(response, order, products) {
    const modal = document.getElementById('receipt-modal');
    const details = document.getElementById('receipt-details');

    const date = new Date().toLocaleString();

    let html = `<p><strong>${response.message}</strong></p>`;
    html += `<p><strong>Date:</strong> ${date}</p>`;
    html += `<ul>`;
    order.forEach(item => {
        const p = products.find(p => p.id === item.id);
        html += `<li>${p.name} x ${item.quantity} — $${(p.price * item.quantity).toFixed(2)}</li>`;
    });
    html += `</ul>`;
    html += `<p><strong>Total:</strong> $${order.reduce((t, o) => {
        const p = products.find(p => p.id === o.id);
        return t + p.price * o.quantity;
    }, 0).toFixed(2)}</p>`;

    details.innerHTML = html;

    modal.querySelector('.cart-content').classList.add('success');
    modal.style.display = 'flex';

    document.getElementById('close-receipt').onclick = () => {
        modal.style.display = 'none';
    };
}

