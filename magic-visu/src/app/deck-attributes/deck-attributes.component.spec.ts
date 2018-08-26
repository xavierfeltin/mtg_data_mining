import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeckAttributesComponent } from './deck-attributes.component';

describe('DeckAttributesComponent', () => {
  let component: DeckAttributesComponent;
  let fixture: ComponentFixture<DeckAttributesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckAttributesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckAttributesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
