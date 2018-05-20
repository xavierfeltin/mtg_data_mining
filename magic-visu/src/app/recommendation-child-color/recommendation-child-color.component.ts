import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../models/card';

@Component({
  selector: 'app-recommendation-child-color',
  //templateUrl: './recommendation-child-color.component.html',
  template: `
    <div *ngFor="let color of this.getColors()">
      <h3>{{this.gameMode}} - {{formatColor(color)}}</h3>
      <app-recommendationview [recommendation]="recommendation" *ngFor="let recommendation of this.card.itemRecommendations[this.gameMode][color]" class="cards"></app-recommendationview>
    </div>`,
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

  formatColor(colorToFormat: string): string{
    let colors: string[] = colorToFormat.split('_');
    let formattedColor: string = '';
    colors.forEach((color, index) => {
      formattedColor += color.charAt(0).toUpperCase() + color.slice(1);
      if (index != (colors.length -1)) {formattedColor += ' / '; }
    });
       
    return formattedColor;
  }
}
