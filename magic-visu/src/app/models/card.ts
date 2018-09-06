export class Card {
    multiverseid: number;
    name: string;
    manaCost: number;
    colors: string[];
    types: string[];

    constructor() {
        this.multiverseid = -1;
        this.name = '';
        this.manaCost = -1;
        this.colors = [];
        this.types = [];
    }

    public getFullType(): string{
        const sortedTypes = this.types.sort();
        return sortedTypes.join(' - ');
    }

    public static createCard(data: Card): Card {
        let card = new Card();
        card.multiverseid = data.multiverseid;
        card.name = data.name;
        card.manaCost = data.manaCost;
        card.colors = [...data.colors];
        card.types = [...data.types];
        return card;
    }
}