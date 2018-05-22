import { Injectable } from '@angular/core';
import { Mode } from './models/mode';
import { MODES } from './store/store-mode';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModeService {

  constructor() { }

  getModes(): Observable<Mode[]>{
    return of(MODES);
  }
}
