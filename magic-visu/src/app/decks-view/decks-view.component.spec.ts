import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DecksViewComponent } from './decks-view.component';
import { Component, Input } from '@angular/core';
import { Deck } from '../models/deck';

@Component({selector: 'app-select-deck', template: ''})
class SelectDeckStubComponent {
  @Input() selectedDeck: Deck;
}

@Component({selector: 'app-deck-display', template: ''})
class DeckDisplayStubComponent {
@Input() multiverseids: string[];
}

@Component({selector: 'app-spinner', template: ''})
class SpinnerStubComponent {}

describe('DecksViewComponent', () => {
  let component: DecksViewComponent;
  let fixture: ComponentFixture<DecksViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        DecksViewComponent, 
        SelectDeckStubComponent,
        DeckDisplayStubComponent,
        SpinnerStubComponent ],
      imports: [HttpClientTestingModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DecksViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
