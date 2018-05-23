import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { ModeService } from '../mode.service';
import { Mode } from '../models/mode';

@Component({
  selector: 'app-select-mode',
  template: ` Mode:
    <select name="mode_selection" size="1" (change)="onSelect($event.target.value)">
      <option *ngFor="let mode of mode$ | async" value={{mode.name}} [selected]="mode.name === selectedMode">{{mode.name}}</option>
    </select>
  `,
  styleUrls: ['./select-mode.component.css']
})
export class SelectModeComponent implements OnInit {
  mode$: Observable<Mode[]>;
  @Input() selectedMode: string;  
  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(private modeService: ModeService) { }

  ngOnInit() {    
    this.mode$ = this.getModes();    
  }

  /** Get the list of available models */
  getModes(): Observable<Mode[]> {
    return this.modeService.getModes();    
  }

  onSelect(value) {
    this.select.emit(value);
  }
}