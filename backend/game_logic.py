import random
import uuid
import os
from typing import Dict, List, Tuple
from .models import GameState, Character, Pillars, Event, Choice
from .llm_service import LLMService, MockLLMService, DeepSeekLLMService

class InternalChoice:
    def __init__(self, text: str, effects: Dict[str, int]):
        self.text = text
        self.effects = effects

class GameEngine:
    def __init__(self):
        self.games: Dict[str, Dict] = {} # game_id -> {state: GameState, current_choices_effects: {id: effects}}

        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            print("Initializing DeepSeek LLM Service")
            self.llm: LLMService = DeepSeekLLMService(api_key)
        else:
            print("Initializing Mock LLM Service")
            self.llm: LLMService = MockLLMService()

    def start_game(self, character: Character) -> GameState:
        game_id = str(uuid.uuid4())
        initial_pillars = Pillars()
        state = GameState(
            game_id=game_id,
            character=character,
            pillars=initial_pillars
        )

        # Generate first event
        event, effects_map = self._generate_event(state)
        state.current_event = event

        self.games[game_id] = {
            "state": state,
            "choices_effects": effects_map
        }
        return state

    def make_choice(self, game_id: str, choice_id: int) -> Tuple[GameState, Dict[str, int], str]:
        if game_id not in self.games:
            raise ValueError("Game not found")

        game_data = self.games[game_id]
        state = game_data["state"]
        effects_map = game_data["choices_effects"]

        if choice_id not in effects_map:
             raise ValueError("Invalid choice")

        # Apply effects
        effects = effects_map[choice_id]
        state.pillars.popularity += effects.get("popularity", 0)
        state.pillars.wealth += effects.get("wealth", 0)
        state.pillars.military += effects.get("military", 0)
        state.pillars.stability += effects.get("stability", 0)
        state.pillars.territory += effects.get("territory", 0)

        # Clamp values between 0 and 100 (except territory maybe?)
        for field in ["popularity", "wealth", "military", "stability"]:
            val = getattr(state.pillars, field)
            setattr(state.pillars, field, max(0, min(100, val)))

        # Check Win/Loss
        death_reason = self._check_game_over(state)
        if death_reason:
            state.is_alive = False
            state.death_reason = death_reason
            state.current_event = None
            return state, effects, "Game Over"

        state.turn_count += 1

        # Generate next event
        event, new_effects_map = self._generate_event(state)
        state.current_event = event
        game_data["choices_effects"] = new_effects_map

        return state, effects, "Next turn"

    def _check_game_over(self, state: GameState) -> str:
        p = state.pillars
        if p.popularity <= 0: return "The people revolted and overthrew you."
        if p.wealth <= 0: return " The kingdom is bankrupt. You are exiled."
        if p.military <= 0: return "The army staged a coup."
        if p.stability <= 0: return "Anarchy reigns. You were assassinated."
        if p.territory >= 100: return "VICTORY: You have conquered the world!"
        if p.territory <= 0: return "You have lost all your lands."
        return None

    def _generate_event(self, state: GameState) -> Tuple[Event, Dict[int, Dict[str, int]]]:
        return self.llm.generate_event(state)

game_engine = GameEngine()
