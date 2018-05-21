import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectColorsComponent } from './select-colors.component';

describe('SelectColorsComponent', () => {
  let component: SelectColorsComponent;
  let fixture: ComponentFixture<SelectColorsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectColorsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectColorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
