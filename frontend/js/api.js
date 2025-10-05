export async function fetchProducts() {
    const res = await fetch('/products');
    return await res.json();
}

export async function checkout(order) {
    const res = await fetch('/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
    });
    return await res.json();
}
