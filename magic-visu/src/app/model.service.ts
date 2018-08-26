import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { map, publishReplay, refCount } from 'rxjs/operators';
import { compareCardsFn, filterColorsTypesNameFn } from './card.utils';
import { Card } from './models/card';
import { ModelLSA, ModelTopN } from './models/model';
import { CardRecommendation } from './models/card-recommendation';
import { COLORS } from './store/store-color';


@Injectable({
  providedIn: 'root'
})
export class ModelService {

  //_lsa: {[key: string]: ModelLSA};
  //_topN: {[key: string]: ModelTopN};

  constructor(private http: HttpClient) { }

  /*
  getContentRecommendations(colors: string[], mode: string, card: Card, nbRecommendations: number): Observable<CardRecommendation[]> {
    const key = this.generate_key(colors,mode);
    return of(this._lsa[key].getRecommendations(card, nbRecommendations));
  }

  getItemRecommendations(colors: string[], mode: string, card: Card, nbRecommendations: number): Observable<CardRecommendation[]> {
    const key = this.generate_key(colors,mode);
    return of(this._topN[key].getRecommendations(card, nbRecommendations));
  }
  */

  loadLSAModel(colors: string[], mode: string): Observable<ModelLSA> {
    const filename = 'lsa_' + mode + '_' + colors.join('_');
    return this.http.get<ModelLSA>('./assets/' + filename + '.json')
    .pipe(
      publishReplay(),
      refCount(),
    );
  }

  loadTopNModel(colors: string[], mode: string): Observable<ModelTopN> {
    const filename = 'topN_' + mode + '_' + colors.join('_');
    return this.http.get<ModelTopN>('./assets/' + filename + '.json')
    .pipe(
      publishReplay(),
      refCount(),
    );
  }

  /*
  private generate_key(colors: string[], mode: string) {
    return mode + '_' + colors.join('_');
  }
  */
}
