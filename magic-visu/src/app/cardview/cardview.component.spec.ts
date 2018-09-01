import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { CardviewComponent } from './cardview.component';
import { NgDragDropModule } from 'ng-drag-drop';
import { Card } from '../models/card';


describe('CardviewComponent', () => {
  let component: CardviewComponent;
  let fixture: ComponentFixture<CardviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CardviewComponent ],
      imports: [
        NgDragDropModule.forRoot(), 
        RouterTestingModule]
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
