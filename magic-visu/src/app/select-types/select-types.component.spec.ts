import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectTypesComponent } from './select-types.component';

describe('SelectTypesComponent', () => {
  let component: SelectTypesComponent;
  let fixture: ComponentFixture<SelectTypesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectTypesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectTypesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
