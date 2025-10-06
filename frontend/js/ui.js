import { checkout } from './api.js';
import { addToCart,updateQty, getCart, getTotal, updateCartCount } from './cart.js';

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
    if (Object.keys(cart).length === 0) {
        document.getElementById('cart-items').innerHTML = '<p>Your cart is empty.</p>';
        document.getElementById('cart-total').innerText = '0.00';
        updateCartCount();
        document.getElementById("checkout-btn").disabled = true;
        return;
    }
    document.getElementById("checkout-btn").disabled = false;
    const container = document.getElementById('cart-items');
    container.innerHTML = '';

    for (let id in cart) {
        const product = products.find(p => p.id == id);
        const qty = cart[id];
        const item = document.createElement('div');
        item.className = 'cart-item';
        item.innerHTML = `
            <span title="${product.name}">${product.name} ($${product.price.toFixed(2)})</span>
            <div class="qty-control">
                <button class="qty-decrease" data-id="${id}" ${qty <= 1 ? 'disabled' : ''}>−</button>
                <input type="number" min="1" value="${qty}" data-id="${id}" class="qty-input">
                <button class="qty-increase" data-id="${id}">+</button>
            </div>
            <button class="remove-item" data-id="${id}">Remove</button>
        `;
        container.appendChild(item);
    }

    document.getElementById('cart-total').innerText = getTotal(products).toFixed(2);
    updateCartCount();

    // functionlity for + and − buttons
    container.querySelectorAll('.qty-increase').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const input = container.querySelector(`.qty-input[data-id="${id}"]`);
            input.value = parseInt(input.value) + 1;
            addToCart(id);
        });
    });

    container.querySelectorAll('.qty-decrease').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const input = container.querySelector(`.qty-input[data-id="${id}"]`);
            input.value = Math.max(1, parseInt(input.value) - 1);
            const currentQty = cart[id];
            if (currentQty > 1) {
                updateQty(id, currentQty - 1);
            }
        });
    });
}

export function showAddToCartFeedback(button) {
    const feedback = document.createElement('span');
    feedback.className = 'add-to-cart-feedback';
    feedback.textContent = '+1';

    // position near the button
    const rect = button.getBoundingClientRect();
    feedback.style.left = rect.left + rect.width / 2 + 'px';
    feedback.style.top = rect.top - 10 + 'px';

    document.body.appendChild(feedback);

    setTimeout(() => feedback.remove(), 800);
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
 
export function showErrorModal(message) {
    const modal = document.getElementById('error-modal');
    document.getElementById('error-message').innerText = message;
    modal.style.display = 'flex';
    modal.querySelector('#close-error').onclick = () => {
        modal.style.display = 'none';
    };
}


