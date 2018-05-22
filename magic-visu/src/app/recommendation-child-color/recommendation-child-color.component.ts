import { Component, Input } from '@angular/core';
import { Observable } from 'rxjs/index';
import { CardService } from '../card.service';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

@Component({
  selector: 'app-recommendation-child-color',
  //templateUrl: './recommendation-child-color.component.html',
  template: `
    <div *ngFor="let color of this.getColors()">
      <h3>{{this.gameMode}} - {{formatColor(color)}}</h3>
      <app-recommendationview *ngFor="let recommendation of this.card.itemRecommendations[this.gameMode][color]"
        [recommendation]="recommendation"
        [card]="getCardOf(recommendation) | async"
        class="cards"
      ></app-recommendationview>
    </div>`,
  styleUrls: ['./recommendation-child-color.component.css'],
})
export class RecommendationChildColorComponent {
  @Input() card: Card;
  @Input() gameMode: string;

  constructor(private cardService: CardService) { }

  getColors(): string[] {
    return Object.keys(this.card.itemRecommendations[this.gameMode]);
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }

  formatColor(colorToFormat: string): string {
    let colors: string[] = colorToFormat.split('_');
    let formattedColor: string = '';
    colors.forEach((color, index) => {
      formattedColor += color.charAt(0).toUpperCase() + color.slice(1);
      if (index != (colors.length - 1)) {formattedColor += ' / '; }
    });

    return formattedColor;
  }
}
