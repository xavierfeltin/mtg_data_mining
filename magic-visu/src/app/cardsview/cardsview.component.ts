import { Component, Input, OnChanges } from '@angular/core';
import { Observable } from 'rxjs';
import { CardService } from '../card.service';
import { Card } from '../models/card';

@Component({
  selector: 'app-cardsview',
  template: `
    <ng-container *ngIf="cards$ | async as cards; else loading">
    <app-cardview *ngFor="let card of cards$ | async | paginate: { itemsPerPage: 5, currentPage: p }; let i = index" 
      [card]="card" class="cards">
    </app-cardview>
    <pagination-controls (pageChange)="p = $event"></pagination-controls>    
    </ng-container>
  `,
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnChanges {
  @Input() filterColor: string;
  @Input() authorizedColors: string[];
  @Input() filterType: string;
  @Input() filterName: string;
  cards$: Observable<Card[]>;
  p: number = 1; //initializing p to one

  constructor(private cardService: CardService) {
  }

  ngOnChanges() {    
    let colors = [this.filterColor];   
    let secondaryColors = this.authorizedColors.filter(color => color !== this.filterColor);
    
    if (this.filterColor === 'All Colors') {
      colors = [];
      secondaryColors = [];
    }

    let types = [this.filterType];   
    if (this.filterType === 'All Types') {
      types = []
    }
    
    this.cards$ = this.cardService.getCards(colors, types, this.filterName, secondaryColors);
  }
}
