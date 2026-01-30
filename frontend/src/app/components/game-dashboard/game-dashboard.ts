import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { GameService, GameState } from '../../services/game';
import { StatsPanelComponent } from '../stats-panel/stats-panel';
import { EventCardComponent } from '../event-card/event-card';

@Component({
  selector: 'app-game-dashboard',
  standalone: true,
  imports: [CommonModule, StatsPanelComponent, EventCardComponent],
  templateUrl: './game-dashboard.html',
  styleUrls: ['./game-dashboard.css']
})
export class GameDashboardComponent implements OnInit {
  state: GameState | null = null;

  constructor(private gameService: GameService, private router: Router) {}

  ngOnInit() {
    this.state = this.gameService.currentState;
    if (!this.state) {
      this.router.navigate(['/']);
    }
  }

  handleChoiceMade(choiceId: number) {
    if (!this.state) return;

    this.gameService.makeChoice(this.state.game_id, choiceId).subscribe({
      next: (response) => {
        this.state = response.state;
        this.gameService.setState(this.state);

        if (!this.state.is_alive) {
          this.router.navigate(['/game-over']);
        }
      },
      error: (err) => console.error(err)
    });
  }
}
