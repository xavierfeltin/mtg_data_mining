import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, ConnectableObservable} from 'rxjs';
import { map, publishReplay, refCount, filter, switchMap } from 'rxjs/operators';
import { Card } from './models/card';
import { CardRecommendation } from './models/card-recommendation';

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {

  _recommendations: Observable<CardRecommendation[]>;

  constructor() { }

  getRecommendationsForMode(card: Card, mode: string): Observable<{[key: string]: CardRecommendation[];}> {
    return of<{[key: string]: CardRecommendation[];}>(card.itemRecommendations[mode])
    .pipe( 
        map(nested_colors => Object.keys(nested_colors).sort(this.fn)),  
        switchMap(color => card.itemRecommendations[mode][color])
    );
  }

  fn(a:any, b:any): number {
      console.log(a);
      if (a < b){ return -1;}
      else if (a > b) {return 1;}
      return 0;
  }
}