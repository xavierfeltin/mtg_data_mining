import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Observable, of } from 'rxjs';

import { DeckDisplayComponent } from './deck-display.component';
import { CardService } from '../card.service';
import { Type } from '../models/type';
import { Card } from '../models/card';

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

@Component({selector: 'app-select-types', template: ''})
class SelectTypeStubComponent {
  @Input() selectedType: string;
  @Input() types: Type[];
  @Output() select: EventEmitter<string> = new EventEmitter();
}

@Component({selector: 'app-input-cards', template: ''})
class InputCardStubComponent {
  @Input() defaultValue: string;
}

@Component({selector: 'app-cardsview', template: ''})
class CardsViewStubComponent {
  @Input() cards: Card[];
  @Input() nb: number;
}

describe('DeckDisplayComponent', () => {
  let component: DeckDisplayComponent;
  let fixture: ComponentFixture<DeckDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        DeckDisplayComponent, 
        SelectTypeStubComponent,
        InputCardStubComponent,
        CardsViewStubComponent ],
      imports: [HttpClientTestingModule],
      providers: [
        {provide: CardService, useClass: MockCard}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
