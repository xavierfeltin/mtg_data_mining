import { Injectable } from '@angular/core';
import { Color } from './models/color';
import { COLORS } from './store/store-color';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ColorService {

  constructor() { }

  getColors(): Observable<Color[]>{
    return of([{name: 'All Colors'}, ...COLORS]);
  }

  getReducedColors(): Observable<Color[]>{
    //return of([...COLORS.slice(0, COLORS.length-1), new Color('No Color')]);
    return of(COLORS);
  }
}
