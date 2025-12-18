from fastapi import FastAPI, HTTPException
import httpx
import json
import os
from typing import Optional


app = FastAPI(title="LLM Verktøy API", version="1.0.0")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
SELECTED_MODEL = "openai/gpt-3.5-turbo"
KONSULENT_API_URL = "http://konsulent-api:8000"

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

    prompt = f"""Du er en AI-assistent for konsulent-staffing.

    OPPGAVE: Lag et kort, profesjonelt sammendrag av tilgjengelige konsulenter

    KRITERIER: 
    - Minimum tilgjengelighet: {criteria.get('min_availability', 'Ikke spesifisert')}%
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
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": SELECTED_MODEL,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 200,
                    "temperature": 0.3
                }
            )
            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"OpenRouter error: {e}")
        return generate_simple_summary(consultants, criteria)
    

def generate_simple_summary(consultants: list, criteria: dict = None) -> str:
    """Generate a simple summary without LLM as a fallback."""
    if not consultants:
        return "Fant ingen konsulenter som matcher kriteriene."
    
    if criteria and (criteria.get('min_availability') or criteria.get('required_skill')):
        details = []
        if criteria.get('min_availability'):
            details.append(f"minst {criteria['min_availability']}% tilgjengelighet")
        if criteria.get('required_skill'):
            details.append(f"ferdigheten '{criteria['required_skill']}'")
        
        criteria_text = " og ".join(details)
        consultant_names = ", ".join([c["navn"] for c in consultants])
        return f"Fant {len(consultants)} konsulent{'er' if len(consultants) > 1 else ''} med {criteria_text}. Navn: {consultant_names}."
    
    return f"Fant {len(consultants)} konsulenter."


@app.get("/tilgjengelige-konsulenter/sammendrag")
async def get_available_consultants_summary(
    min_tilgjengelighet_prosent: Optional[int] = None,
    påkrevd_ferdighet: Optional[str] = None
):
    """Endpoint to get a summary of available consultants based on criteria"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{KONSULENT_API_URL}/konsulenter")
            response.raise_for_status()
            consultants = response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Konsulent API ikke tilgjengelig: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feil ved henting av data: {str(e)}")

    filtered = consultants

    if min_tilgjengelighet_prosent is not None and min_tilgjengelighet_prosent > 0:
        filtered = [k for k in filtered if (100 - k["belastning_prosent"]) >= min_tilgjengelighet_prosent]
    
    if påkrevd_ferdighet is not None and påkrevd_ferdighet != "":
        påkrevd_lower = påkrevd_ferdighet.lower()
        filtered = [k for k in filtered if any(påkrevd_lower == skill.lower() for skill in k["ferdigheter"])]

    criteria = {
        "min_availability": min_tilgjengelighet_prosent,
        "required_skill": påkrevd_ferdighet
    }

    summary = await generate_llm_summary(filtered, criteria)

    return {"sammendrag": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)