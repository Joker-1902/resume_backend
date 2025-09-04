from fastapi import FastAPI
from backend.routers import router, user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
app.include_router(user_router)
origins = [
    'https://resume-project-z732.onrender.com',
    'http://localhost:7135'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)