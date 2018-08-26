import { Component, Input, OnChanges } from '@angular/core';
import { Observable } from 'rxjs/index';
import { CardService } from '../card.service';
import { RecommendationService } from '../recommendation.service';
import { Card } from '../models/card';
import { Color } from '../models/color';
import { Mode } from '../models/mode';
import { CardRecommendation } from '../models/card-recommendation';

@Component({
  selector: 'app-recommendation-child-color',
  template: `
    //<div *ngFor="let color of getColors(this.recommendationWithColors$ | async) ">
    <!--<h3>{{mode.name}} - {{formatColor(colors)}}</h3>-->
    <div class="cards-color">
    <app-recommendationview *ngFor="let recommendation of getRecommendations(card, mode, colors) | async"
      [recommendation]="recommendation"
      [card]="getCardOf(recommendation) | async"
      class="cards">
    </app-recommendationview>
    </div>
    <!--</div>-->
    `,
    styleUrls: ['./recommendation-child-color.component.css'],
})
export class RecommendationChildColorComponent {
  @Input() card: Card;
  @Input() mode: Mode;
  @Input() colors: Color[];

  recommendationWithColors$: Observable<{ [key: string]: CardRecommendation[]; }>;
  recommendations$: Observable< CardRecommendation[] >;

  constructor(private cardService: CardService,
              private recommendationService: RecommendationService) { }

  ngOnInit() {}

  getColors(mapColorRecommendation: { [key: string]: CardRecommendation[]; }): string[] {
    return Array.from(Object.keys(mapColorRecommendation));
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }

  getColorsAndRecommendations(card: Card, gameMode: string): Observable<{ [key: string]: CardRecommendation[]; }> {
    return this.recommendationService.getRecommendationsForMode(card, gameMode);
  }

  //getRecommendations(card: Card, gameMode: string, color: string): Observable< CardRecommendation[] > {
  getRecommendations(card: Card, gameMode: Mode, colors: Color[]): Observable< CardRecommendation[] > {
    return this.recommendationService.getRecommendationsForModeAndColor(card, gameMode.name, colors.map(color => color.name.toLowerCase()).join('_'));
  }

  /*
  formatColor(colors: Color[]): string {
    return colors.map(color => color.name).join(' / ');
  }
  */

  ngOnChanges() {
    this.recommendationWithColors$ = this.getColorsAndRecommendations(this.card, this.mode.name);
  }
}
