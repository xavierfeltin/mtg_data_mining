import { Component, Input, OnChanges } from '@angular/core';
import { Observable } from 'rxjs';
import { CardService } from '../card.service';
import { Card } from '../models/card';

@Component({
  selector: 'app-cardsview',
  template: `
    <app-cardview *ngFor="let card of cards$ | async | paginate: { itemsPerPage: 10, currentPage: p }; let i = index" 
      [card]="card" class="cards">
    </app-cardview>
    <pagination-controls (pageChange)="p = $event"></pagination-controls>
  `,
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnChanges {
  @Input() filterColor: string;
  cards$: Observable<Card[]>;
  p: number = 1; //initializing p to one

  constructor(private cardService: CardService) {
  }
  ngOnChanges() {
    console.log(this.filterColor);
    this.cards$ = this.cardService.getCards([this.filterColor],['Creature']);
  }
}
