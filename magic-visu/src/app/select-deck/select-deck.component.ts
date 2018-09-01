import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs';
import { DeckService } from '../deck.service';
import { map } from 'rxjs/Operators';

@Component({
  selector: 'app-select-deck',
  template: `
    <label for="type_selection" class="form-component"> Type: <label>
    <select id="type_selection" name="type_selection" class="form-component" size="1" (change)="onSelect($event.target.value)">
      <option *ngFor="let deck of decks" value={{deck}} [selected]="deck === selectedDeck">{{deck}}</option>
    </select>
  `,
  styleUrls: ['./select-deck.component.css']
})
export class SelectDeckComponent implements OnInit {
  decks: string[] = [];
  @Input() selectedDeck: string = '';
  @Output() select: EventEmitter<string> = new EventEmitter();

  constructor(private deckService: DeckService) { }

  ngOnInit() {    
    this.deckService.getDecksName().subscribe(names => {
      this.decks = ['My Deck', ...names]
    });
  }

  onSelect(value) {
    this.select.emit(value);
  }
}
