import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Deck } from './models/deck';
import { Card } from './models/card';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators'
import { Color } from './models/color';
import { Mode } from './models/mode';
import { LAND } from './store/store-type';
import { map, publishReplay, refCount } from 'rxjs/operators';
import { CardService } from './card.service';

@Injectable({
  providedIn: 'root'
})
export class DeckService {

  _deck: Deck;
  _decks: Observable<number[][]> ;

  constructor(private http: HttpClient,
             private cardService: CardService) { }

  getDeck(): Observable<Deck>{    
    if(!this._deck) {
      this._deck = new Deck();
    }    
    return of(this._deck);
  }

  getCards(): Observable<Card[]>{    
    return of(this._deck.cards);
  }

  getAllCards(): Observable<Card[]>{
    let allCards = [];
    for(const card of this._deck.cards) {
      const nbInstances = this._deck.instances[card.multiverseid];
      for(let i = 0; i < nbInstances; i++) {
        allCards.push(card);
      }
    }
    return of(allCards);
  }

  getActiveCards(): Observable<Card[]>{
    return of(this._deck.cards.filter(card => !card.types.includes(LAND)));
  }

  getInstances(): Observable<{}>{    
    return of(this._deck.instances);
  }

  getColors(): Color[]{
    return this._deck.colors;
  }

  getMode(): Mode{
    return this._deck.mode;
  }

  update(deck: Deck): Observable<Deck>{
    this._deck = Deck.createDeck(deck.colors.map(color => color.name), deck.mode.name);
    this._deck.cards = [...deck.cards];
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

  incrementCard(card: Card) {
    this._deck.addInstance(card);
    return of(this._deck);
  }

  decrementCard(card: Card) {
    this._deck.removeInstance(card);
    return of(this._deck);
  }

  loadDecks(): Observable<number[][]> {
    if (!this._decks) {
      const colors = this._deck.colors.map(color => color.name);
      const mode = this._deck.mode.name;
      const filename = 'decks_' + mode + '_' + colors.join('_');
      this._decks = this.http.get<number[][]>('./assets/' + filename + '.json')
      .pipe(                        
        publishReplay(),
        refCount(),
        catchError(this.handleError)
      );
    }
    return this._decks;
  }

  getDeckAt(pos: number): Observable<number[]> {
    if (pos == -1) {
      return of(this._deck.cards.map(card => card.multiverseid));
    }
    else {
      return this._decks.pipe<number[]>(map(decks => decks[pos]));
    }    
  }

  getDecksName(): Observable<string[]> {
    return this._decks.pipe<string[]>(map(decks => decks.map((row, i) => 'Deck-' + (i+1))));
  }

  cleanCache() {
    this._decks = null;
  }

  private handleError(error: HttpErrorResponse) {
    return throwError(
      'Something bad happened; please try again later.');
  };
}