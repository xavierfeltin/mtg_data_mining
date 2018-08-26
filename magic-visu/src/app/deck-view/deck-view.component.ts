import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { Observable } from 'rxjs';
import { Deck } from '../models/deck';
import { Card } from '../models/card';
import { DeckService } from '../deck.service';

@Component({
  selector: 'app-deck-view',
  template: `
    <div class="hlayout"> 
    <h2> <a routerLink="/catalog"> My deck </a> </h2>
    <button class="nav-button" (click)="onClick($event)"> New deck </button>
    </div>
    <app-deck-attributes [deck]="deck$ | async"> </app-deck-attributes>
  `,
  styleUrls: ['./deck-view.component.css']
})
export class DeckViewComponent implements OnInit {
  deck$: Observable<Deck>;
  //cards$: Observable<Card[]>;  
  constructor(private deckService: DeckService,
              private router: Router) { }

  ngOnInit() {
    //this.deckService.getDeck().subscribe(deck => this.deck = deck);
    //this.cards$ = this.deckService.getCards();
    this.deck$ = this.deckService.getDeck();
  }

  onClick(event) {
    this.router.navigate(['']);
  }
}
