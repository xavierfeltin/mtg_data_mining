import { Injectable } from '@angular/core';
import { Card } from './models/card';
import { Mode } from './models/mode';
import { MODES } from './store/store-mode';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModeService {

  constructor() { }

  getModes(card: Card): Observable<string[]>{
    //return of(MODES);
    /*
    const modes = Object.keys(card.itemRecommendations).sort();
    return of(modes);
    */
   return of(['Legacy']);
  }

  getFirstMode(card: Card): Observable<string>{
    //return of(MODES);
    /*
    const modes = Object.keys(card.itemRecommendations).sort();        
    return of(modes[0]);
    */
    return of('Legacy');
  }

  getAllModes(): Observable<Mode[]>{
    return of(MODES);
  }
}
