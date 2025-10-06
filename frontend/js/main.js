import { fetchProducts, checkout as checkoutAPI } from "./api.js";
import {
  addToCart,
  updateQty,
  removeFromCart,
  getCart,
  clearCart,
} from "./cart.js";
import {
  renderProducts,
  renderCart,
  toggleCart,
  showReceipt,
  showErrorModal,
  showAddToCartFeedback
} from "./ui.js";

let products = [];

const checkoutBtn = document.getElementById("checkout-btn");

document.addEventListener("DOMContentLoaded", async () => {
  products = await fetchProducts();
  renderProducts(products);
  renderCart(products);

  document.getElementById("cart-button").addEventListener("click", () => toggleCart(true));
  document.getElementById("close-cart").addEventListener("click", () => toggleCart(false));

  document.getElementById("products").addEventListener("click", (e) => {
    if (e.target.classList.contains("add-to-cart")) {
      addToCart(e.target.dataset.id);
      renderCart(products);
      showAddToCartFeedback(e.target);
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

    // Simulate server processing delay for checkout
    async function simulateServerDelay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }

  checkoutBtn.addEventListener("click", async () => {
    checkoutBtn.disabled = true;
    checkoutBtn.innerText = "Processing...";
    const order = Object.entries(getCart()).map(([id, qty]) => ({
      id: parseInt(id),
      quantity: qty,
    }));

    try {
      await simulateServerDelay(1000); // Simulate 1 second delay
      const res = await checkoutAPI(order);
      console.log(res);

      if (res.status === "success") {
        showReceipt(res, order, products);
        clearCart();
        renderCart(products);
        toggleCart(false);
      } else {
        showErrorModal(res.message || "Payment failed. Please try again.");
      }
    } catch (error) {
      showErrorModal(error.message);
    } finally {
      checkoutBtn.disabled = false;
      checkoutBtn.innerText = "Checkout";
    }
  });
});