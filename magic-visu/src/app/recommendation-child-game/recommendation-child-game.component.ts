import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../models/card';

@Component({
  selector: 'app-recommendation-child-game',
  template: `
    <div>
      <h2>Items Recommendations:</h2>
      <app-select-mode (select)="onSelect($event)" [selectedMode]="filterMode"></app-select-mode>
    </div>
    <app-recommendation-child-color [card]="card" [gameMode]="filterMode"></app-recommendation-child-color>
    `,
  styleUrls: ['./recommendation-child-game.component.css']
})
export class RecommendationChildGameComponent implements OnInit {
  @Input() card: Card;
  filterMode: string = 'Commander';
  
  constructor() { }

  ngOnInit() {
  }

  getGameModes(): string[] {
    return Object.keys(this.card.itemRecommendations);
  }

  onSelect(selected: string): void{
    this.filterMode = selected;
  }
}
