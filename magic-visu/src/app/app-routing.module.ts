import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommendationComponent }  from './recommendation/recommendation.component';
import { CardsindexComponent } from './cardsindex/cardsindex.component';
import { DeckConfigComponent } from './deck-config/deck-config.component';
import { DecksViewComponent } from './decks-view/decks-view.component';
import { DeckRecommendationsComponent } from './deck-recommendations/deck-recommendations.component';
import { MydeckDisplayComponent } from './mydeck-display/mydeck-display.component';
import { AuthGuardService } from './auth-guard.service';

const routes: Routes = [
  { path: '', component: DeckConfigComponent },
  { path: 'catalog', component: CardsindexComponent,  canActivate: [AuthGuardService]},
  { path: 'mydeck', component: MydeckDisplayComponent,  canActivate: [AuthGuardService]},
  { path: 'decks', component: DecksViewComponent,  canActivate: [AuthGuardService]},
  { path: 'recommendations', component: DeckRecommendationsComponent,  canActivate: [AuthGuardService]},
  { path: 'recommendation/:multiverseid', component: RecommendationComponent, canActivate: [AuthGuardService]},  
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ],  
  providers: [AuthGuardService]
})
export class AppRoutingModule {}