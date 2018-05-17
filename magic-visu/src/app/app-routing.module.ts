import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CardsviewComponent } from './cardsview/cardsview.component'
import { RecommendationComponent }  from './recommendation/recommendation.component';

const routes: Routes = [
  { path: 'cards', component: CardsviewComponent },
  { path: 'recommendation/:multiverseid', component: RecommendationComponent },
  { path: '', redirectTo: '/cards', pathMatch: 'full' }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}