import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Component, Input } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Card } from '../models/card';
import { Model, ModelLSA, ModelTopN } from '../models/model';
import { DeckRecommendationsComponent } from './deck-recommendations.component';
import { CardService } from '../card.service';

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

@Component({selector: 'app-recommendation-list', template: ''})
class RecommendationListStubComponent {
  @Input() model: Model;
  @Input() cards: Card[];
  @Input() nbRecommendations: number = 5;
  @Input() modelType: string;
}

@Component({selector: 'app-spinner', template: ''})
class SpinnerStubComponent {}

describe('DeckRecommendationsComponent', () => {
  let component: DeckRecommendationsComponent;
  let fixture: ComponentFixture<DeckRecommendationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        DeckRecommendationsComponent, 
        RecommendationListStubComponent,
        SpinnerStubComponent ],
      imports: [HttpClientTestingModule],
      providers: [
        {provide: CardService, useClass: MockCard},
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckRecommendationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
