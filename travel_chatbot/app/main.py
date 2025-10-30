from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import connect_db, disconnect_db
from app.api.v1.router import api_router
from app.services.websocket_service import router as ws_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


origins = [
    "https://travelbotvn29.vercel.app", 
    "https://www.travelbotvn29.vercel.app",  
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(ws_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Travel Chatbot API",
        "docs": "/docs",
        "openapi": f"{settings.API_V1_PREFIX}/openapi.json"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
