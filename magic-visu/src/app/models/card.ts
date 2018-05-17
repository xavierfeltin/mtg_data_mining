import { CardRecommendation } from "./card-recommendation";

export class Card {
    name: string;
    multiverseid: number;
    contentRecommendations: CardRecommendation[];    
    /*
    item_recommendations:{
        [key: GameMode]: {
            [key: ColorCombination]: CardRecommendation[]
        }
    },
    */
}