from fastapi import FastAPI
import json
import os

app = FastAPI(title="Konsulent API", version="1.0.0")


def load_data():
    """Loads consultant data from a JSON file"""
    data_path = os.path.join(os.getcwd(), "data.json")
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["konsulenter"]
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


KONSULENTER = load_data()


@app.get("/konsulenter")
async def get_konsulenter():
    """Endpoint to retrieve the list of consultants."""
    return KONSULENTER


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
