import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { GameService, GameState } from '../../services/game';

@Component({
  selector: 'app-game-over',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-over.html',
  styleUrls: ['./game-over.css']
})
export class GameOverComponent implements OnInit {
  state: GameState | null = null;

  constructor(private gameService: GameService, private router: Router) {}

  ngOnInit() {
    this.state = this.gameService.currentState;
    // If no state, maybe redirect to home, but keep it for now
  }

  restart() {
    this.router.navigate(['/']);
  }
}
