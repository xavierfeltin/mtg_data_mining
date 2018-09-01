import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Component, Input } from '@angular/core';
import { Observable, of } from 'rxjs';

import { CardService } from '../card.service';
import { DeckService } from '../deck.service';
import { ModelService } from '../model.service';
import { Card } from '../models/card';
import { Mode } from '../models/mode';
import { Deck } from '../models/deck';
import { Color } from '../models/color';
import { Model, ModelLSA, ModelTopN } from '../models/model';
import { RecommendationComponent } from './recommendation.component';

class MockCard {   
  loadCards(colors: string[], mode: string): Observable<Card[]> {
    return of([]);
  }
  cleanCache() { return; }
  getCards(filterColors: string[] = [], filterTypes: string[] = [], filterName: string = '', filterSecondaryColors: string[] = []): Observable<Card[]> {
    return of([]);
  }
  getCard(id: number): Observable<Card> {
    return of(null);
  }
  getCardsById(ids: number[], filterColors: string[] = [], filterTypes: string[] = [], filterName: string = '', filterSecondaryColors: string[] = []): Observable<Card []> {
    return of([]);
  }
}

class MockDeck {
  getDeck(): Observable<Deck>{ return of(new Deck()); }
  getCards(): Observable<Card[]> { return of([]); }
  getColors(): Color[] { return []; }
  getMode(): Mode { return new Mode(); }
  update(deck: Deck): Observable<Deck>{ return of(new Deck());}
  removeCard(card: Card) { return; }
  addCard(card: Card) { return ; }
  loadDecks(): Observable<number[][]> { return of([]); }
  getDeckAt(pos: number): Observable<number[]> { return of([]); }
  getDecksName(): Observable<string[]> { return of([]); }
  cleanCache() { return; }
}

class MockModel {
  loadLSAModel(colors: string[], mode: string): Observable<ModelLSA> {return of(new ModelLSA([],{})); }
  loadTopNModel(colors: string[], mode: string): Observable<ModelTopN> {return of(new ModelTopN([],[])); }
  cleanCache() { return; }
}

@Component({selector: 'app-cardview', template: ''})
class CardViewStubComponent {
  @Input() card: Card;
}

@Component({selector: 'app-recommendation-list', template: ''})
class RecommendationListStubComponent {
  @Input() model: Model;
  @Input() cards: Card[];
  @Input() nbRecommendations: number = 5;
  @Input() modelType: string;
}


describe('RecommendationComponent', () => {
  let component: RecommendationComponent;
  let fixture: ComponentFixture<RecommendationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        RecommendationComponent, 
        CardViewStubComponent,
        RecommendationListStubComponent ],
        imports: [RouterTestingModule, HttpClientTestingModule],
        providers: [
          {provide: CardService, useClass: MockCard},
          {provide: DeckService, useClass: MockDeck},
          {provide: ModelService, useClass: MockModel},
        ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecommendationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
