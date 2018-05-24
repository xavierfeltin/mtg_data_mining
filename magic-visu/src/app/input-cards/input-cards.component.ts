import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-input-cards',
  template: `
    <label for="name_selection" class="form-component">Card's name:</label>
    <input id="name_selection" type="text" name="card-name" id="card-name" class="form-component" [value]="defaultValue">
  `,
  styleUrls: ['./input-cards.component.css']
})
export class InputCardsComponent implements OnInit {
  @Input() defaultValue: string;
  constructor() { }

  ngOnInit() {
  }
}
