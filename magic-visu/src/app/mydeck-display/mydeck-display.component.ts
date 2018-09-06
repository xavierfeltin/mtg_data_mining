import { Component, OnInit, Input, TestabilityRegistry } from '@angular/core';
import { Card } from '../models/card';
import { DeckService } from '../deck.service';

@Component({
  selector: 'app-mydeck-display',
  template: `
    <app-deck-stats [cards]="deckService.getAllCards() | async" *ngIf="(deckService.getActiveCards() | async).length > 0"></app-deck-stats>
    <app-deck-display [multiverseids]="deckService.getDeckAt(idDeck) | async"></app-deck-display>
  `,
  styleUrls: ['./mydeck-display.component.css']
})
export class MydeckDisplayComponent implements OnInit {
  idDeck: number = -1;
  constructor(private deckService: DeckService) { }

  ngOnInit() {}
}
