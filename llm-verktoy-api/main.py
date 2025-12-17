from fastapi import FastAPI, HTTPException
import httpx
import json
import os

app = FastAPI(title="LLM Verktøy API", version="1.0.0")

KONSULENT_API_URL = os.getenv("KONSULENT_API_URL", "http://localhost:8000/konsulenter")


@app.get("/")
async def root():
    return {"message": "LLM Verktøy API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)