import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { CardService }  from '../card.service';
import { Card } from '../models/card'

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent implements OnInit {
  card: Card;
  selectedCard : Card;

  constructor(
    private route: ActivatedRoute,
    private cardService: CardService,
    private location: Location) { }

  ngOnInit() {
    this.getCard();
  }

  getCard(): void {
    const id = +this.route.snapshot.paramMap.get('multiverseid');
    this.cardService.getCard(id)
      .subscribe(card => this.card = card);
  }

  onSelect(card: Card): void{
    this.selectedCard  = card;    
  }

  goBack(): void {
    this.location.back();
  }
}
