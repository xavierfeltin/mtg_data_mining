import { Component, OnInit, Input, SimpleChanges, OnChanges } from '@angular/core';
import { DeckService } from '../deck.service';
import { Card } from '../models/card';
import { TYPES } from '../store/store-type'
import { Deck } from '../models/deck';

@Component({
  selector: 'app-deck-cards',
  template: `
  <div class="deck-block" style="padding: 5px;">     
    <div style="min-height: 100px;" droppable [dragOverClass]="'drag-target-border'" [dragHintClass]="'drag-hint'" (onDrop)="onItemDrop($event)">
      <ng-container *ngIf="cards.length > 0; else empty">      
      
        <p class=information> {{nbSelectedCards}} selected cards </p>
        <ng-container *ngFor="let type of types"> 
            <ng-container *ngIf="filterByType(type).length > 0"> 
            <span class="subtitle"> {{type}}: </span>
            <ul>
              <div class="hlayout" *ngFor="let card of filterByType(type); let i = index">
                <li>
                  <app-card-link [card]="card" [nbInstance]="instances[card.multiverseid]"></app-card-link>
                </li>
                <button class="nav-button" (click)="onIncrementCard($event, card)"> ➕ </button>
                <button class="nav-button" (click)="onDecrementCard($event, card)"> ➖ </button>
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
export class DeckCardsComponent implements OnInit, OnChanges {  
  @Input() cards: Card[] = [];
  @Input() instances: {} = {};
  types: string[] = [];  

  constructor(private deckService: DeckService) { }

  ngOnInit() {}

  ngOnChanges(change: SimpleChanges) {
    if (change.cards.previousValue) {
      if (change.cards.previousValue.length != change.cards.currentValue.length) {
        this.setTypes()
      }
    }          
  }

  setTypes() {
    for(const card of this.cards){
      const fullType = card.getFullType();
      if (!this.types.includes(fullType)){
        this.types.push(fullType);
      }
    }
    this.types = this.types.sort();
  }

  filterByType(type: string): Card[] {
    let filtered = this.cards.filter(card => {
      return card.getFullType().toLowerCase() === type.toLowerCase();
    });

    return filtered.sort(function(a,b) {
      if (a.name === b.name) {
        return 0;
      }
      else {
        return a.name < b.name ? -1 : 1;
      }
    });
  }

  get nbSelectedCards() {
    let nbCards = 0;
    Object.keys(this.instances).forEach(id => {
      nbCards += this.instances[id];
    })
    return nbCards;
  }

  onRemoveCard(event, card) {    
    this.deckService.removeCard(card);
  }

  onItemDrop(event) {    
    this.deckService.addCard(Card.createCard(event.dragData));
  }

  onIncrementCard(event, card) {
    this.deckService.incrementCard(card);
  }

  onDecrementCard(event, card) {
    this.deckService.decrementCard(card);
  }
}
