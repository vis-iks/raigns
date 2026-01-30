import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Character {
  name: string;
  ruler_type: string;
  traits: string[];
}

export interface Pillars {
  popularity: number;
  wealth: number;
  military: number;
  stability: number;
  territory: number;
}

export interface Choice {
  id: number;
  text: string;
}

export interface Event {
  description: string;
  choices: Choice[];
}

export interface GameState {
  game_id: string;
  character: Character;
  pillars: Pillars;
  turn_count: number;
  is_alive: boolean;
  death_reason?: string;
  current_event?: Event;
}

export interface ChoiceResponse {
  state: GameState;
  effects_applied: any;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://localhost:8000/api';

  currentState: GameState | null = null;

  constructor(private http: HttpClient) { }

  startGame(character: Character): Observable<GameState> {
    return this.http.post<GameState>(`${this.apiUrl}/start`, character);
  }

  makeChoice(gameId: string, choiceId: number): Observable<ChoiceResponse> {
    return this.http.post<ChoiceResponse>(`${this.apiUrl}/choice`, { game_id: gameId, choice_id: choiceId });
  }

  setState(state: GameState) {
    this.currentState = state;
  }
}
