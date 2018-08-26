import { Injectable } from '@angular/core';
import { Deck } from './models/deck';
import { Card } from './models/card';
import { DECK } from './store/store-deck';
import { Observable, of } from 'rxjs';
import { Color } from './models/color';
import { COLORS } from './store/store-color';
import { makePropDecorator } from '@angular/core/src/util/decorators';
import { Mode } from './models/mode';

@Injectable({
  providedIn: 'root'
})
export class DeckService {

  _deck: Deck;

  constructor() { }

  getDeck(): Observable<Deck>{
    if(!this._deck) {
      this._deck = new Deck();
      this._deck.cards = [...DECK.cards];
      this._deck.colors = [...DECK.colors];      
      this._deck.mode = DECK.mode;
    }
    return of(this._deck);
  }

  getCards(): Observable<Card[]>{    
    return of(this._deck.cards);    
  }

  getColors(): Color[]{
    //return of([...this._deck.colors, new Color('No color')]);
    return this._deck.colors;
  }

  getMode(): Mode{
    return this._deck.mode;
  }

  //TODO: delete in future if unused
  createDeck(colors: string[], mode: string) {
    this._deck.createDeck(colors, mode);    
  }

  update(deck: Deck): Observable<Deck>{
    this._deck.cards = [...deck.cards];
    this._deck.colors = [...deck.colors];
    this._deck.mode = new Mode(deck.mode.name);
    return of(this._deck);
  }

  removeCard(card: Card) {
    this._deck.removeCard(card);
    return of(this._deck);
  }

  addCard(card: Card) {
    this._deck.addCard(card);
    return of(this._deck);
  }
}