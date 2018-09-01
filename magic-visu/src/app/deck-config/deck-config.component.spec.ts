import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing'; 
import { RouterTestingModule } from '@angular/router/testing';

import { DeckConfigComponent } from './deck-config.component';
import { Color } from '../models/color';
import { Mode } from '../models/mode';
import { Deck } from '../models/deck';

@Component({selector: 'app-deck-form', template: ''})
class DeckFormStubComponent {
  @Input() colors: Color[];
  @Input() modes: Mode[];
  @Output()  create: EventEmitter<Deck> = new EventEmitter<Deck>();
}

describe('DeckConfigComponent', () => {
  let component: DeckConfigComponent;
  let fixture: ComponentFixture<DeckConfigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeckConfigComponent, DeckFormStubComponent ],
      imports: [HttpClientTestingModule, RouterTestingModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeckConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
