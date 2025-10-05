import { fetchProducts, checkout as checkoutAPI } from "./api.js";
import {
  addToCart,
  updateQty,
  removeFromCart,
  getCart,
  clearCart,
} from "./cart.js";
import { renderProducts, renderCart, toggleCart, showReceipt } from "./ui.js";

let products = [];

document.addEventListener("DOMContentLoaded", async () => {
  products = await fetchProducts();
  renderProducts(products);
  renderCart(products);

  document.getElementById("products").addEventListener("click", (e) => {
    if (e.target.classList.contains("add-to-cart")) {
      addToCart(e.target.dataset.id);
      renderCart(products);
    }
  });

  document.getElementById("cart-items").addEventListener("input", (e) => {
    if (e.target.classList.contains("qty-input")) {
      updateQty(e.target.dataset.id, parseInt(e.target.value));
      renderCart(products);
    }
  });

  document.getElementById("cart-items").addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-item")) {
      removeFromCart(e.target.dataset.id);
      renderCart(products);
    }
  });

  document
    .getElementById("cart-button")
    .addEventListener("click", () => toggleCart(true));
  document
    .getElementById("close-cart")
    .addEventListener("click", () => toggleCart(false));

  document
    .getElementById("checkout-btn")
    .addEventListener("click", async () => {
      const order = Object.entries(getCart()).map(([id, qty]) => ({
        id: parseInt(id),
        quantity: qty,
      }));
      const res = await checkoutAPI(order);

      if (res && res.message) {
        showReceipt(res, order, products);
        clearCart();
        renderCart(products);
        toggleCart(false);
      }
    });
});
