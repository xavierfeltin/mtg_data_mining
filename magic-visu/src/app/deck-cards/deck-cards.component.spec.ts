import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NgDragDropModule } from 'ng-drag-drop';
import { DeckCardsComponent } from './deck-cards.component';

describe('DeckCardsComponent', () => {
  let component: DeckCardsComponent;
  let fixture: ComponentFixture<DeckCardsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckCardsComponent ],
      imports: [
        NgDragDropModule.forRoot(), 
        RouterTestingModule,
        HttpClientTestingModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
