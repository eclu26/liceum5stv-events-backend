from fastapi import FastAPI

from app.api_v1 import users

app = FastAPI(title="Lyceum 5 Stavropol Events API", version="1.0.0")

app.include_router(users.router)

@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}