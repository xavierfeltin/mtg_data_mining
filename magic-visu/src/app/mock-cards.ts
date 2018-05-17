import {Card} from './models/card';
import {CardRecommendation} from './models/card-recommendation'
import { GameMode } from "./models/game-mode";
import { ColorCombination } from "./models/color-combination";

export const CARDS: Card[] = [
    {name: 'Pia Nalaar', multiverseid: 417697, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Abrade', multiverseid: 430772, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Magma Spray', multiverseid: 380452,contentRecommendations: [], itemRecommendations: {}},
    {name: 'Aethersphere Harvester', multiverseid: 423809, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Bomat Courier', multiverseid: 418828, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Chandra, Torch of Defiance', multiverseid: 418739, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Earthshaker Khenra', multiverseid: 431376, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Slobad, Goblin Tinkerer', multiverseid: 421803, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Pia and Kiran Nalaar', multiverseid: 442783, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Gnome-Made Engine', multiverseid: 439537, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Ravenous Intruder', multiverseid: 423761, contentRecommendations: [], itemRecommendations: {}},
    {name: 'Whirler Rogue', multiverseid: 442779, contentRecommendations: [], itemRecommendations: {}}
];

let contentRecommendations: CardRecommendation[] = [
    {card: CARDS[7], item_similarity: null, content_similarity: 0.791},
    {card: CARDS[8], item_similarity: null, content_similarity: 0.785},
    {card: CARDS[9], item_similarity: null, content_similarity: 0.782},
    {card: CARDS[10], item_similarity: null, content_similarity: 0.779},
    {card: CARDS[11], item_similarity: null, content_similarity: 0.774}
];
CARDS[0].contentRecommendations = contentRecommendations;

let itemRecommendationsStandardRed: CardRecommendation[] = [
    {card: CARDS[6], item_similarity: 0.798, content_similarity: 0.469},
    {card: CARDS[5], item_similarity: 0.785, content_similarity: 0.265}    
];
CARDS[0].itemRecommendations['standard'] = {};
CARDS[0].itemRecommendations['standard']['red'] = itemRecommendationsStandardRed;

let itemRecommendationsStandardBlackRed: CardRecommendation[] = [
    {card: CARDS[1], item_similarity: 0.898, content_similarity: 0.339},
    {card: CARDS[2], item_similarity: 0.67, content_similarity: 0.331},
    {card: CARDS[3], item_similarity: 0.639, content_similarity: 0.655},
    {card: CARDS[4], item_similarity: 0.595, content_similarity: 0.326}    
];
CARDS[0].itemRecommendations['standard']['black_red'] = itemRecommendationsStandardBlackRed;

let itemRecommendationsCommanderBlackRed: CardRecommendation[] = [
    {card: CARDS[1], item_similarity: 0.824, content_similarity: 0.339},
    {card: CARDS[6], item_similarity: 0.811, content_similarity: 0.469},
    {card: CARDS[2], item_similarity: 0.768, content_similarity: 0.331}        
];
CARDS[0].itemRecommendations['commander'] = {};
CARDS[0].itemRecommendations['commander']['black_red'] = itemRecommendationsCommanderBlackRed;