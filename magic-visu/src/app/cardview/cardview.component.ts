import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { Card } from '../models/card';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-cardview',  
  template: `<a routerLink="/recommendation/{{card.multiverseid}}" draggable [dragData]="card"><img [src]="cardUrl" [alt]="card.name"></a>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class CardviewComponent implements OnInit {
  @Input() card: Card = new Card();
  
  constructor() { }

  ngOnInit() {}

  get cardUrl() {
    return `${CARD_IMG_URL}${this.card.multiverseid}`;
  } 
}
