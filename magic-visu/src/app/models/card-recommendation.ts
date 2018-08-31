export class CardRecommendation {
    multiverseid: number;
    score: number;
    contributions: {[key: number]: number};    

    constructor(id: number, score: number, contributions: {[key: number]: number} = {}) {
        this.multiverseid = id;
        this.score = score;  
        this.contributions = contributions;      
    }
}