import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NgDragDropModule } from 'ng-drag-drop';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { RecommendationviewComponent } from './recommendationview.component';
import { Observable, of } from 'rxjs';
import { CardService } from '../card.service';
import { Card } from '../models/card';

class MockCard {   
  loadCards(colors: string[], mode: string): Observable<Card[]> {
    return of([]);
  }
  cleanCache() { return; }
  getCards(filterColors: string[] = [], filterTypes: string[] = [], filterName: string = '', filterSecondaryColors: string[] = []): Observable<Card[]> {
    return of([]);
  }
  getCard(id: number): Observable<Card> {
    return of(null);
  }
  getCardsById(ids: number[], filterColors: string[] = [], filterTypes: string[] = [], filterName: string = '', filterSecondaryColors: string[] = []): Observable<Card []> {
    return of([]);
  }
}

describe('RecommendationviewComponent', () => {
  let component: RecommendationviewComponent;
  let fixture: ComponentFixture<RecommendationviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecommendationviewComponent ],
      imports: [ 
        NgDragDropModule.forRoot(), 
        RouterTestingModule,
        HttpClientTestingModule],
        providers: [
          {provide: CardService, useClass: MockCard}
        ]
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
