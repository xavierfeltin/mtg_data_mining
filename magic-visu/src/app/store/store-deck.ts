import { Card } from "../models/card";
import { Deck } from "../models/deck";
import { COLORS } from "./store-color";
import { MODES } from "./store-mode";

const card1: Card = {
    multiverseid: 401824,
    name: 'card 1',
    manaCost: 1,
    colors: [COLORS[0].name],
    types: [MODES[0].name] /*,
    contentRecommendations: [],
    itemRecommendations: {}*/
};

const card2: Card = {
    multiverseid: 201563,
    name: 'card 2',
    manaCost: 1,
    colors: [COLORS[0].name],
    types: [MODES[1].name]/*,
    contentRecommendations: [],
    itemRecommendations: {}*/
};

const card3: Card = {
    multiverseid: 228959,
    name: 'card 3',
    manaCost: 1,
    colors: [COLORS[0].name],
    types: [MODES[2].name]/*,
    contentRecommendations: [],
    itemRecommendations: {}*/
};

export const DECK: Deck = new Deck();
DECK.cards = [card1, card2, card3];
DECK.colors = [COLORS[0], COLORS[1]];
DECK.mode = MODES[0];