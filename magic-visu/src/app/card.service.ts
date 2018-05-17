import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Card } from './models/card'
import { CARDS } from './mock-cards'

@Injectable({
  providedIn: 'root'
})
export class CardService {

  constructor() { }

  getCards(): Observable<Card[]> {
    return of(CARDS);
  }

  getCard(id: number): Observable<Card> {
    return of(CARDS.find(card => card.multiverseid === id));
  }
}
