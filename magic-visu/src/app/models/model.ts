import { Card } from "./card";
import { CardRecommendation } from "./card-recommendation";

export abstract class Model {
    cards: number[];
    coefficients: any;
    public abstract getRecommendations(cards: Card[], nbRecommendations: number): CardRecommendation[];
}

export class ModelLSA extends Model {
    cards: number[];
    coefficients: {[key: string]: number[]};

    constructor(cards: number[], coefficients: {[key: string]: number[]}) {    
        super();    
        this.cards = [...cards];
        this.coefficients = {};
        for(const multiverseid of Object.keys(coefficients)){
            this.coefficients[multiverseid] = [...coefficients[multiverseid]];
        }        
    }

    public getRecommendations(cards: Card[], nbRecommendations: number): CardRecommendation[] {
        let recommendations = [];
        const card = cards[0];
        const card_coeff = this.coefficients[card.multiverseid];
        const nbCoefficients = card_coeff.length;

        for(const elt of this.cards) {
            if (elt !== card.multiverseid) {
                const elt_coeff = this.coefficients[elt];
                let result = 0.0;
                
                for(let i = 0; i < nbCoefficients; i++) {
                    result += card_coeff[i] * elt_coeff[i];
                }

                //TODO: check if keeping a sorted array with nbRecommendations elements
                //is faster than keeping all recmmendations and sorting before returning results
                recommendations.push(new CardRecommendation(elt,result));
                recommendations.sort((n1,n2) => n2.score - n1.score);

                if (recommendations.length > nbRecommendations) {
                    recommendations.pop();
                }
            }
        }
        return recommendations;
    }
}

export class ModelTopN extends Model {
    cards: number[];
    coefficients: number[][];

    constructor(cards: number[], coefficients: number[][]) {     
        super();   
        this.cards = [...cards];
        this.coefficients = [];
        const nbColumns = coefficients.length;
        for (let i = 0; i < nbColumns; i++) {
            this.coefficients.push([...coefficients[i]]);
        }        
    }

    public getRecommendations(cards: Card[], nbRecommendations: number): CardRecommendation[] {
        const nbRows = this.coefficients.length; //square matrix
        let recommendations = [];
        let indexes = []

        if (cards.length == 0) {
            return recommendations;
        }
        
        for(const card of cards) {
            const indexCard = this.cards.findIndex(function(value, index, array) { return value == card.multiverseid});
            indexes.push(indexCard);
        }
        
        let results = [];
        let indexResults = [];
        for(let i = 0; i < nbRows; i++) {
            if (!indexes.includes(i)) {
                let coeff = 0.0;
                for(const indexCard of indexes) {
                    coeff += this.coefficients[i][indexCard];
                }

                if(results.length < nbRecommendations || coeff > results[results.length -1]) {
                    const indexToInsert = this.findIndexToInsert(results, coeff);
                    results = this.insertData(results, coeff, indexToInsert);
                    indexResults = this.insertData(indexResults, i, indexToInsert);                    
                }

                if(results.length > nbRecommendations) {
                    results.pop();
                    indexResults.pop();
                }
            }
        }

        const maxLength = results.length;
        for (let i = 0; i < maxLength; i++) {
            recommendations.push(new CardRecommendation(this.cards[indexResults[i]], results[i]));
        }
        
        return recommendations;     
    }

    public findIndexToInsert(arr, value) {
        let i = 0;
        let j = arr.length;
        let mid = 0;

        if (arr.length == 0) {
            return 0;
        }
        else if (value < arr[arr.length-1]) {
            return arr.length;
        }
        else if (value >= arr[0]) {
            return 0;
        }
        else {
            let found = false;
            while (!found) {
                mid = ((i+j)%2 == 0) ? (i+j)/2 : (i+j-1) / 2;

                if(arr[mid] >= value && value > arr[mid+1]) {
                    found = true
                }
                else if (value > arr[mid])  {
                    j = mid;
                }
                else {
                    i = mid;
                }
            }
    
            return mid +1;
        }
    }

    public insertData(arr, value, pos) {
        return [...arr.slice(0, pos),value, ...arr.slice(pos, arr.length)];
    }
}