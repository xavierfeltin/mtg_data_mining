import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-cardsindex',
  template: `
    <h2>Available Cards</h2>
    <div>
      <app-select-colors (select)="onSelectColor($event)" [selectedColor]="filterColor"></app-select-colors>
      <app-select-types (select)="onSelectType($event)" [selectedType]="filterType"></app-select-types>
    </div>
    <app-cardsview [filterColor]="filterColor" [filterType]="filterType"> </app-cardsview>
  `,
  styleUrls: ['./cardsindex.component.css']
})
export class CardsindexComponent implements OnInit {
  filterColor: string = 'blue';
  filterType: string = 'Creature';

  constructor() { }

  ngOnInit() {
  }

  onSelectColor(selected: string): void{
    this.filterColor = selected;
  }

  onSelectType(selected: string): void{
    this.filterType = selected;
  }
}