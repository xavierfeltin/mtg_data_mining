import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { DeckFormComponent } from './deck-form.component';

describe('DeckFormComponent', () => {
  let component: DeckFormComponent;
  let fixture: ComponentFixture<DeckFormComponent>;
  
   // create new instance of FormBuilder
   const fb: FormBuilder = new FormBuilder();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckFormComponent ],
      imports: [ReactiveFormsModule],
      providers: [
        { provide: FormBuilder, useValue: fb }
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckFormComponent);
    component = fixture.componentInstance;
    
    // pass in the form dynamically
    component.formDeck = fb.group({
      deck_colors: '',      
      deck_modes: '',
    });    

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
