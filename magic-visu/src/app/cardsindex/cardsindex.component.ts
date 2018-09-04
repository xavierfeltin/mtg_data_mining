import { Component, OnInit } from '@angular/core';
import { CardService } from '../card.service';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';
import { Deck } from '../models/deck';
import { Card } from '../models/card';
import { Color } from '../models/color';
import { Observable } from 'rxjs';
import { ModelTopN } from '../models/Model';

@Component({
  selector: 'app-cardsindex',
  template: `
    <ng-container *ngIf="(cards$ | async) && (modelTopN$ | async) && (decks$ | async); else loading">      
      <h2>Available Cards</h2>
      <div>
        <app-select-colors (select)="onSelectColor($event)" [selectedColor]=colors[0] [colors]=colors></app-select-colors>
        <app-select-types (select)="onSelectType($event)" [selectedType]="filterType"></app-select-types>
        <app-input-cards (keyup.enter)="onValidateName($event.target.value)" [defaultValue]="filterName"></app-input-cards>
      </div>
      <app-cardsview [cards]="getCards()|async" [nb]=10> </app-cardsview>
    </ng-container>

    <ng-template #loading>      
      <app-spinner></app-spinner>
    </ng-template>
  `,
  styleUrls: ['./cardsindex.component.css']
})
export class CardsindexComponent implements OnInit {
  deck: Deck;
  modelTopN$: Observable<ModelTopN>;
  cards$: Observable<Card[]>;
  decks$: Observable<number[][]>;
  colors: Color[];
  colorsNames: string[];
  filterColor: string;
  filterType: string = 'All Types';
  filterName: string = '';  

  constructor(private cardService: CardService, 
              private deckService: DeckService,
              private modelService: ModelService,) {}

  ngOnInit() {
    this.deckService.getDeck().subscribe(deck => {
      this.deck = deck;
      this.modelTopN$ = this.modelService.loadTopNModel(this.deck.colors.map(color => color.name), this.deck.mode.name);
      this.colors = [...this.deck.colors];
      this.colorsNames = this.colors.map(color => color.name);
      this.filterColor = this.colors.length == 0 ? '' : this.colors[0].name;      
      this.cards$ = this.cardService.loadCards(this.deck.colors.map(color => color.name), this.deck.mode.name);
      this.decks$ = this.deckService.loadDecks();
    });        
  }

  onSelectColor(selected: string): void{
    this.filterColor = selected;    
    this.resetInputField();
  }

  onSelectType(selected: string): void{
    this.filterType = selected;
    this.resetInputField();
  }

  onValidateName(value: string): void{
    this.resetCombobox();
    this.filterName = value;    
  }

  resetCombobox(): void{
    this.filterType = 'All Types';
    this.filterColor = this.colors[0].name;
  }

  resetInputField(): void{
    this.filterName = '';
  }

  getCards(): Observable<Card[]> {    
    let colors = [this.filterColor];   
    let secondaryColors = this.colorsNames.filter(color => color !== this.filterColor);
    
    if (this.filterColor === 'All Colors') {
      colors = [];
      secondaryColors = [];
    }

    let types = [this.filterType];   
    if (this.filterType === 'All Types') {
      types = []
    }
    
    return this.cardService.getCards(colors, types, this.filterName, secondaryColors);
  }
}