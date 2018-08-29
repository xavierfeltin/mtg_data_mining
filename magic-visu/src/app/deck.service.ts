import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Deck } from './models/deck';
import { Card } from './models/card';
import { Observable, of } from 'rxjs';
import { count} from 'rxjs/operators';
import { Color } from './models/color';
import { Mode } from './models/mode';
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

  getColors(): Color[]{
    //return of([...this._deck.colors, new Color('No color')]);
    return this._deck.colors;
  }

  getMode(): Mode{
    return this._deck.mode;
  }

  //TODO: delete in future if unused
  createDeck(colors: string[], mode: string) {
    //this._deck.createDeck(colors, mode);    
    this._deck = Deck.createDeck(colors, mode);
  }

  update(deck: Deck): Observable<Deck>{
    this._deck = Deck.createDeck(deck.colors.map(color => color.name), deck.mode.name);
    this._deck.cards = [...deck.cards];
    //this._deck.colors = [...deck.colors];
    //this._deck.mode = new Mode(deck.mode.name);
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

  loadDecks(): Observable<number[][]> {
    if (!this._decks) {
      const colors = this._deck.colors.map(color => color.name);
      const mode = this._deck.mode.name;
      const filename = 'decks_' + mode + '_' + colors.join('_');
      this._decks = this.http.get<number[][]>('./assets/' + filename + '.json')
      .pipe(        
        publishReplay(),
        refCount(),
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
}