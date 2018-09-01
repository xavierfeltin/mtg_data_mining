import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';
import { CardService } from '../card.service';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-recommendationview',
  template: `
    <div draggable [dragData]="card">
    <div class="score"> {{title}} </div>
    <a routerLink="/recommendation/{{recommendation.multiverseid}}">
      <img [src]="cardUrl" [alt]="card?.name" [title]="toolTip"/>
    </a>
    </div>
    `,
  styleUrls: ['./recommendationview.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RecommendationviewComponent implements OnInit {
  @Input() card: Card = new Card();
  @Input() recommendation: CardRecommendation = new CardRecommendation(0, 0, {});
  contributions: Card[] = [];

  constructor(private cardService: CardService) {}

  ngOnInit() {            
    this.cardService.getCardsById(Object.keys(this.recommendation.contributions)
      .map(key => parseInt(key)))
      .subscribe(cards => this.contributions = cards);
  }

  get cardUrl() {
    return `${CARD_IMG_URL}${this.recommendation.multiverseid}`;
  }

  get title() {
    return `Content: ${this.recommendation.score.toFixed(3)}`;
  }

  get toolTip() {
    if (Object.keys(this.contributions).length > 0) {
      let meaningfulContribs = [];
      for(const card of this.contributions) {
        if (this.recommendation.contributions[card.multiverseid]) {
          meaningfulContribs.push({name: card.name, contribution: this.recommendation.contributions[card.multiverseid]});
        }
      }
      
      meaningfulContribs.sort(function(a,b) {
        const valA = a['contribution'];
        const valB = b['contribution'];

        if (valA == valB) {return 0;}
        else if (valA < valB) {return 1;}
        else return -1;
      });

      let title = 'Since you selected: \n';
      for(const contrib of meaningfulContribs.slice(0,10)) {
        title += ` - ${contrib['name']}: ${(contrib['contribution'] * 100.0).toFixed(0)}% \n`        
      }    
        
      return title;
    }
    else {
      return this.card.name;
    }    
  }
}