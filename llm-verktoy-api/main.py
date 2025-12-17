from fastapi import FastAPI, HTTPException
import httpx
import json
import os

app = FastAPI(title="LLM Verktøy API", version="1.0.0")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
SELECTED_MODEL = "openai/gpt-3.5-turbo"

KONSULENT_API_URL = os.getenv("KONSULENT_API_URL", "http://localhost:8000/konsulenter")


@app.get("/")
async def root():
    return {"message": "LLM Verktøy API is running."}

async def generate_llm_summary(consultants: list, criteria: dict) -> str:
    """
    Generate summary using LLM

    Uses SELECTED_MODEL via OpenRouter API to generate a summary based on consultants and criteria.
    Falls back to a simple summary if LLM fails.
    """
    consultant_data = []
    for c in consultants:
        availability = 100 - c["belastning_prosent"]
        consultant_data.append({
            "navn": c["navn"],
            "ferdigheter": c["ferdigheter"],
            "tilgjengelighet": f"{availability}%"
        })

    prompt = f"""
        Du er en AI-assistent for konsulent-staffing.

        OPPGAVE: Lag et kort, profesjonelt sammendrag av tilgjengelige konsulenter

        KRITERIER: 
        - Minimum tilgjengelighet: {criteria.get('min_availability', 'Ikke spesifisert')}
        - Nødvendige ferdigheter: {criteria.get('required_skill', 'Ikke spesifisert')}

        KONSULENTER FUNNET:
        {json.dumps(consultant_data, ensure_ascii=False, indent=2)}

        INSTRUKSJONER:
        1. Start med antall konsulenter funnet
        2. Nevn søkekriteriene hvis de er spesifisert
        3. List hver konsulent med navn og tilgjengelighet
        4. Skriv på norsk
        5. Hold det kort og profesjonelt
        6. Maksimalt 2-3 setninger

        EKSEMPEL PÅ SVAR: "Fant 2 konsulenter med minst 50% tilgjengelighet og ferdigheten Python. Ola Nordmann (70% tilgjengelig), Kari Nordmann (50%)."
        """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)