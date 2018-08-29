import { Component, Input, OnInit } from '@angular/core';
import { Card } from '../models/card';

@Component({
  selector: 'app-cardsview',
  template: `
    <ng-container *ngIf="cards; else loading">
    <app-cardview *ngFor="let card of cards | paginate: { itemsPerPage: nb, currentPage: p }; let i = index" 
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
export class CardsviewComponent implements OnInit {
  @Input() cards: Card[];
  @Input() nb: number = 5;
  p: number = 1; //initializing p to one

  constructor() {}

  ngOnInit() {}
}
