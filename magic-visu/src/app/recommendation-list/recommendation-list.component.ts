import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { Model, ModelLSA, ModelTopN } from '../models/Model';
import { CardRecommendation } from '../models/card-recommendation';
import { Card } from '../models/card';
import { Observable } from 'rxjs';
import { CardService } from '../card.service';

@Component({
  selector: 'app-recommendation-list',
  template: `
  <ng-container *ngIf="cards.length > 0; else empty">
    <div class="cards-grid">
      <app-recommendationview class="card"
        *ngFor="let recommendation of recommendations"
        [recommendation]="recommendation" [card]="getCardOf(recommendation) | async"
      >
      </app-recommendationview>
    </div>
  </ng-container>

  <ng-template #empty>      
    <p class="information"> <b> No card available for making recommendations... </b> </p>
  </ng-template>
  `,
  styleUrls: ['./recommendation-list.component.css']
})
export class RecommendationListComponent implements OnInit, OnChanges {
  @Input() model: Model = new ModelLSA([], {});
  @Input() cards: Card[] = [];
  @Input() nbRecommendations: number = 5;
  @Input() modelType: string = '';
  recommendations: CardRecommendation[] = [];

  constructor(private cardService: CardService) { }

  ngOnInit() {}

  ngOnChanges() {
    if (this.model != null && this.cards != null) {
      const instanceModel = this.isLSA() ? new ModelLSA(this.model.cards, this.model.coefficients) : new ModelTopN(this.model.cards, this.model.coefficients);  
      this.recommendations = instanceModel.getRecommendations(this.cards, this.nbRecommendations);
    }
  }

  isLSA(): boolean {
    return this.modelType === "LSA";
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }
}
