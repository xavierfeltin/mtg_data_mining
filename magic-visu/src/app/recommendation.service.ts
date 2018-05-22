import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Card } from './models/card';
import { CardRecommendation } from './models/card-recommendation';

@Injectable({
  providedIn: 'root',
})
export class RecommendationService {

  getRecommendationsForMode(
    card: Card,
    mode: string,
  ): Observable<{ [key: string]: CardRecommendation[]; }> {
    const byMode = card.itemRecommendations[mode];
    const byColor: { [key: string]: CardRecommendation[] } = Object.keys(byMode).sort().reduce(
      (acc, color) => ({ ...acc, [color]: card.itemRecommendations[mode][color] }),
      {},
    );

    return of(byColor);
  }
}
