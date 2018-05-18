import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecommendationChildColorComponent } from './recommendation-child-color.component';

describe('RecommendationChildColorComponent', () => {
  let component: RecommendationChildColorComponent;
  let fixture: ComponentFixture<RecommendationChildColorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecommendationChildColorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecommendationChildColorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
