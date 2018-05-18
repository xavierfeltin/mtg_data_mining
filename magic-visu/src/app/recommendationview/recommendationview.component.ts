import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { CardService } from '../card.service'
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',  
  template: `
    <a routerLink="/recommendation/{{recommendation.multiverseid}}">
    <img [src]="cardUrl" [alt]="card.name" [title]="title"/>
    </a>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent implements OnInit {
  @Input() recommendation: CardRecommendation;
  card: Card;
  
  constructor(private cardService: CardService) { }

  ngOnInit() {
    this.cardService.getCard(this.recommendation.multiverseid)
    .subscribe(card => this.card = card);
  }

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.multiverseid}`;
  } 

  get title() {
    return this.recommendation.item_similarity === null ? 
      `Content score: ${this.recommendation.content_similarity}`
      :`Item score: ${this.recommendation.item_similarity}\nContent score: ${this.recommendation.content_similarity}`;
  }
}
