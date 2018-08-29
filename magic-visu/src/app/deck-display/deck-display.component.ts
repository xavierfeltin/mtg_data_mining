import { Component, OnInit, Input } from '@angular/core';
import { DeckService } from '../deck.service';
import { CardService } from '../card.service';
import { Card } from '../models/card';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-deck-display',
  template: `
    <div>
      <app-select-types (select)="onSelectType($event)" [selectedType]="filterType"></app-select-types>
      <app-input-cards (keyup.enter)="onValidateName($event.target.value)" [defaultValue]="filterName"></app-input-cards>
    </div>
    <app-cardsview [cards]="getCards()|async" [nb]=10> </app-cardsview>
  `,
  styleUrls: ['./deck-display.component.css']
})
export class DeckDisplayComponent implements OnInit {  
  @Input() multiverseids: number [];
  filterType: string = 'All Types';
  filterName: string = '';

  constructor(private cardService: CardService) { }

  ngOnInit() {}

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
  }

  resetInputField(): void{
    this.filterName = '';
  }

  getCards(): Observable<Card[]> {    
    let types = [this.filterType];   
    if (this.filterType === 'All Types') {
      types = []
    }

    return this.cardService.getCardsById(this.multiverseids, [], types, this.filterName, []);
  }
}