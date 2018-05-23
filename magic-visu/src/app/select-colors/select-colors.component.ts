import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { ColorService } from '../color.service';
import { Color } from '../models/color';

@Component({
  selector: 'app-select-colors',
  template: `
    <label for="color_selection" class="form-component"> Color: </label>
    <select id="color_selection" name="color_selection" size="1" class="form-component" (change)="onSelect($event.target.value)">
      <option *ngFor="let color of colors$ | async" value={{color.name}} [selected]="color.name === selectedColor">{{color.name}}</option>
    </select>
  `,
  styleUrls: ['./select-colors.component.css']
})
export class SelectColorsComponent implements OnInit {
  colors$: Observable<Color[]>;
  @Input() selectedColor: string;
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
