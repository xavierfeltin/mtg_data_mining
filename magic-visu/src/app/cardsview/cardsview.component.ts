import { Component, OnInit } from '@angular/core';
import { Card } from '../models/card';
import { CARDS } from '../mock-cards';
import { CardService } from '../card.service';

@Component({
  selector: 'app-cardsview',
  templateUrl: './cardsview.component.html',
  styleUrls: ['./cardsview.component.css']
})
export class CardsviewComponent implements OnInit {
  cards: Card[];
  selectedCard: Card;

  constructor(private cardService: CardService) { }

  ngOnInit() {
    this.getCards();
  }

  onSelect(card: Card): void{
    this.selectedCard  = card;
    console.log(card.name);
  }
  
  getCards(): void {
    this.cardService.getCards()
      .subscribe(cards => this.cards = cards);
  }
}
