import { Injectable } from '@angular/core';
import { Type } from './models/type';
import { TYPES } from './store/store-type';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  constructor() { }

  getTypes(): Observable<Type[]>{
    return of([{name: 'All Types'}, ...TYPES]);
  }
}
