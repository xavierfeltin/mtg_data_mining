import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, ConnectableObservable} from 'rxjs';
import { map, publishReplay, refCount } from 'rxjs/operators';
import { Card } from './models/card'
import { CARDS } from './mock-cards'

@Injectable({
  providedIn: 'root'
})
export class CardService {

  _cards: Observable<Card[]>;

  constructor(private http: HttpClient) { }

  getCards(): Observable<Card[]> {
    //return of(CARDS);
    //return this.http.get<Card[]>('/assets/db_similarities_small.json');
    if (!this._cards) { 
      this._cards = this.http.get<Card[]>('/assets/db_similarities_small.json')
      .pipe(
        publishReplay(),
        refCount()
      );
    } 
    return this._cards;
  }

  getCard(id: number): Observable<Card> {
    //return of(CARDS.find(card => card.multiverseid === id));
    return this.getCards().pipe(map(cards => cards.filter(card => card.multiverseid === id).pop()));
  }
}
