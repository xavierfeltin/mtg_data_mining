import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MydeckDisplayComponent } from './mydeck-display.component';

describe('MydeckDisplayComponent', () => {
  let component: MydeckDisplayComponent;
  let fixture: ComponentFixture<MydeckDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MydeckDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MydeckDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
