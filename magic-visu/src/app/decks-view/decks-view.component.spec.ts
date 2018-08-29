import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DecksViewComponent } from './decks-view.component';

describe('DecksViewComponent', () => {
  let component: DecksViewComponent;
  let fixture: ComponentFixture<DecksViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DecksViewComponent ]
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
