import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',
  template: `
    <div draggable [dragData]="card">
    <div class="score"> {{title}} </div>
    <a routerLink="/recommendation/{{recommendation.multiverseid}}">
      <img [src]="cardUrl" [alt]="card?.name" [title]="card?.name"/>
    </a>
    </div>
    `,
  styleUrls: ['./recommendationview.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent {
  @Input() card: Card;
  @Input() recommendation: CardRecommendation;

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.multiverseid}`;
  }

  get title() {
    return `Content: ${this.recommendation.score.toFixed(3)}`
  }
}