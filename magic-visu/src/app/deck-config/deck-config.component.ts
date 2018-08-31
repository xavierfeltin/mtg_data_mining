import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { Observable } from 'rxjs';
import { Color } from '../models/color';
import { Mode } from '../models/mode';
import { Deck } from '../models/deck';
import { ColorService } from '../color.service';
import { ModeService } from '../mode.service';
import { CardService } from '../card.service';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';

@Component({
  selector: 'app-deck-config',
  template: `
    <h2> Create a new deck </h2>
    <p class=information> You may find the data repartition between the different modes and colors inside the 
      <a href="https://github.com/xavierfeltin/mtg_data_mining/wiki/Proof-of-concept#decks-repartitions" target="_"> wiki </a> 
      <br/> Models with less than 30 decks as input are not available </p>
    <i> This deck will replace the current one </i>
    <app-deck-form [colors]="color$ | async" [modes]="mode$ | async" (create)="onSubmit($event)"></app-deck-form>
    <ng-container *ngIf="errors.length > 0">
      <p class="information"> Something occured when loading assets for {{mode}} - {{colors.join(' / ')}} ... </p>
      <ul>
        <li *ngFor="let err of errors" class="error"> {{err}} </li>
      </ul>  
    </ng-container>
  `,
  styleUrls: ['./deck-config.component.css']
})
export class DeckConfigComponent implements OnInit {
  color$: Observable<Color[]>;
  mode$:  Observable<Mode[]>;  
  errors: string[];
  mode: string;
  colors: string[];

  constructor(private colorService: ColorService, 
              private modeService: ModeService,
              private cardService: CardService,
              private modelService: ModelService,
              private deckService: DeckService,              
              private router: Router) {}

  ngOnInit() {
    this.color$ = this.colorService.getReducedColors();
    this.mode$ =  this.modeService.getAllModes();
    this.errors = [];
  }

  async onSubmit(event: Deck) {
    this.colors = event.colors.map(color => color.name);
    this.mode = event.mode.name;
    this.errors = [];

    await this.deckService.update(event).toPromise();  
    this.cardService.cleanCache();
    this.modelService.cleanCache();
    this.deckService.cleanCache();

    try {
      await this.deckService.loadDecks().toPromise();
    } catch (error) { this.errors.push('Decks list is not available'); }

    try {
      await this.cardService.loadCards(this.colors, this.mode).toPromise();
    } catch (error) { this.errors.push('Cards catalog is not available'); }

    try {
      await this.modelService.loadLSAModel(this.colors, this.mode).toPromise();
    } catch (error) { this.errors.push('LSA model is not available'); }
    
    try {
      await this.modelService.loadTopNModel(this.colors, this.mode).toPromise();
    } catch (error) { this.errors.push('TopN model is not available'); }

    if (this.errors.length == 0) {
      this.router.navigate(['catalog']);
    }
  }
}
