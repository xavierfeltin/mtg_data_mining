import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SelectDeckComponent } from './select-deck.component';
import { Observable, of } from 'rxjs';
import { DeckService } from '../deck.service';
import { Deck } from '../models/deck';
import { Mode } from '../models/mode';
import { Color } from '../models/color';
import { Card } from '../models/card';

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

describe('SelectDeckComponent', () => {
  let component: SelectDeckComponent;
  let fixture: ComponentFixture<SelectDeckComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectDeckComponent ],
      imports: [HttpClientTestingModule],
      providers: [
        {provide: DeckService, useClass: MockDeck}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectDeckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
