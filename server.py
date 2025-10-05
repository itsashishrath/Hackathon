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
    {"id": 1, "name": "Product A", "price": 10.99, "stock": 5, "imageUrl": "https://placehold.co/400x200.png?text=Product_1"},
    {"id": 2, "name": "Product B", "price": 15.49, "stock": 2, "imageUrl": "https://placehold.co/400x200.png?text=Product_2"},
    {"id": 3, "name": "Product C", "price": 7.99, "stock": 0, "imageUrl": "https://placehold.co/400x200.png?text=Product_3"},
    {"id": 4, "name": "Product D", "price": 12.99, "stock": 10, "imageUrl": "https://placehold.co/400x200.png?text=Product_4"},
    {"id": 5, "name": "Product E", "price": 5.99, "stock": 1, "imageUrl": "https://placehold.co/400x200.png?text=Product_5"},
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
            if product["stock"] <= 0:
                raise HTTPException(status_code=400, detail=f"Product '{product['name']}' is out of stock.")
            if order_item["quantity"] > product["stock"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Requested quantity ({order_item['quantity']}) exceeds available stock ({product['stock']}) for '{product['name']}'."
                )

            # Update stock and calculate total
            product["stock"] -= order_item["quantity"]
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
        # Automatically handled by FastAPI, but you can customize output
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
