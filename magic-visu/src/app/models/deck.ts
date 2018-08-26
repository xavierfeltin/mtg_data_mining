import { Card } from "./card";
import { Color } from "./color";
import { Mode } from "./mode";

export class Deck {
    cards: Card[];
    colors: Color[];
    mode: Mode;

    constructor() {
        this.cards = [];
        this.colors = [];
        this.mode = new Mode();
    }

    public createDeck(colors: string[], mode: string) {
        this.cards = [];    
        this.colors = [];

        colors.forEach(function(color) {
            this.colors.push(new Color(color));
        }, this);      
        this.mode = new Mode(mode);
    }    

    public addCard(card: Card) {
        if (this.cards.indexOf(card) == -1) {this.cards.push(card);}
    }

    public removeCard(card: Card) {
        this.cards = this.cards.filter(obj => obj.multiverseid !== card.multiverseid && obj.name !== card.name);
    }
}