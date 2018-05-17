import {Card} from './models/card';
import {CardRecommendation} from './models/card-recommendation'

export const CARDS: Card[] = [
    {name: 'Pia Nalaar', multiverseid: 417697, contentRecommendations: []},
    {name: 'Abrade', multiverseid: 430772, contentRecommendations: []},
    {name: 'Magma Spray', multiverseid: 380452,contentRecommendations: []},
    {name: 'Aethersphere Harvester', multiverseid: 423809, contentRecommendations: []},
    {name: 'Bomat Courier', multiverseid: 418828, contentRecommendations: []},
    {name: 'Chandra, Torch of Defiance', multiverseid: 418739, contentRecommendations: []},
    {name: 'Earthshaker Khenra', multiverseid: 431376, contentRecommendations: []},
    {name: 'Slobad, Goblin Tinkerer', multiverseid: 421803, contentRecommendations: []},
    {name: 'Pia and Kiran Nalaar', multiverseid: 442783, contentRecommendations: []},
    {name: 'Gnome-Made Engine', multiverseid: 439537, contentRecommendations: []},
    {name: 'Ravenous Intruder', multiverseid: 423761, contentRecommendations: []},
    {name: 'Whirler Rogue', multiverseid: 442779, contentRecommendations: []}
];

let recommendations: CardRecommendation[] = [
    {card: CARDS[7], item_similarity: null, content_similarity: 0.791},
    {card: CARDS[8], item_similarity: null, content_similarity: 0.785},
    {card: CARDS[9], item_similarity: null, content_similarity: 0.782},
    {card: CARDS[10], item_similarity: null, content_similarity: 0.779},
    {card: CARDS[11], item_similarity: null, content_similarity: 0.774},
];
CARDS[0].contentRecommendations = recommendations;
