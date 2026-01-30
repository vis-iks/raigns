from abc import ABC, abstractmethod
from typing import Tuple, Dict, List
import random
import os
import json
from openai import OpenAI
from .models import GameState, Event, Choice

class LLMService(ABC):
    @abstractmethod
    def generate_event(self, state: GameState) -> Tuple[Event, Dict[int, Dict[str, int]]]:
        """
        Generates a new event based on the current game state.
        Returns the Event object and a map of choice_id -> effects.
        """
        pass

class MockLLMService(LLMService):
    def generate_event(self, state: GameState) -> Tuple[Event, Dict[int, Dict[str, int]]]:
        # Simple Mock LLM logic
        templates = [
            {
                "text": "A neighboring kingdom requests an alliance against the northern barbarians.",
                "choices": [
                    {"text": "Accept alliance.", "effects": {"military": 10, "wealth": -5, "territory": 5}},
                    {"text": "Decline politely.", "effects": {"military": -5, "stability": 5}},
                    {"text": "Execute the messenger.", "effects": {"military": 5, "popularity": -10, "stability": -10, "territory": 2}}
                ]
            },
            {
                "text": "A mysterious plague is spreading in the capital.",
                "choices": [
                    {"text": "Quarantine the city.", "effects": {"popularity": -10, "stability": 10, "wealth": -5}},
                    {"text": "Pray to the gods.", "effects": {"popularity": 5, "wealth": -2, "stability": -5}},
                    {"text": "Ignore it.", "effects": {"popularity": -20, "stability": -20, "wealth": 10}}
                ]
            },
            {
                "text": "The treasury is running low, but the peasants are starving.",
                "choices": [
                    {"text": "Raise taxes.", "effects": {"wealth": 15, "popularity": -15, "stability": -5}},
                    {"text": "Open the granaries.", "effects": {"wealth": -10, "popularity": 15, "stability": 5}},
                ]
            },
            {
                "text": "A new gold mine was discovered near the border.",
                "choices": [
                    {"text": "Seize it for the crown.", "effects": {"wealth": 20, "popularity": -5}},
                    {"text": "Share profits with locals.", "effects": {"wealth": 5, "popularity": 10, "stability": 5}},
                ]
            }
        ]

        template = random.choice(templates)
        description = template["text"]

        # Simple flavor text modifications
        if "mad" in state.character.traits:
            description = "The voices whisper... " + description
        if "Dictator" == state.character.ruler_type:
            description = "My Leader! " + description

        choices_list = []
        effects_map = {}

        for i, choice_data in enumerate(template["choices"]):
            text = choice_data["text"]
            if "sneaky" in state.character.traits and i == 1:
                text = "(Sneaky) " + text

            choices_list.append(Choice(id=i, text=text))
            effects_map[i] = choice_data["effects"]

        return Event(description=description, choices=choices_list), effects_map

class DeepSeekLLMService(LLMService):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def generate_event(self, state: GameState) -> Tuple[Event, Dict[int, Dict[str, int]]]:
        prompt = self._build_prompt(state)

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=1.2 # High creativity
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            return self._parse_response(data)

        except Exception as e:
            print(f"DeepSeek API Error: {e}. Falling back to Mock.")
            return MockLLMService().generate_event(state)

    def _get_system_prompt(self):
        return """
        You are the Game Master for a strategy game like 'Reigns'.
        You must generate a scenario based on the Ruler's type, traits, and current kingdom status.

        Output strictly in JSON format:
        {
            "event_text": "Description of the event...",
            "choices": [
                {
                    "text": "Choice description",
                    "effects": {
                        "popularity": integer (-20 to 20),
                        "wealth": integer (-20 to 20),
                        "military": integer (-20 to 20),
                        "stability": integer (-20 to 20),
                        "territory": integer (-10 to 10)
                    }
                },
                ... (2 or 3 choices)
            ]
        }

        The 'effects' are hidden from the player but modify their stats.
        Be creative, funny, dark, or weird based on the Ruler's traits.
        """

    def _build_prompt(self, state: GameState) -> str:
        pillars = state.pillars
        return f"""
        Ruler: {state.character.name}
        Type: {state.character.ruler_type}
        Traits: {', '.join(state.character.traits)}

        Current Status:
        - Popularity: {pillars.popularity}
        - Wealth: {pillars.wealth}
        - Military: {pillars.military}
        - Stability: {pillars.stability}
        - Territory: {pillars.territory}

        Turn: {state.turn_count}
        Previous Event: {state.current_event.description if state.current_event else "None"}

        Generate the next event.
        """

    def _parse_response(self, data: Dict) -> Tuple[Event, Dict[int, Dict[str, int]]]:
        choices_list = []
        effects_map = {}

        for i, choice_data in enumerate(data.get("choices", [])):
            choices_list.append(Choice(id=i, text=choice_data["text"]))
            effects_map[i] = choice_data.get("effects", {})

        event = Event(
            description=data.get("event_text", "Something happens..."),
            choices=choices_list
        )

        return event, effects_map
