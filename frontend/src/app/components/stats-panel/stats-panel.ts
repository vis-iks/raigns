import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Pillars } from '../../services/game';

@Component({
  selector: 'app-stats-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-panel.html',
  styleUrls: ['./stats-panel.css']
})
export class StatsPanelComponent {
  @Input() pillars!: Pillars;
}
