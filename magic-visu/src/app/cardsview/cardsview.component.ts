import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Card } from '../models/card';
import { CardService } from '../card.service';

@Component({
  selector: 'app-cardsview',
  template: `
    <h2>Available Cards</h2>
      <app-cardview *ngFor="let card of cards$ | async | paginate: { itemsPerPage: 10, currentPage: p }; let i = index" 
        [card]="card" class="cards">
      </app-cardview>
      <pagination-controls (pageChange)="p = $event"></pagination-controls>
  `,
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnInit {
  cards$: Observable<Card[]>;
  p: number = 1; //initializing p to one
  
  constructor(private cardService: CardService) { 
    this.cards$ = this.cardService.getCards();
  }

  ngOnInit() {
    
  }
}