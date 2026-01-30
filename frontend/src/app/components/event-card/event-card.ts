import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Event } from '../../services/game';

@Component({
  selector: 'app-event-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './event-card.html',
  styleUrls: ['./event-card.css']
})
export class EventCardComponent {
  @Input() event: Event | undefined;
  @Output() choiceMade = new EventEmitter<number>();

  onChoice(id: number) {
    this.choiceMade.emit(id);
  }
}
