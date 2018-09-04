import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Component, Input } from '@angular/core';
import { CardsviewComponent } from './cardsview.component';
import { NgxPaginationModule } from 'ngx-pagination';
import { Card } from '../models/card';

@Component({selector: 'app-cardview', template: ''})
class CardStubComponent {
  @Input() card: Card;
}

@Component({selector: 'app-spinner', template: ''})
class SpinnerdStubComponent {}


describe('CardsviewComponent', () => {
  let component: CardsviewComponent;
  let fixture: ComponentFixture<CardsviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        CardsviewComponent,
        CardStubComponent, 
        SpinnerdStubComponent
      ],
      imports: [NgxPaginationModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CardsviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
