import { Component, OnInit } from '@angular/core';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';
import { Deck } from '../models/deck';
import { Observable } from 'rxjs';
import { ModelTopN } from '../models/Model';

@Component({
  selector: 'app-deck-recommendations',
  template: `
    <ng-container *ngIf="(modelTopN$ | async) && (decks$ | async); else loading">      
      <h2>Deck Recommendations:</h2>
      <p class="information">Recommendations are based on the cards present in your deck (<a href="https://github.com/xavierfeltin/mtg_data_mining/wiki/Deck-recommendations" target="_blank">more information</a>)
      <br/> A higher score means the card is played more often with the cards in your deck
      <br/> The details of the contribution of your deck on the recommendations are displayed in the cards tooltip 
      </p>
      <app-recommendation-list [model]="modelTopN$ | async" [cards]="deckService.getCards() | async" [nbRecommendations]="10" [modelType]="'TOPN'"></app-recommendation-list>      
    </ng-container>

    <ng-template #loading>      
      <app-spinner></app-spinner>
    </ng-template>
  `,
  styleUrls: ['./deck-recommendations.component.css']
})
export class DeckRecommendationsComponent implements OnInit {

  deck: Deck;
  modelTopN$: Observable<ModelTopN>;
  decks$: Observable<number[][]>;

  constructor(private deckService: DeckService,
              private modelService: ModelService,) {}

  ngOnInit() {
    this.deckService.getDeck().subscribe(deck => {
      this.deck = deck;
      this.modelTopN$ = this.modelService.loadTopNModel(this.deck.colors.map(color => color.name), this.deck.mode.name);
      this.decks$ = this.deckService.loadDecks();
    });        
  }
}
