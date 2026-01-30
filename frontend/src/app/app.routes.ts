import { Routes } from '@angular/router';
import { CharacterCreationComponent } from './components/character-creation/character-creation';
import { GameDashboardComponent } from './components/game-dashboard/game-dashboard';
import { GameOverComponent } from './components/game-over/game-over';

export const routes: Routes = [
  { path: '', redirectTo: 'create-character', pathMatch: 'full' },
  { path: 'create-character', component: CharacterCreationComponent },
  { path: 'game', component: GameDashboardComponent },
  { path: 'game-over', component: GameOverComponent }
];
