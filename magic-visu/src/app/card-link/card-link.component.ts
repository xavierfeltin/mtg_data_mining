import { Component, OnInit, Input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Card } from '../models/card';

const CARD_IMG_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=';

@Component({
  selector: 'app-card-link',
  template: `
    <a routerLink="/recommendation/{{card.multiverseid}}" [tooltip]="popTemplate" placement="right" content="body"> {{card.name}} </a>

    <ng-template #popTemplate>
      <div [innerHtml]="htmlTooltip"> </div>
    </ng-template>
  `,
  styleUrls: ['./card-link.component.css']
})
export class CardLinkComponent implements OnInit {
  @Input() card: Card = new Card();
  htmlTooltip: SafeHtml;

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.htmlTooltip = '<img src="' + this.cardUrl + '" alt="' + this.card.name + '" title="toolTip"/>';;    
  }

  get cardUrl() {
    return `${CARD_IMG_URL}${this.card.multiverseid}`;
  }
}
