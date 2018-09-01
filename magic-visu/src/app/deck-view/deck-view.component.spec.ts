import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Component, Input } from '@angular/core';
import { Deck } from '../models/deck';
import { Card } from '../models/card';
import { DeckViewComponent } from './deck-view.component';

@Component({selector: 'app-deck-attributes', template: ''})
class DeckAttributesStubComponent {
  @Input() deck: Deck;
}

@Component({selector: 'app-deck-cards', template: ''})
class DeckCardsStubComponent {
  @Input() cards: Card[];
}


describe('DeckViewComponent', () => {
  let component: DeckViewComponent;
  let fixture: ComponentFixture<DeckViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        DeckViewComponent, 
        DeckAttributesStubComponent, 
        DeckCardsStubComponent ],
      imports: [HttpClientTestingModule, RouterTestingModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
