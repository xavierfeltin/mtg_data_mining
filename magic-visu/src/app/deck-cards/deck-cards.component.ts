import { Component, OnInit, Input } from '@angular/core';
import { DeckService } from '../deck.service';
import { Card } from '../models/card';
import { TYPES } from '../store/store-type'

@Component({
  selector: 'app-deck-cards',
  template: `
  <div class="deck-block" style="padding: 5px;">     
    <div style="min-height: 100px;" droppable [dragOverClass]="'drag-target-border'" [dragHintClass]="'drag-hint'" (onDrop)="onItemDrop($event)">
      <ng-container *ngIf="cards.length > 0; else empty">      
      
        <p class=information> {{cards.length}} selected cards </p>
        <ng-container *ngFor="let type of types"> 
            <ng-container *ngIf="filterByType(type).length > 0"> 
            <span class="subtitle"> {{type}}: </span>
            <ul>
              <div class="hlayout" *ngFor="let card of filterByType(type); let i = index">
                <li>
                  <app-card-link [card]="card"></app-card-link>
                </li>
                <button class="nav-button" (click)="onRemoveCard($event, card)"> ❌ </button>
              </div>
            </ul>
            </ng-container>  
        </ng-container>
      
      </ng-container>
    </div>
  </div>  
  
  <ng-template #empty>      
    <p class="information"> Drag and drop here some cards ! </p>
  </ng-template> 
  `,
  styleUrls: ['./deck-cards.component.css']
})
export class DeckCardsComponent implements OnInit {  
  @Input() cards: Card[] = [];  
  types: string[] = [];  

  constructor(private deckService: DeckService) { }

  ngOnInit() {
    this.types = TYPES.map(type => type.name).sort();
  }

  filterByType(type: string): Card[] {
    let filtered = this.cards.filter(function(card, index, arr) {
      return card.types.includes(type);
    })

    return filtered.sort(function(a,b) {
      if (a.name === b.name) {
        return 0;
      }
      else {
        return a.name < b.name ? -1 : 1;
      }
    })
  }

  onRemoveCard(event, card) {    
    this.deckService.removeCard(card);
  }

  onItemDrop(event) {    
    this.deckService.addCard(event.dragData);
  }
}
