import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { GameService, Character } from '../../services/game';

@Component({
  selector: 'app-character-creation',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './character-creation.html',
  styleUrls: ['./character-creation.css']
})
export class CharacterCreationComponent {
  name: string = '';
  selectedRulerType: string = 'King';
  rulerTypes: string[] = ['King', 'President', 'Dictator'];

  availableTraits: string[] = ['mad', 'crazy', 'intelligent', 'sneaky'];
  selectedTraits: { [key: string]: boolean } = {};

  isLoading = false;

  constructor(private gameService: GameService, private router: Router) {
    this.availableTraits.forEach(t => this.selectedTraits[t] = false);
  }

  startGame() {
    if (!this.name) {
      alert('Please enter a name');
      return;
    }

    const traits = Object.keys(this.selectedTraits).filter(t => this.selectedTraits[t]);

    const character: Character = {
      name: this.name,
      ruler_type: this.selectedRulerType,
      traits: traits
    };

    this.isLoading = true;
    this.gameService.startGame(character).subscribe({
      next: (state) => {
        this.gameService.setState(state);
        this.router.navigate(['/game']);
      },
      error: (err) => {
        console.error(err);
        this.isLoading = false;
        alert('Failed to start game');
      }
    });
  }
}
