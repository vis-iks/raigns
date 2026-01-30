from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .models import Character, GameState
from .game_logic import game_engine

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChoiceRequest(BaseModel):
    game_id: str
    choice_id: int

@app.post("/api/start", response_model=GameState)
def start_game(character: Character):
    return game_engine.start_game(character)

@app.post("/api/choice")
def make_choice(request: ChoiceRequest):
    try:
        state, effects, message = game_engine.make_choice(request.game_id, request.choice_id)
        return {
            "state": state,
            "effects_applied": effects,
            "message": message
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Reigns LLM API is running"}
