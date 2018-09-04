import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'; 
import { ReactiveFormsModule } from '@angular/forms';

import {NgxPaginationModule} from 'ngx-pagination'; //https://github.com/michaelbromley/ngx-pagination
import { NgDragDropModule } from 'ng-drag-drop';
import { TooltipModule } from 'ngx-bootstrap/tooltip';

import { AppComponent } from './app.component';
import { CardviewComponent } from './cardview/cardview.component';
import { CardsviewComponent } from './cardsview/cardsview.component';
import { AppRoutingModule } from './/app-routing.module';
import { RecommendationComponent } from './recommendation/recommendation.component';
import { RecommendationviewComponent } from './recommendationview/recommendationview.component';
import { SelectColorsComponent } from './select-colors/select-colors.component';
import { CardsindexComponent } from './cardsindex/cardsindex.component';
import { SelectTypesComponent } from './select-types/select-types.component';
import { SelectModeComponent } from './select-mode/select-mode.component';
import { SpinnerComponent } from './spinner/spinner.component';
import { InputCardsComponent } from './input-cards/input-cards.component';
import { DeckViewComponent } from './deck-view/deck-view.component';
import { DeckConfigComponent } from './deck-config/deck-config.component';
import { DeckFormComponent } from './deck-form/deck-form.component';
import { DeckAttributesComponent } from './deck-attributes/deck-attributes.component';
import { RecommendationListComponent } from './recommendation-list/recommendation-list.component';
import { DeckCardsComponent } from './deck-cards/deck-cards.component';
import { DeckDisplayComponent } from './deck-display/deck-display.component';
import { DecksViewComponent } from './decks-view/decks-view.component';
import { SelectDeckComponent } from './select-deck/select-deck.component';
import { CardLinkComponent } from './card-link/card-link.component';
import { DeckRecommendationsComponent } from './deck-recommendations/deck-recommendations.component';

@NgModule({
  declarations: [
    AppComponent,
    CardviewComponent,
    CardsviewComponent,
    RecommendationComponent,
    RecommendationviewComponent,    
    SelectColorsComponent,
    CardsindexComponent,
    SelectTypesComponent,
    SelectModeComponent,
    SpinnerComponent,
    InputCardsComponent,    
    DeckViewComponent, 
    DeckConfigComponent,
    DeckFormComponent, 
    DeckAttributesComponent, 
    RecommendationListComponent, 
    DeckCardsComponent, 
    DeckDisplayComponent, 
    DecksViewComponent, 
    SelectDeckComponent, CardLinkComponent, DeckRecommendationsComponent    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxPaginationModule,
    ReactiveFormsModule,
    NgDragDropModule.forRoot(),
    TooltipModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
