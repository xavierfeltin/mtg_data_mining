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
    <i> This deck will replace the current one </i>
    <app-deck-form [colors]="color$ | async" [modes]="mode$ | async" (create)="onSubmit($event)"></app-deck-form>
  `,
  styleUrls: ['./deck-config.component.css']
})
export class DeckConfigComponent implements OnInit {
  color$: Observable<Color[]>;
  mode$:  Observable<Mode[]>;  

  constructor(private colorService: ColorService, 
              private modeService: ModeService,
              private cardService: CardService,
              private modelService: ModelService,
              private deckService: DeckService,              
              private router: Router) {}

  ngOnInit() {
    this.color$ = this.colorService.getReducedColors();
    this.mode$ =  this.modeService.getAllModes();
  }

  async onSubmit(event: Deck) {
    await this.deckService.update(event).toPromise();  
    this.cardService.cleanCache();
    this.router.navigate(['catalog']);
  }
}
