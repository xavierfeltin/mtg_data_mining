import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Color } from '../models/color';

@Component({
  selector: 'app-select-colors',
  template: `
    <label for="color_selection" class="form-component"> Color: </label>
    <select id="color_selection" name="color_selection" size="1" class="form-component" (change)="onSelect($event.target.value)">
      <option *ngFor="let color of colors" value={{color.name}} [selected]="color.name === selectedColor">{{color.name}}</option>      
    </select>
  `,
  styleUrls: ['./select-colors.component.css']
})
export class SelectColorsComponent implements OnInit {
  //colors$: Observable<Color[]>;
  @Input() selectedColor: string;
  @Input() colors: Color[];
  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(/*private colorService: ColorService*/) { }

  ngOnInit() {}

  onSelect(value) {        
    this.select.emit(value);
  }
}
