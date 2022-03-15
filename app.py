from fastapi import FastAPI
from routers import pet_router, customer_router, adoption_router, report_router

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to buchi api"}

app.include_router(pet_router.router)
app.include_router(customer_router.router)
app.include_router(adoption_router.router)
app.include_router(report_router.router)