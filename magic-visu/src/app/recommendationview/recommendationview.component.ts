import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { CardService } from '../card.service'
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

import { Observable } from 'rxjs';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',  
  template: `
    <a routerLink="/recommendation/{{recommendation.multiverseid}}">
    <img [src]="cardUrl" [alt]="name" [title]="title"/>
    </a>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent implements OnInit {
  card$: Observable<Card>;
  card: Card;
  @Input() recommendation: CardRecommendation;
 
  constructor(private cardService: CardService) { }

  ngOnInit() {
    //this.card$ = this.cardService.getCard(this.recommendation.multiverseid);
    this.cardService.getCard(this.recommendation.multiverseid).subscribe(card => this.card = card);
  }

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.multiverseid}`;
  } 

  get title() {
    return this.recommendation.itemSimilarity === null ? 
      `Content score: ${this.recommendation.contentSimilarity}`
      :`Item score: ${this.recommendation.itemSimilarity}\nContent score: ${this.recommendation.contentSimilarity}`;
  }

  get name() { 
   return this.card.name;
  }
}
