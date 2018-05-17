import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CardviewComponent } from './cardview.component';

describe('CardviewComponent', () => {
  let component: CardviewComponent;
  let fixture: ComponentFixture<CardviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CardviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CardviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
