import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Component, Input } from '@angular/core'
import { RecommendationListComponent } from './recommendation-list.component';
import { Card } from '../models/card';
import { CardRecommendation } from '../models/card-recommendation';

@Component({selector: 'app-recommendationview', template: ''})
class RecommendationViewStubComponent {
  @Input() recommendation: CardRecommendation;
  @Input() card: Card;
}


describe('RecommendationListComponent', () => {
  let component: RecommendationListComponent;
  let fixture: ComponentFixture<RecommendationListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecommendationListComponent, RecommendationViewStubComponent ],
      imports: [ HttpClientTestingModule ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecommendationListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
