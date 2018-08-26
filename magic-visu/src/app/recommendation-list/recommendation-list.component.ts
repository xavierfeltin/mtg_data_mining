import { Component, OnInit, Input } from '@angular/core';
import { Model, ModelLSA, ModelTopN } from '../models/Model';
import { CardRecommendation } from '../models/card-recommendation';
import { Card } from '../models/card';
import { Observable } from 'rxjs';
import { CardService } from '../card.service';
import { isPlatformServer } from '@angular/common';

@Component({
  selector: 'app-recommendation-list',
  template: `
  <div class="cards-grid">
    <app-recommendationview class="card"
      *ngFor="let recommendation of recommendations"
      [recommendation]="recommendation" [card]="getCardOf(recommendation) | async"
    >
    </app-recommendationview>
  </div>
  `,
  styleUrls: ['./recommendation-list.component.css']
})
export class RecommendationListComponent implements OnInit {
  @Input() model: Model;
  @Input() card: Card;
  @Input() nbRecommendations: number = 5;
  @Input() modelType: string;
  recommendations: CardRecommendation[];

  constructor(private cardService: CardService) { }

  ngOnInit() {}

  ngOnChanges() {
    if (this.model != null) {
      const instanceModel = this.isLSA() ? new ModelLSA(this.model.cards, this.model.coefficients) : new ModelTopN(this.model.cards, this.model.coefficients);  
      this.recommendations = instanceModel.getRecommendations(this.card, this.nbRecommendations);
    }
  }

  isLSA(): boolean {
    return this.modelType === "LSA";
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }
}
