import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { Observable } from "rxjs";
import { DeckService } from '../deck.service';
import { Deck } from '../models/deck';
import { Card } from '../models/card';

@Component({
  selector: 'app-deck-view',
  template: `
    <div class="hlayout">   
      <a routerLink="/catalog" id="menu"> Cards </a>
      <a routerLink="/decks" id="menu"> Decks </a>
      <a routerLink="/" id="menu"> New Deck </a>    
    </div>

    <div style="border: solid; margin: 5px;">      
      <h2 style="padding: 5px 5px 0px 5px;"> My deck </h2>      
      <app-deck-attributes [deck]="deckService.getDeck() | async"> </app-deck-attributes>
    </div>

    <app-deck-cards [cards]="deckService.getCards() | async"> </app-deck-cards>   
  `,
  styleUrls: ['./deck-view.component.css']
})
export class DeckViewComponent implements OnInit {
  deck$: Observable<Deck>;
  deckCards$: Observable<Card[]>;

  constructor(public deckService: DeckService,
              private router: Router) { }

  ngOnInit() {
    this.deck$ = this.deckService.getDeck();
    this.deckCards$ = this.deckService.getCards();
  }

  onClick(event) {
    this.router.navigate(['']);
  }
}
