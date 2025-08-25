
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth_routes, ticket_routes, webhook_routes

load_dotenv()

app = FastAPI(title="Chatbot Ticketing API")

origins = [os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"ok": True, "service": "chatbot-ticketing"}

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(ticket_routes.router, prefix="/tickets", tags=["tickets"])
app.include_router(webhook_routes.router, prefix="/webhook", tags=["webhook"])

