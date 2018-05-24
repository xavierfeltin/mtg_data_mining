import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../models/card';
import { Observable, Subscription } from 'rxjs';
import { ModeService } from '../mode.service';

@Component({
  selector: 'app-recommendation-child-game',
  template: `
    <div>
      <h2>Items Recommendations:</h2>
      <p class="information">Recommendations are cards played the most together with the selected card (<a href="https://github.com/xavierfeltin/mtg_data_mining/wiki/Collaborative-Filtering" target="_blank">more information</a>)
      <br/> A score of 1 means the two cards are only played together </p>
      <app-select-mode (select)="onSelect($event)" [card]="card" [defaultMode]="filterMode"></app-select-mode>
    </div>
    <app-recommendation-child-color [card]="card" [gameMode]="filterMode"></app-recommendation-child-color>
    `,
  styleUrls: ['./recommendation-child-game.component.css']
})
export class RecommendationChildGameComponent implements OnInit {
  @Input() card: Card;
  filterMode: string;
  subscription: Subscription;
  
  constructor(private modeService: ModeService) { }

  ngOnInit() {
    this.subscription = this.getFirstMode().subscribe(card => this.filterMode = card);
  }

  onSelect(selected: string): void{
    console.log(selected);
    this.filterMode = selected;
  }

  getFirstMode(): Observable<string> {
    return this.modeService.getFirstMode(this.card);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
