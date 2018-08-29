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

  _lsa: Observable<ModelLSA>;
  _topN: Observable<ModelTopN>;

  constructor(private http: HttpClient) { }

  loadLSAModel(colors: string[], mode: string): Observable<ModelLSA> {
    if (!this._lsa) {
      const filename = 'lsa_' + mode + '_' + colors.join('_');
      this._lsa = this.http.get<ModelLSA>('./assets/' + filename + '.json')
      .pipe(
        publishReplay(),
        refCount(),
      );
    }
    return this._lsa;
  }

  loadTopNModel(colors: string[], mode: string): Observable<ModelTopN> {
    if (!this._topN) {
      const filename = 'topN_' + mode + '_' + colors.join('_');
      this._topN = this.http.get<ModelTopN>('./assets/' + filename + '.json')
      .pipe(
        publishReplay(),
        refCount(),
      );
    }
    return this._topN;
  }

  cleanCache() {
    this._lsa = null;
    this._topN = null;
  }
}
