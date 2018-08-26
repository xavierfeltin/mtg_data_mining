import { Component, OnInit, Input } from '@angular/core';
import { CardService } from '../card.service';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';
import { Deck } from '../models/deck';
import { Color } from '../models/color';

@Component({
  selector: 'app-cardsindex',
  template: `
    <h2>Available Cards</h2>
    <div>
      <app-select-colors (select)="onSelectColor($event)" [selectedColor]=colors[0] [colors]=colors></app-select-colors>
      <app-select-types (select)="onSelectType($event)" [selectedType]="filterType"></app-select-types>
      <app-input-cards (keyup.enter)="onValidateName($event.target.value)" [defaultValue]="filterName"></app-input-cards>
    </div>
    <app-cardsview [filterColor]="filterColor" [filterType]="filterType" [filterName]="filterName" [authorizedColors]="colorsNames"> </app-cardsview>
    <ng-template #loading>      
      <app-spinner></app-spinner>
    </ng-template>
  `,
  styleUrls: ['./cardsindex.component.css']
})
export class CardsindexComponent implements OnInit {
  deck: Deck;
  colors: Color[];
  colorsNames: string[];
  filterColor: string;
  filterType: string = 'All Types';
  filterName: string = '';

  constructor(private cardService: CardService, 
              private deckService: DeckService,
              private modelService: ModelService,) {}

  ngOnInit() {
    this.deckService.getDeck().subscribe(deck => this.deck = deck);
    this.colors = [...this.deck.colors];
    this.colorsNames = this.colors.map(color => color.name);
    this.filterColor = this.colors[0].name;
    this.cardService.loadCards(this.deck.colors.map(color => color.name), this.deck.mode.name);
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
}