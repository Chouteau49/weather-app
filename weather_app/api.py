from fastapi import FastAPI, HTTPException, APIRouter
from weather_app.weather import get_weather

app = FastAPI(title="Weather API", version="1.0.0")
api_router = APIRouter(prefix="/api")

@api_router.get("/weather/{city}")
async def read_weather(city: str):
    """Récupère la météo pour une ville."""
    weather = get_weather(city)
    if weather:
        return {"city": city, "temperature": weather["temp"], "description": weather["description"]}
    raise HTTPException(status_code=404, detail="Météo non trouvée")

app.include_router(api_router)