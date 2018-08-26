export class CardRecommendation {
    multiverseid: number;
    score: number;    

    constructor(id, score) {
        this.multiverseid = id;
        this.score = score;        
    }
}