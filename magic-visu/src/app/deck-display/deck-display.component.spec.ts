import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeckDisplayComponent } from './deck-display.component';

describe('DeckDisplayComponent', () => {
  let component: DeckDisplayComponent;
  let fixture: ComponentFixture<DeckDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckDisplayComponent ]
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
