from pydantic import BaseModel
from typing import List, Dict, Optional

class Character(BaseModel):
    name: str
    ruler_type: str  # King, President, Dictator
    traits: List[str]  # mad, crazy, intelligent, sneaky

class Pillars(BaseModel):
    popularity: int = 50
    wealth: int = 50
    military: int = 50
    stability: int = 50
    territory: int = 10

class Choice(BaseModel):
    id: int
    text: str

class Event(BaseModel):
    description: str
    choices: List[Choice]

class GameState(BaseModel):
    game_id: str
    character: Character
    pillars: Pillars
    turn_count: int = 0
    is_alive: bool = True
    death_reason: Optional[str] = None
    current_event: Optional[Event] = None
