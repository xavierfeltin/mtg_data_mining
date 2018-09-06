import { Card } from "./card";
import { Color } from "./color";
import { Mode } from "./mode";
import { LAND } from "../store/store-type";

export class Deck {
    cards: Card[];
    instances: {};
    colors: Color[];
    mode: Mode;

    constructor() {
        this.cards = [];
        this.colors = [];
        this.mode = new Mode();
        this.instances = {};
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

    public addCard(newCard: Card) {
        if (this.cards.findIndex(card => card.multiverseid == newCard.multiverseid) == -1) {
            this.cards = [...this.cards, newCard];
            this.instances[newCard.multiverseid] = 1;
        }
    }

    //Add an instance of the card
    //Maximum instance is 3. Except for Commander which is 1.
    //Lands are not concerned by this restriction
    public addInstance(card: Card) {
        if (Object.keys(this.instances).includes(card.multiverseid.toString())) {
            if ((this.mode.name !== 'Commander' && this.instances[card.multiverseid] < 3)
            || card.types.includes(LAND)) {
                this.instances[card.multiverseid]++;
            }
        }
    }

    //Remove an instance of the card
    //Minimum instance is 1. User needs to delete the card itself otherwise.
    public removeInstance(card: Card) {
        if (Object.keys(this.instances).includes(card.multiverseid.toString())) {
            if (this.instances[card.multiverseid] > 1) {
                this.instances[card.multiverseid]--;
            }
        }
    }

    public removeCard(card: Card) {
        this.cards = this.cards.filter(obj => obj.multiverseid !== card.multiverseid && obj.name !== card.name);
        delete this.instances[card.multiverseid];
    }
}