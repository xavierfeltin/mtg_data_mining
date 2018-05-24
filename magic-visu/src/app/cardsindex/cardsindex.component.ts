import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-cardsindex',
  template: `
    <h2>Available Cards</h2>
    <div>
      <app-select-colors (select)="onSelectColor($event)" [selectedColor]="filterColor"></app-select-colors>
      <app-select-types (select)="onSelectType($event)" [selectedType]="filterType"></app-select-types>
      <app-input-cards (keyup.enter)="onValidateName($event.target.value)" [defaultValue]="filterName"></app-input-cards>
    </div>
    <app-cardsview [filterColor]="filterColor" [filterType]="filterType" [filterName]="filterName"> </app-cardsview>
  `,
  styleUrls: ['./cardsindex.component.css']
})
export class CardsindexComponent implements OnInit {
  filterColor: string = 'All Colors';
  filterType: string = 'All Types';
  filterName: string = '';

  constructor() { }

  ngOnInit() {
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
    this.filterColor = 'All Colors';
  }

  resetInputField(): void{
    this.filterName = '';
  }
}