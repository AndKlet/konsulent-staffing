# MCP Konsulent Staffing

En Model Context Protocol (MCP) løsning for konsulent-staffing med to mikrotjenester og OpenRouter LLM-integrasjon.

## Arkitektur

- **konsulent-api** (port 8000): Server med hardkodet konsulentdata
- **llm-verktoy-api** (port 8001): Klient som filtrerer data og genererer AI-drevne sammendrag

## Forutsetninger

- Docker og Docker Compose
- OpenRouter API-nøkkel

## Oppsett

1. Klon kodebasen
   ```
   git clone git@github.com:AndKlet/konsulent-staffing.git
   ```
2. Opprett en `.env` fil i rotmappa:
   ```
   OPENROUTER_API_KEY=din_openrouter_api_nokkel_her
   ```
3. Start tjenestene:
   ```bash
   docker compose up --build
   ```

## Bruk

### Hent alle konsulenter
```bash
curl http://localhost:8000/konsulenter
```

### Hent filtrert konsulentsammendrag
```bash
curl "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=60&pakrevd_ferdighet=python"
```

### API-parametere

- `min_tilgjengelighet_prosent`: Minimum tilgjengelighetsprosent (0-100)
- `pakrevd_ferdighet`: Påkrevd ferdighet (case-insensitive)

### Eksempel på respons
```json
{
  "sammendrag": "Fant 3 konsulenter med minst 60% tilgjengelighet og ferdigheten 'python'. Anna K. har 60% tilgjengelighet. Leo T. har 80% tilgjengelighet. Ida N. har 75% tilgjengelighet."
}
```

## API-dokumentasjon

Når tjenestene kjører:
- Konsulent API: http://localhost:8000/docs
- LLM Verktøy API: http://localhost:8001/docs

## Testing

Et testskript er inkludert, men fungerer foreløpig bare på Windows:
```powershell
.\test_mcp_solution.bat
```

## Modellvalg

Løsningen bruker OpenRouter sin gpt-3.5-turbo modell for god balanse mellom kostnad og kvalitet, egnet for tekstsammendrag med norsk språkstøtte.
