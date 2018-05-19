import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { Card } from './models/card'
import { CARDS } from './mock-cards'

@Injectable({
  providedIn: 'root'
})
export class CardService {
  cards: Card[];

  constructor(private http: HttpClient) { }

  getCards(): Observable<Card[]> {
    //return of(CARDS);
    return this.http.get<Card[]>('./assets/db_similarities_small.json');
  }

  getCard(id: number): Observable<Card> {
    return of(CARDS.find(card => card.multiverseid === id));
  }
}
