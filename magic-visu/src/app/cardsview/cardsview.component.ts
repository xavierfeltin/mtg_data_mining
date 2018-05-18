import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Card } from '../models/card';
import { CardService } from '../card.service';

@Component({
  selector: 'app-cardsview',
  template: `
    <h2>Available Cards</h2>
      <app-cardview *ngFor="let card of cards$ | async" 
        [card]="card">
      </app-cardview>
  `,
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnInit {
  cards$: Observable<Card[]>;

  constructor(private cardService: CardService) { 
    this.cards$ = this.cardService.getCards();
  }

  ngOnInit() {}
}