from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Allow all origins for simplicity (to be restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcoded products added stocks
products = [
    {
        "id": 1,
        "name": "Fresh Bananas (1 kg)",
        "price": 1.49,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg"
    },
    {
        "id": 2,
        "name": "Whole Milk (1L)",
        "price": 2.19,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Milk_glass.jpg"
    },
    {
        "id": 3,
        "name": "Brown Bread Loaf (400g)",
        "price": 2.99,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Loaf_of_bread..jpg"
    },
    {
        "id": 4,
        "name": "Free Range Eggs (12 pack)",
        "price": 3.59,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Eggs_in_carton.jpg"
    },
    {
        "id": 5,
        "name": "Apples (1 kg)",
        "price": 2.79,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"
    },
    {
        "id": 6,
        "name": "Potato Chips (200g)",
        "price": 1.99,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/6/69/Potato-Chips.jpg"
    },
    {
        "id": 7,
        "name": "Orange Juice (1L)",
        "price": 3.49,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/0/05/Orangejuice.jpg"
    },
    {
        "id": 8,
        "name": "Mangoes (500g)",
        "price": 5.49,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/4/40/Mango_4.jpg"
    },
    {
        "id": 9,
        "name": "Cheddar Cheese (250g)",
        "price": 4.29,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/4/45/Cheese.jpg"
    },
    {
        "id": 10,
        "name": "Tomatoes (500g)",
        "price": 1.99,
        "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/8/88/Bright_red_tomato_and_cross_section02.jpg"
    }
]


app.mount("/home", StaticFiles(directory="frontend", html=True), name="static")


@app.get("/products", response_class=JSONResponse)
async def get_products():
    """Fetch all available products."""
    return JSONResponse(content=products, status_code=status.HTTP_200_OK)


@app.post("/checkout", response_class=JSONResponse)
async def checkout(request: Request):
    """
    Process checkout request.
    Expected input: [{"id": 1, "quantity": 2}, {"id": 3, "quantity": 1}]
    """
    try:
        data = await request.json()

        # Validate input type
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise HTTPException(status_code=400, detail="Invalid data format. Expected a list of objects.")

        # Validate fields
        for item in data:
            if "id" not in item or "quantity" not in item:
                raise HTTPException(status_code=400, detail="Each item must include 'id' and 'quantity' fields.")
            if not isinstance(item["id"], int) or not isinstance(item["quantity"], int):
                raise HTTPException(status_code=400, detail="'id' and 'quantity' must be integers.")
            if item["quantity"] <= 0:
                raise HTTPException(status_code=400, detail="Quantity must be at least 1.")

        total_cost = 0
        for order_item in data:
            product = next((p for p in products if p["id"] == order_item["id"]), None)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {order_item['id']} not found.")
            total_cost += product["price"] * order_item["quantity"]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Checkout successful",
                "total_amount": round(total_cost, 2),
                "status": "success",
            },
        )

    except HTTPException as http_err:
        return JSONResponse(
            status_code=http_err.status_code,
            content={"message": http_err.detail, "status": "error"},
        )

    except Exception as e:
        print("Error processing order:", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error", "status": "error"},
        )
