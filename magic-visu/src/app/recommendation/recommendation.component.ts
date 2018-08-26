import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/Operators';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';
import { Color } from '../models/Color';
import { Mode } from '../models/Mode';
import { ModelLSA, ModelTopN } from '../models/Model';
import { CardService } from '../card.service';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent {
  card$: Observable<Card>;
  colors: string[];
  mode: string;
  selectedCard : Card;
  modelLSA: ModelLSA;
  modelTopN$: Observable<ModelTopN>;

  constructor(
    private route: ActivatedRoute,
    private cardService: CardService,
    private deckService: DeckService,
    private modelService: ModelService,
    private location: Location) {
      this.card$ = route.params.pipe(
        map(params => +params.multiverseid),
        switchMap(id => this.cardService.getCard(id))
      );      
    }

  ngOnInit() {
    this.colors = this.deckService.getColors().map(color => color.name);
    this.mode = this.deckService.getMode().name;
    this.card$.subscribe(card => this.selectedCard = card);
    this.modelService.loadLSAModel(this.colors, this.mode).subscribe(model => this.modelLSA = model);
    //this.modelTopN$ = this.modelService.loadTopNModel(this.colors, this.mode);
  }

  getCardOf(recommendation: CardRecommendation): Observable<Card> {
    return this.cardService.getCard(recommendation.multiverseid);
  }

  formatColor(colors: string[]): string {
    return colors.join(' / ');
  }

  /*
  onSelect(card: Card): void{
    this.selectedCard = card;
  }
  */

  goBack(): void {
    this.location.back();
  }
}
