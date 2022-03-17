from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import pet_router, customer_router, adoption_router, report_router

app = FastAPI(title="Buchi", version="1.0.0 beta", description="Buchi, a pet discovery and adoption platform")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/")
def index():
    return {"message": "Welcome to buchi api"}

app.mount("/cdn", StaticFiles(directory="cdn"), "cdn")

app.include_router(pet_router.router)
app.include_router(customer_router.router)
app.include_router(adoption_router.router)
app.include_router(report_router.router)