import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, publishReplay, refCount } from 'rxjs/operators';
import { compareCardsFn, filterColorsTypesNameFn } from './card.utils';
import { Card } from './models/card';

@Injectable({
  providedIn: 'root'
})
export class CardService {

  _cards: Observable<Card[]>;

  constructor(private http: HttpClient) { }

  loadCards(colors: string[], mode: string): Observable<Card[]> {
    if (!this._cards) {
      const filename = 'catalog_' + mode + '_' + colors.join('_');
      this._cards = this.http.get<Card[]>('./assets/' + filename + '.json')
      .pipe(
        map(cards => cards.sort(compareCardsFn)),
        publishReplay(),
        refCount(),
      );
    }
    return this._cards;
  }

  cleanCache() {
    this._cards = null;
  }

  getCards(filterColors: string[] = [], filterTypes: string[] = [], filterName: string = '', filterSecondaryColors: string[] = []): Observable<Card[]> {
    //return of(CARDS);
    //return this.http.get<Card[]>('/assets/db_similarities_small.json');

    /* Cache is created now when the deck is created.
    if (!this._cards) {
      this._cards = this.http.get<Card[]>('./assets/db_similarities_small.json')
      .pipe(
        map(cards => cards.sort(compareCardsFn)),
        publishReplay(),
        refCount(),
      );
    }
    */
    return this._cards.pipe(
      map(cards => cards.filter(card => filterColorsTypesNameFn(card, filterColors, filterTypes, filterName, filterSecondaryColors))),
    );
  }

  getCard(id: number): Observable<Card> {
    //return of(CARDS.find(card => card.multiverseid === id));
    return this.getCards().pipe(map(cards => cards.filter(card => card.multiverseid === id).pop()));
  }
}
