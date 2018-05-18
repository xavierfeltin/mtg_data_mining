import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { CardviewComponent } from './cardview/cardview.component';
import { CardsviewComponent } from './cardsview/cardsview.component';
import { AppRoutingModule } from './/app-routing.module';
import { RecommendationComponent } from './recommendation/recommendation.component';
import { RecommendationviewComponent } from './recommendationview/recommendationview.component';
import { RecommendationChildGameComponent } from './recommendation-child-game/recommendation-child-game.component';
import { RecommendationChildColorComponent } from './recommendation-child-color/recommendation-child-color.component';

@NgModule({
  declarations: [
    AppComponent,
    CardviewComponent,
    CardsviewComponent,
    RecommendationComponent,
    RecommendationviewComponent,
    RecommendationChildGameComponent,
    RecommendationChildColorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
