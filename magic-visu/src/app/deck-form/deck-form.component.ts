import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Color } from '../models/color';
import { Mode } from '../models/mode';
import { Deck } from '../models/deck';

@Component({
  selector: 'app-deck-form',
  template: `
    <form [formGroup]="formDeck" (ngSubmit)="onSubmit(formDeck)">
      <fieldset formGroupName="deck_colors">
        <legend> Colors </legend>        
            <div *ngFor="let color of colors;">
              <input type="checkbox" [formControlName]="color.name"/>
              <label [for]="color.name">{{color.name}}</label>
            </div>        
        </fieldset>

        <fieldset>
        <legend> Mode </legend>
          <div *ngFor="let mode of modes; let i = index;">                        
            <input type="radio" formControlName="deck_modes" [value]="mode.name" [checked]="i==0"/>
            <label [for]="mode.name">{{mode.name}}</label>
          </div>        
        </fieldset>
    
      <div class="full-width"> 
        <button type="submit"> Create </button>
      </div>
    </form>
  `,
  styleUrls: ['./deck-form.component.css']
})
export class DeckFormComponent implements OnInit {
  @Input() colors: Color[];
  @Input() modes: Mode[];
  @Output()  create: EventEmitter<Deck> = new EventEmitter<Deck>();

  formDeck: FormGroup;  

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.formDeck = this.fb.group({
      deck_colors: this.fb.group({}),      
      deck_modes: this.modes[0].name,
    });    

    this.colors.forEach(color => {
      (this.formDeck.controls.deck_colors as FormGroup).addControl(color.name, this.fb.control(false))
    }); 
  }

  onSubmit(form: FormGroup) {
    const colors: string[] = Object
		  .keys(form.value.deck_colors)
		  .filter(color => form.value.deck_colors[color]);
    
    let deck = new Deck();
    deck.createDeck(colors, form.value.deck_modes);
    this.create.emit(deck);
  }
}
