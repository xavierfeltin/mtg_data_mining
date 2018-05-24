import { Component, Input, OnChanges } from '@angular/core';
import { Observable } from 'rxjs';
import { CardService } from '../card.service';
import { Card } from '../models/card';

@Component({
  selector: 'app-cardsview',
  template: `
    <ng-container *ngIf="cards$ | async as cards; else loading">
    <app-cardview *ngFor="let card of cards$ | async | paginate: { itemsPerPage: 12, currentPage: p }; let i = index" 
      [card]="card" class="cards">
    </app-cardview>
    <pagination-controls (pageChange)="p = $event"></pagination-controls>    
    </ng-container>
    <ng-template #loading>      
      <app-spinner></app-spinner>
    </ng-template>
  `,
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnChanges {
  @Input() filterColor: string;
  @Input() filterType: string;
  cards$: Observable<Card[]>;
  p: number = 1; //initializing p to one

  constructor(private cardService: CardService) {
  }

  ngOnChanges() {
    this.cards$ = this.cardService.getCards([this.filterColor],[this.filterType]);
  }
}
