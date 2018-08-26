import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommendationComponent }  from './recommendation/recommendation.component';
import { CardsindexComponent } from './cardsindex/cardsindex.component';
import { DeckConfigComponent} from './deck-config/deck-config.component';
import { TempMatrixComponent } from './temp-matrix/temp-matrix.component';

const routes: Routes = [
  { path: '', component: DeckConfigComponent },
  { path: 'catalog', component: CardsindexComponent },
  { path: 'recommendation/:multiverseid', component: RecommendationComponent },
  //{ path: 'temploadmatrix', component: TempMatrixComponent },
  //{ path: '', redirectTo: '/cards', pathMatch: 'full' }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}