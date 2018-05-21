import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CardsindexComponent } from './cardsindex.component';

describe('CardsindexComponent', () => {
  let component: CardsindexComponent;
  let fixture: ComponentFixture<CardsindexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CardsindexComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CardsindexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
