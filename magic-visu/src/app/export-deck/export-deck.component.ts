import { Component, OnInit, Input } from '@angular/core';
import { saveAs } from "file-saver";
import { Deck } from '../models/deck';

@Component({
  selector: 'app-export-deck',
  template: `
    <button class="nav-button" (click)="onExport($event, deck)" *ngIf="deck.cards.length > 0;"> Export </button>
  `,
  styleUrls: ['./export-deck.component.css']
})
export class ExportDeckComponent implements OnInit {
  @Input() deck: Deck = new Deck();

  constructor() { }

  ngOnInit() {}

  onExport(event, deck: Deck) {
    const content = this.deck.cards.map(card => this.deck.instances[card.multiverseid] + ' ' + card.name).join('\r\n')
    let file = new Blob([content], {type: "application/octet-stream;charset=utf-8"});
    saveAs(file, "my_deck.dec");
  }
}
