# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import query_router

app = FastAPI(title="Geo-AI Visualizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(query_router.router, prefix="/api/v1", tags=["Query"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Geo-AI Visualizer API!"}