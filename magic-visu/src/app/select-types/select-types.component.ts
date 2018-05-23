import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { Type } from '../models/type';
import { TypeService } from '../type.service';

@Component({
  selector: 'app-select-types',
  template: `
  <label for="type_selection"> Type: <label>
  <select id="type_selection" name="type_selection" size="1" (change)="onSelect($event.target.value)">
    <option *ngFor="let type of types$ | async" value={{type.name}} [selected]="type.name === selectedType">{{type.name}}</option>
  </select>
  `,
  styleUrls: ['./select-types.component.css']
})
export class SelectTypesComponent implements OnInit {
  types$: Observable<Type[]>;
  @Input() selectedType: string;
  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(private typeService: TypeService) { }

  ngOnInit() {    
    this.types$ = this.getTypes();
  }

  /** Get the list of available models */
  getTypes(): Observable<Type[]> {
    return this.typeService.getTypes();    
  }

  onSelect(value) {
    this.select.emit(value);
  }
}
