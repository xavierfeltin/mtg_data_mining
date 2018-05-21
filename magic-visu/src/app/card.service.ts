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
      this._cards = this.http.get<Card[]>('./assets/db_similarities_small.json')
      .pipe(
        map(cards => cards.sort(this.compareCardsFn)),
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

  compareCardsFn(a: Card, b: Card): number {
    //order by nb colors, color, manaCost and name
    let compareColors = function compareColors(a: Card, b: Card): number {
      if (a.colors.length < b.colors.length){return -1;}
      else if (a.colors.length > b.colors.length) {return 1;}    
      else {
        let comparison = 0;
        let nbColors = a.colors.length;
        let i = 0;
        while (i < nbColors && comparison == 0) {
          if (a.colors[i] < b.colors[i]) {
            comparison = -1;      
          }
          else if (a.colors[i] > b.colors[i]) {
            comparison = 1;
          }
          i++;
        } 
        return comparison;     
      }       
    };
  
    let compareManaCost = function compareManaCost(a: Card, b: Card): number {
      if (a.manaCost < b.manaCost) {return -1;}
      else if (a.manaCost > b.manaCost) {return 1;}
      else return 0;
    };
  
    let compareName = function compareName(a: Card, b: Card): number {
      if (a.name < b.name) {return -1;}
      else if (a.name > b.name) {return 1;}
      else return 0;
    };
    
    let comparison = compareColors(a,b);
    if (comparison == 0) {
      comparison = compareManaCost(a,b);        
    }
    if (comparison == 0) {
      comparison = compareName(a,b);
    }
    return comparison;             
  }
}
