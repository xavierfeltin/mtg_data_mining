import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Card } from './models/card';
import { CardRecommendation } from './models/card-recommendation';
import { compareColorsAsKey } from './card.utils'

@Injectable({
  providedIn: 'root',
})
export class RecommendationService {

  getRecommendationsForMode(
    card: Card,
    mode: string
  ): Observable<{ [key: string]: CardRecommendation[]; }> {
    if (mode in card.itemRecommendations){
      const byMode = card.itemRecommendations[mode];
      const byColor: { [key: string]: CardRecommendation[] } = Object.keys(byMode).sort(compareColorsAsKey).reduce(
        (acc, color) => ({ ...acc, [color]: card.itemRecommendations[mode][color] }),
        {},
      );      
      return of(byColor);
    }
    else {
      return of({})
    }
  }

  getRecommendationsForModeAndColor(
    card: Card,
    mode: string,
    color: string
  ): Observable<CardRecommendation[]> {
    return of(card.itemRecommendations[mode][color]);
  }
}
