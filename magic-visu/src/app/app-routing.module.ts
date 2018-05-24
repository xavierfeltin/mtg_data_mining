import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommendationComponent }  from './recommendation/recommendation.component';
import { CardsindexComponent } from './cardsindex/cardsindex.component';

const routes: Routes = [
  { path: '', component: CardsindexComponent },
  { path: 'recommendation/:multiverseid', component: RecommendationComponent },
  //{ path: '', redirectTo: '/cards', pathMatch: 'full' }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}