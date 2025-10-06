# 🛍️ Shopping Store — FastAPI + HTML/CSS/JS

A simple, lightweight **shopping cart web application** built with **FastAPI** as the backend and **HTML/CSS/JavaScript** for the frontend.
It allows users to browse products, add them to the cart, update quantities, and checkout with a generated receipt.

---

## 🎥 Demo

🔗 **Video Demonstration:** [Click here to watch the demo](https://www.loom.com/share/b9658075c992495c92fcb9216e8b2523)
🔗 **Live Deployment (Render):** [View on Render](https://hackathon-host.onrender.com/home) *(Please allow ~30 seconds delay — Render pods may spin down after inactivity.)*

---

## 🧠 Assumptions Made

* Product list is **static** (does not change dynamically).
  → If 10 products exist, those 10 remain consistent during a session.As, I don't reset the already saved item if the id changed, it would result in error.
* Each product has **unlimited stock quantity** (for simplicity).
* API may **occasionally fail** or return invalid data — error handling and validation are built in.
* **Negative or invalid quantities** are prevented at the frontend, but additional backend checks exist for robustness.
* Checkout includes success/failure handling with receipt messages.

---

## ⚙️ Tech Stack

**Frontend:**

* HTML, CSS, JavaScript (no frameworks used)
* LocalStorage for cart persistence

**Backend:**

* [FastAPI](https://fastapi.tiangolo.com/) (Python)
* RESTful endpoints for `/products` and `/checkout`


**Serving Static Files:**

* The **frontend (HTML, CSS, JS)** is served directly by **FastAPI** using `StaticFiles`.
In `server.py`, this is done with:

  ```python
  from fastapi.staticfiles import StaticFiles

  app.mount("/home", StaticFiles(directory="frontend", html=True), name="static")
  ```


**Testing:**

* [pytest](https://docs.pytest.org/) for automated backend testing
* FastAPI’s built-in `TestClient`

---

## 🧩 Project Structure

```
📦 Hackathon
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js
│       ├── cart.js
│       ├── ui.js
│       └── main.js
│
├── server.py
├── test_products.py
├── test_checkout.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started (Run Locally)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/itsashishrath/Hackathon.git
cd Hackathon
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI server

```bash
uvicorn server:app --reload
```

### 5️⃣ Open the app

Go to 👉 **[http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)** in your browser.

---

## 🧪 Running Tests

All backend unit tests are built with **pytest**.

```bash
pytest -v
```

This runs:

* `test_products.py` — validates `/products` endpoint
* `test_checkout.py` — validates `/checkout` endpoint (success, invalid data, etc.)

---

## 🧱 API Endpoints

### `GET /products`

Returns a list of all available products.

**Response Example:**

```json
[
  {
    "id": 1,
    "name": "Fresh Bananas",
    "price": 1.49,
    "imageUrl": "https://..."
  }
]
```

### `POST /checkout`

Accepts a list of ordered items.

**Request Example:**

```json
[
  { "id": 1, "quantity": 2 },
  { "id": 3, "quantity": 1 }
]
```

**Response Example:**

```json
{
  "message": "Checkout successful",
  "total_amount": 7.97,
  "status": "success"
}
```

---

## 🧰 Error Handling

* Returns appropriate HTTP codes (`400`, `404`, `500`) for validation and server errors.
* Displays frontend modals for:

  * ✅ Successful checkout
  * ⚠️ Checkout failed

---

## 🧑‍💻 Author

**Ashish Rathore**
📧 [anandashish654@gmail.com](mailto:anandashish654@gmail.com)