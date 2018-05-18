import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../models/Card';

@Component({
  selector: 'app-recommendation-child-game',
  templateUrl: './recommendation-child-game.component.html',
  styleUrls: ['./recommendation-child-game.component.css']
})
export class RecommendationChildGameComponent implements OnInit {
  @Input() card: Card;

  constructor() { }

  ngOnInit() {
  }

  getGameModes(): string[] {
    return Object.keys(this.card.itemRecommendations);
  }
}
