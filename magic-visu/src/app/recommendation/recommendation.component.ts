import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/Operators';
import { CardService } from '../card.service';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent {
  card$: Observable<Card>;
  selectedCard : Card;

  constructor(
    private route: ActivatedRoute,
    private cardService: CardService,
    private location: Location) {
      this.card$ = route.params.pipe(
        map(params => +params.multiverseid),
        switchMap(id => this.cardService.getCard(id))
      );
    }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }

  onSelect(card: Card): void{
    this.selectedCard = card;
  }

  goBack(): void {
    this.location.back();
  }
}
