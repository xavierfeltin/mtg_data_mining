import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecommendationviewComponent } from './recommendationview.component';

describe('RecommendationviewComponent', () => {
  let component: RecommendationviewComponent;
  let fixture: ComponentFixture<RecommendationviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecommendationviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecommendationviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
