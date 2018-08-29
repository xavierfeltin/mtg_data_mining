import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { Deck } from '../models/deck';

@Component({
  selector: 'app-deck-attributes',
  template: `
    <div style="padding: 0px 5px 5px 5px;">
      <ng-container *ngIf="!deck.isUndefined(); else empty">    
        <p class="subtitle"> Mode: <span class="information"> {{deck.mode.name}} </span> </p>
        <p class="subtitle"> Colors: <span class="information"> {{colors}} </span> </p>
      </ng-container>
      <ng-template #empty>      
        <p class="information"> No deck created... </p>
      </ng-template>    
    </div>
  `,
  styleUrls: ['./deck-attributes.component.css']
})
export class DeckAttributesComponent implements OnInit, OnChanges {
  @Input() deck: Deck;
  colors: string;

  constructor() { }

  ngOnInit() {}

  ngOnChanges() {
    this.colors = this.deck['colors'].map(color => color.name).join(' / ');
  }
}