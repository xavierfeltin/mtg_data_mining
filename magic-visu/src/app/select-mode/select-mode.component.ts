import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { ModeService } from '../mode.service';
//import { Mode } from '../models/mode';
import { Card } from '../models/card';

@Component({
  selector: 'app-select-mode',
  template: `
    <label for="mode_selection"> Mode: <label>
    <select id="mode_selection" name="mode_selection" size="1" (change)="onSelect($event.target.value)">
      <option *ngFor="let mode of mode$ | async; let i = index" value={{mode}} [selected]="mode === defaultMode">{{mode}}</option>
    </select>
  `,
  styleUrls: ['./select-mode.component.css']
})
export class SelectModeComponent implements OnInit {
  mode$: Observable<string[]>;
  @Input() card: Card;
  @Input() defaultMode: string;
  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(private modeService: ModeService) { }

  ngOnInit() {        
    this.mode$ = this.getModes();    
  }

  /** Get the list of available models */
  getModes(): Observable<string[]> {
    return this.modeService.getModes(this.card);    
  }

  onSelect(value) {
    this.select.emit(value);
  }
}