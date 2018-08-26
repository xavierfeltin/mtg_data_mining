import { Component, OnInit, Input } from '@angular/core';
import { Deck } from '../models/deck';
import { DeckService } from '../deck.service';

@Component({
  selector: 'app-deck-attributes',
  template: `
    <p> Mode: {{deck.mode.name}} </p>
    <p> Colors: </p>
    <ul>
    <li *ngFor="let color of deck.colors;">
      {{color.name}}
    </li>
    </ul>    
    <p> Cards: </p>    
    <div droppable class="card card-outline-primary mb-3" [dragOverClass]="'drag-target-border'" [dragHintClass]="'drag-hint'" (onDrop)="onItemDrop($event)">
      <ul>
        <div class="hlayout" *ngFor="let card of deck.cards; let i = index">
          <li>
            <a routerLink="/recommendation/{{card.multiverseid}}"> {{card.name}} </a>
          </li>
          <button class="nav-button" (click)="onRemoveCard($event, card)"> X </button>
        </div>
      </ul>
    </div>
  `,
  styleUrls: ['./deck-attributes.component.css']
})
export class DeckAttributesComponent implements OnInit {
  @Input() deck: Deck;

  constructor(private deckService: DeckService) { }

  ngOnInit() {
  }

  onRemoveCard(event, card) {
    this.deckService.removeCard(card);
  }

  onItemDrop(event) {
    this.deckService.addCard(event.dragData);
  }
}
