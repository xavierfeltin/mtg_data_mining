import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Observable, of } from 'rxjs';

import { CardsindexComponent } from './cardsindex.component';
import { CardService } from '../card.service';
import { Color } from '../models/color';
import { Type } from '../models/type';
import { Card } from '../models/card';
import { Model } from '../models/model';

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

@Component({selector: 'app-select-colors', template: ''})
class SelectColorsStubComponent {
  @Input() selectedColor: string;
  @Input() colors: Color[];
  @Output() select: EventEmitter<string> = new EventEmitter();
}

@Component({selector: 'app-select-types', template: ''})
class SelectTypeStubComponent {
  @Input() selectedType: string;
  @Input() types: Type[];
  @Output() select: EventEmitter<string> = new EventEmitter();
}

@Component({selector: 'app-input-cards', template: ''})
class InputCardsStubComponent {
  @Input() defaultValue: string;
}

@Component({selector: 'app-cardsview', template: ''})
class CardsViewStubComponent {
  @Input() cards: Card[];
}

@Component({selector: 'app-recommendation-list', template: ''})
class RecommendationListStubComponent {
  @Input() model: Model;
  @Input() cards: Card[];
  @Input() nbRecommendations: number;
  @Input() modelType: string;
}

@Component({selector: 'app-spinner', template: ''})
class SpinnerStubComponent {}

describe('CardsindexComponent', () => {
  let component: CardsindexComponent;
  let cardService: CardService;
  let fixture: ComponentFixture<CardsindexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        CardsindexComponent,
        SelectColorsStubComponent,
        SelectTypeStubComponent,
        InputCardsStubComponent,
        CardsViewStubComponent,
        RecommendationListStubComponent,
        SpinnerStubComponent
      ],
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        {provide: CardService, useClass: MockCard}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CardsindexComponent);
    cardService = TestBed.get(CardService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
