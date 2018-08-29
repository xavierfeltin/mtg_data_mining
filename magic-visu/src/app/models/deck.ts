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

    public isUndefined() {
        return this.cards.length == 0 && this.colors.length == 0 && this.mode.name === '';
    }

    public static createDeck(colors: string[], mode: string): Deck {
        let newDeck = new Deck();

        newDeck.cards = [];    
        newDeck.colors = [];

        colors.forEach(function(color) {
            newDeck.colors.push(new Color(color));
        }, this);      
        newDeck.mode = new Mode(mode);

        return newDeck;
    }    

    public addCard(card: Card) {
        if (this.cards.indexOf(card) == -1) {this.cards = [...this.cards, card]}
    }

    public removeCard(card: Card) {
        this.cards = this.cards.filter(obj => obj.multiverseid !== card.multiverseid && obj.name !== card.name);
    }
}