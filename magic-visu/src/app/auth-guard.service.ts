import { Injectable } from '@angular/core';
import {CanActivate, Router, RouterStateSnapshot, ActivatedRouteSnapshot} from '@angular/router';
import { DeckService } from './deck.service';

@Injectable()
export class AuthGuardService implements CanActivate {

  constructor(
    private router: Router,
    private deckService: DeckService
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.deckService._deck.isUndefined()) {
        this.router.navigate(['/']);
        return false;
    }
    else {
        return true;
    }    
  }
}