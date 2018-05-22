import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-cardsindex',
  template: `
    <h2>Available Cards</h2>
    <div>
      <app-select-colors (select)="onSelect($event)"></app-select-colors>
    </div>
    <app-cardsview [filterColor]="filterColor"> </app-cardsview>
  `,
  styleUrls: ['./cardsindex.component.css']
})
export class CardsindexComponent implements OnInit {
  filterColor: string = 'blue';

  constructor() { }

  ngOnInit() {
  }

  onSelect(selected: string): void{
    this.filterColor = selected;
  }
}
