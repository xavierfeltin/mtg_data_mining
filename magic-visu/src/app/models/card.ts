import { CardRecommendation } from "./card-recommendation";
import { GameMode } from "./game-mode";
import { ColorCombination } from "./color-combination";

export class Card {
    name: string;
    multiverseid: number;
    contentRecommendations: CardRecommendation[];        
    itemRecommendations:{
        [key: string]: {
            [key: string]: CardRecommendation[]
        }
    }    
}