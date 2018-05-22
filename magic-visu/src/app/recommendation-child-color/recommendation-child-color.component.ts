import { Component, Input } from '@angular/core';
import { Observable } from 'rxjs/index';
import { CardService } from '../card.service';
import { RecommendationService } from '../recommendation.service';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

@Component({
  selector: 'app-recommendation-child-color',
  template: `
    <div *ngFor="let color of getColors(this.recommendationWithColors$ | async) ">
      <h3>{{formatColor(color)}}</h3>
      <app-recommendationview *ngFor="let recommendation of getRecommendations(card, gameMode, color) | async"
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

  recommendationWithColors$: Observable<{ [key: string]: CardRecommendation[]; }>;
  recommendations$: Observable< CardRecommendation[] >;

  constructor(private cardService: CardService,
              private recommendationService: RecommendationService) { }

  ngOnInit() {
    this.recommendationWithColors$ = this.getColorsAndRecommendations(this.card, this.gameMode);        
  }

  getColors(mapColorRecommendation: { [key: string]: CardRecommendation[]; }): string[] {
    return Array.from(Object.keys(mapColorRecommendation));
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }

  getColorsAndRecommendations(card: Card, gameMode: string): Observable<{ [key: string]: CardRecommendation[]; }> {
    return this.recommendationService.getRecommendationsForMode(card, gameMode);
  }

  getRecommendations(card: Card, gameMode: string, color: string): Observable< CardRecommendation[] > {
    return this.recommendationService.getRecommendationsForModeAndColor(card, gameMode, color);
  }

  formatColor(colorToFormat: string): string {
    let colors: string[] = colorToFormat.split('_').sort();
    let formattedColor: string = '';
    colors.forEach((color, index) => {
      formattedColor += color.charAt(0).toUpperCase() + color.slice(1);
      if (index != (colors.length - 1)) {formattedColor += ' / '; }
    });

    return formattedColor;
  }
}
