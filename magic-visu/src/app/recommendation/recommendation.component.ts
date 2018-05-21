import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/Operators';
import { CardService }  from '../card.service';
import { Card } from '../models/card';

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.css']
})
export class RecommendationComponent implements OnInit {
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
  
  ngOnInit() {}

  onSelect(card: Card): void{
    this.selectedCard  = card;    
  }

  goBack(): void {
    this.location.back();
  }
}
