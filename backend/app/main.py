# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

# --- Initialize FastAPI app ---
app = FastAPI(title="Financial QA & Insights API")

# --- CORS settings for Frontend (Next.js) ---
origins = [
    "http://localhost:3000",  # Next.js local
    "http://127.0.0.1:3000",
    # You can add deployed URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Router ---
app.include_router(router)

# --- Root endpoint ---
@app.get("/")
def root():
    return {"message": "Financial QA & Insights API is running 🚀"}