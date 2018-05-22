import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',
  template: `
    <a routerLink="/recommendation/{{recommendation.multiverseid}}">
      <img [src]="cardUrl" [alt]="card?.name" [title]="title"/>
    </a>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent {
  @Input() card: Card;
  @Input() recommendation: CardRecommendation;

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.multiverseid}`;
  }

  get title() {
    return this.recommendation.itemSimilarity === null ?
      `Content score: ${this.recommendation.contentSimilarity}`
      :`Item score: ${this.recommendation.itemSimilarity}\nContent score: ${this.recommendation.contentSimilarity}`;
  }
}
