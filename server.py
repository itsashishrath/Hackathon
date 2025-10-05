from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow all origins for simplicity (to be restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcoded products
products = [
    {"id": 1, "name": "Product A", "price": 10.99, "imageUrl": "https://placehold.co/400x200.png?text=Product_1"},
    {"id": 2, "name": "Product B", "price": 15.49, "imageUrl": "https://placehold.co/400x200.png?text=Product_2"},
    {"id": 3, "name": "Product C", "price": 7.99, "imageUrl": "https://placehold.co/400x200.png?text=Product_3"},
    {"id": 4, "name": "Product D", "price": 12.99, "imageUrl": "https://placehold.co/400x200.png?text=Product_4"},
    {"id": 5, "name": "Product E", "price": 5.99, "imageUrl": "https://placehold.co/400x200.png?text=Product_5"},
]

from fastapi.staticfiles import StaticFiles

app.mount("/home", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/products")
async def get_products():
    return JSONResponse(products)

@app.post("/checkout")
async def checkout(request: Request):
    data = await request.json()
    print("Order received:", data)
    return {"message": "Payment successful!"}
