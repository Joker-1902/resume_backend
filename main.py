from fastapi import FastAPI
from backend.routers import router, user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)