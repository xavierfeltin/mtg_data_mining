import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeckConfigComponent } from './deck-config.component';

describe('DeckConfigComponent', () => {
  let component: DeckConfigComponent;
  let fixture: ComponentFixture<DeckConfigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckConfigComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
