import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { DeckService } from '../deck.service';

@Component({
  selector: 'app-deck-view',
  template: `
    <div class="deck-block">        
      <div class="hlayout">
        <h3> My Deck </h3> 
        <app-export-deck [deck]="deckService.getDeck() | async"></app-export-deck>
      </div>
      <app-deck-attributes [deck]="deckService.getDeck() | async"> </app-deck-attributes>
    </div>

    <app-deck-cards [cards]="deckService.getCards() | async" [instances]="deckService.getInstances() | async"> </app-deck-cards>   
  `,
  styleUrls: ['./deck-view.component.css']
})
export class DeckViewComponent implements OnInit {
  constructor(public deckService: DeckService,
              private router: Router) { }

  ngOnInit() {
  }

  onClick(event) {
    this.router.navigate(['']);
  }
}
