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
    return of(COLORS);
  }
}
