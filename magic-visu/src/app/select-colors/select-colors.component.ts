import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { ColorService } from '../color.service';
import { Color } from '../models/color';

@Component({
  selector: 'app-select-colors',
  template: `
    <select name="color_selection" size="1" (change)="onSelect($event.target.value)">
      <option disabled selected value> -- select a color -- </option>
      <option *ngFor="let color of colors$ | async" value={{color.name}}>{{color.name}}</option>
    </select>
  `,
  styleUrls: ['./select-colors.component.css']
})
export class SelectColorsComponent implements OnInit {
  colors$: Observable<Color[]>;

  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(private colorService: ColorService) { }

  ngOnInit() {    
    this.colors$ = this.getColors();
  }

  /** Get the list of available models */
  getColors(): Observable<Color[]> {
    return this.colorService.getColors();    
  }

  onSelect(value) {
    this.select.emit(value);
  }
}
