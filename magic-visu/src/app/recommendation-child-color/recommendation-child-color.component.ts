import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../models/card';

@Component({
  selector: 'app-recommendation-child-color',
  templateUrl: './recommendation-child-color.component.html',
  styleUrls: ['./recommendation-child-color.component.css']
})
export class RecommendationChildColorComponent implements OnInit {
  @Input() card: Card;
  @Input() gameMode: string;

  constructor() { }

  ngOnInit() {
  }

  getColors(): string[] {
    return Object.keys(this.card.itemRecommendations[this.gameMode]);
  }
}
