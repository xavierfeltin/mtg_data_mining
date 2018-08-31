import { Component, OnInit } from '@angular/core';
import { DeckService } from '../deck.service';
import { CardService } from '../card.service';
import { Card } from '../models/card';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-decks-view',
  template: `
    <ng-container *ngIf="(cards$ | async) && (decks$ | async); else loading">      
      <h2> Decks: </h2>
      <app-select-deck (select)="onSelectDeck($event)" [selectedDeck]="filterDeck"></app-select-deck>
      <app-deck-display [multiverseids]="deckService.getDeckAt(idDeck) | async"></app-deck-display>  
    </ng-container>

    <ng-template #loading>      
      <app-spinner></app-spinner>
    </ng-template>
  `,
  styleUrls: ['./decks-view.component.css']
})
export class DecksViewComponent implements OnInit {  
  filterDeck: string = 'My Deck';  
  idDeck: number = -1;
  cards$: Observable<Card[]>;
  decks$: Observable<number[][]>;

  constructor(private deckService: DeckService,
              private cardService: CardService) { }

  ngOnInit() {
    this.deckService.getDeck().subscribe(deck => {
      const d = deck;
      this.cards$ = this.cardService.loadCards(d.colors.map(color => color.name), d.mode.name);
      this.decks$ = this.deckService.loadDecks();      
    });
  }

  onSelectDeck(selected: string): void{
    this.filterDeck = selected;
    this.idDeck = (selected === 'My Deck') ? -1 : (parseInt(selected.split('-')[1]) - 1);      
  }

  resetCombobox(): void{
    this.filterDeck = 'My Deck';    
  }
}
