import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',  
  template: `
    <a routerLink="/recommendation/{{recommendation.card.multiverseid}}" *ngIf="recommendation.item_similarity == null; else showItemRecommendation">      
        <img [src]="cardUrl" [alt]="recommendation.card.name" title="Content score: {{recommendation.content_similarity}}">
        <ng-template #elseBlock> 
          <img [src]="cardUrl" [alt]="recommendation.card.name" title="Item score: {{recommendation.item_similarity}}\nContent score: {{recommendation.content_similarity}}"> 
        </ng-template>        
    </a>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent implements OnInit {
  @Input() recommendation: CardRecommendation;
  
  constructor() { }

  ngOnInit() {
  }

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.card.multiverseid}`;
  } 
}
