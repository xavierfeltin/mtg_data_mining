import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-cardsindex',
  template: `
    <h2>Available Cards</h2>
    <div> <app-select-colors (change)="onSelect($event.target.value)"></app-select-colors> </div>
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
