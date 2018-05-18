import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecommendationChildGameComponent } from './recommendation-child-game.component';

describe('RecommendationChildGameComponent', () => {
  let component: RecommendationChildGameComponent;
  let fixture: ComponentFixture<RecommendationChildGameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecommendationChildGameComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecommendationChildGameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
