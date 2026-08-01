from fastapi import FastAPI

from app.api.player import router as player_router
from app.api.team import router as team_router
from app.api.match import router as match_router
from app.api.venue import router as venue_router
from app.api.delivery import router as delivery_router
from app.api.wicket import router as wicket_router
from app.api.match_squad import router as match_squad_router
from app.api.player_of_match import router as player_of_match_router
from app.api.powerplay import router as powerplay_router
from app.api.extras_breakdown import router as extras_breakdown_router

app = FastAPI(
    title="CricketIQ AI",
    version="1.0.0"
)

app.include_router(player_router)
app.include_router(team_router)
app.include_router(match_router)
app.include_router(venue_router)
app.include_router(delivery_router)
app.include_router(wicket_router)
app.include_router(match_squad_router)
app.include_router(player_of_match_router)
app.include_router(powerplay_router)
app.include_router(extras_breakdown_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to CricketIQ AI 🚀"
    }

