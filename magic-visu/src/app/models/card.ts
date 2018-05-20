import { CardRecommendation } from "./card-recommendation";
import { GameMode } from "./game-mode";
import { ColorCombination } from "./color-combination";

export class Card {
    multiverseid: number;
    name: string;
    manaCost: number;
    colors: string[];
    types: string[];
    contentRecommendations: CardRecommendation[];        
    itemRecommendations:{
        [key: string]: {
            [key: string]: CardRecommendation[]
        }
    }
}

/*
Example of Json:
{"multiverseid": 439680, 
"name": "Snubhorn Sentry", 
"manaCost": 1, 
"types": ["Creature"], 
"colors": ["white"], 
"contentRecommendations": [
    {"multiverseid": 439678, "contentSimilarity": 0.944, "itemSimilarity": null}, 
    {"multiverseid": 439658, "contentSimilarity": 0.185, "itemSimilarity": null}, 
    {"multiverseid": 435205, "contentSimilarity": 0.126, "itemSimilarity": null}, 
    {"multiverseid": 426736, "contentSimilarity": 0.101, "itemSimilarity": null}, 
    {"multiverseid": 435223, "contentSimilarity": 0.092, "itemSimilarity": null}], 
"itemRecommendations": 
    {"Commander": 
        {"white_blue": [
            {"multiverseid": 439678, "itemSimilarity": 1.0, "contentSimilarity": 0.944},
            {"multiverseid": 439658, "itemSimilarity": 1.0, "contentSimilarity": 0.185}, 
            {"multiverseid": 435205, "itemSimilarity": 1.0, "contentSimilarity": 0.126}, 
            {"multiverseid": 426736, "itemSimilarity": 1.0, "contentSimilarity": 0.101}, 
            {"multiverseid": 417578, "itemSimilarity": 1.0, "contentSimilarity": 0.09}]}}}
*/