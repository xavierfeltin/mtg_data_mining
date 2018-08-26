import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TempMatrixComponent } from './temp-matrix.component';

describe('TempMatrixComponent', () => {
  let component: TempMatrixComponent;
  let fixture: ComponentFixture<TempMatrixComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TempMatrixComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TempMatrixComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
