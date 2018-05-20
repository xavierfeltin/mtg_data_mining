import {Card} from './models/card';
import {CardRecommendation} from './models/card-recommendation'
import { GameMode } from "./models/game-mode";
import { ColorCombination } from "./models/color-combination";

export const CARDS: Card[] = [
    {name: 'Pia Nalaar', multiverseid: 417697, manaCost: 0, colors: [], types:[], contentRecommendations: [], itemRecommendations: {}},
    {name: 'Abrade', multiverseid: 430772, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Magma Spray', multiverseid: 380452, manaCost: 0, colors: [], types:[], contentRecommendations: [], itemRecommendations: {}},
    {name: 'Aethersphere Harvester', multiverseid: 423809, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Bomat Courier', multiverseid: 418828, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Chandra, Torch of Defiance', multiverseid: 418739, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Earthshaker Khenra', multiverseid: 431376, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Slobad, Goblin Tinkerer', multiverseid: 421803, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Pia and Kiran Nalaar', multiverseid: 442783, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Gnome-Made Engine', multiverseid: 439537, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Ravenous Intruder', multiverseid: 423761, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}},
    {name: 'Whirler Rogue', multiverseid: 442779, manaCost: 0, colors: [], types:[],  contentRecommendations: [], itemRecommendations: {}}
];

let contentRecommendations: CardRecommendation[] = [
    {multiverseid: CARDS[7].multiverseid, itemSimilarity: null, contentSimilarity: 0.791},
    {multiverseid: CARDS[8].multiverseid, itemSimilarity: null, contentSimilarity: 0.785},
    {multiverseid: CARDS[9].multiverseid, itemSimilarity: null, contentSimilarity: 0.782},
    {multiverseid: CARDS[10].multiverseid, itemSimilarity: null, contentSimilarity: 0.779},
    {multiverseid: CARDS[11].multiverseid, itemSimilarity: null, contentSimilarity: 0.774}
];
CARDS[0].contentRecommendations = contentRecommendations;

let itemRecommendationsStandardRed: CardRecommendation[] = [
    {multiverseid: CARDS[6].multiverseid, itemSimilarity: 0.798, contentSimilarity: 0.469},
    {multiverseid: CARDS[5].multiverseid, itemSimilarity: 0.785, contentSimilarity: 0.265}    
];
CARDS[0].itemRecommendations['standard'] = {};
CARDS[0].itemRecommendations['standard']['red'] = itemRecommendationsStandardRed;

let itemRecommendationsStandardBlackRed: CardRecommendation[] = [
    {multiverseid: CARDS[1].multiverseid, itemSimilarity: 0.898, contentSimilarity: 0.339},
    {multiverseid: CARDS[2].multiverseid, itemSimilarity: 0.67, contentSimilarity: 0.331},
    {multiverseid: CARDS[3].multiverseid, itemSimilarity: 0.639, contentSimilarity: 0.655},
    {multiverseid: CARDS[4].multiverseid, itemSimilarity: 0.595, contentSimilarity: 0.326}    
];
CARDS[0].itemRecommendations['standard']['black_red'] = itemRecommendationsStandardBlackRed;

let itemRecommendationsCommanderBlackRed: CardRecommendation[] = [
    {multiverseid: CARDS[1].multiverseid, itemSimilarity: 0.824, contentSimilarity: 0.339},
    {multiverseid: CARDS[6].multiverseid, itemSimilarity: 0.811, contentSimilarity: 0.469},
    {multiverseid: CARDS[2].multiverseid, itemSimilarity: 0.768, contentSimilarity: 0.331}        
];
CARDS[0].itemRecommendations['commander'] = {};
CARDS[0].itemRecommendations['commander']['black_red'] = itemRecommendationsCommanderBlackRed;