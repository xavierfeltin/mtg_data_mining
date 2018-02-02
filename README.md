# Magic the gathering: Data Mining

I am learning data mining approaches. To practice, I decided to apply them to the card based game Magic the gathering.
The objective is to realize a recommendation engine for deck building.

At the moment, the approaches integrated into this project are :
  - Identification of frequent items in existing decks
  - Generation of association rules

The code is developped in Python 3.

## Magic The Gathering
https://en.wikipedia.org/wiki/Magic:_The_Gathering

This card game is edited since 1993. Different game mode exists, the most simple is two players challenging each other through a selection of cards.
Usually, each player is playing with 60 cards called deck. At each game turn, a player has the possibility to play several cards to try to inflige damage to the other player.
First player with no more life has lost.

Each card has different charasterics such as :
  - A cost that the player has to pay to be able to play the card
  - A power and a defense score
  - Categories making the card subjects to certain game effects dedicated to some categories
  - Special rules described in a text from a few words to several lines

## Data Mining and Magic The Gathering
Since 1993, this game has published around 19 000 cards across different editions. This game is played by thousands and thousands of players across the world. A lot of tournaments are occuring regularly as well.

A deck is built based on the different characteristics of the cards available to the player (some cards may be really expensive). A player is looking for selecting 60 cards that have synergies between them in order to build interesting combinations during games.

The process of building a deck asks of the player to know the game mechanics and a lot of cards (his and others that can be opposed to him).
From my point of view, data mining may have a role to play in this context. One idea is to build a recommendation engine to suggest cards to the player from cards that he has already selected.

## Global approach
The chosen approach is based on the identification of frequent cards used in existing decks. Then, rules are produced based on the frequent cards combinations.
These rules will be used to produce recommendations to the player. More steps to improve the recommendations may come later.

Two approaches are implemented to identify frequent cards among several existing decks:
  - Apriori (https://en.wikipedia.org/wiki/Apriori_algorithm)
  - FPGrowth (https://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Frequent_Pattern_Mining/The_FP-Growth_Algorithm)
  
The association rules generation is based on an algorithm based on the Apriori approach.
In order to exploit the FPGrowth results, I transformed the FPGrowth output so they may be used by the Apriori association rules function.

## First results
At the moment, the input data are 97 000 decks from Magic the gathering tournaments. 
The frequent card sets and rules generated from Apriori and FPgrowth are relevant to build consistent decks. The rules suggest common cards for classic deck building approaches (mono color decks, specialized decks, ...)

However, in this game, players look for high value combinations. These combinations bring to the deck a huge victory potential (globally or againt specific decks).
These combinations even if they are present in existing decks are difficult to make appear in rules. This is due to the high use of really common cards across decks. These cards are by nature really frequent and tend to diluate specific combinations played more in specific cases.

I have been able to make appear such a combination by extracting from the data common played cards (present more than 10% across all the decks).
This combination take advantage of the special rule of each card to give bonuses on the overall : 
  - Goblin King (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=150140)
  - Gempalm incinerator (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=166949)
  - Goblin Matron (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=184247)
  - Goblin Warchief (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=166197)
  - Goblin Piledriver (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=399645)
  - Goblin Ringleader (http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=179146)

## Next developments
Due to its better computing performance, the main approach for frequent card set identification will be FPGrowth.
The next developments will try to complete/improve the current implementation of this approach (memory usage, reducing non-pertinent and redundant generated rules, ...) 

## Other developments
A file is dedicated to encode cards into a vector of descriptors. I used LSA (Latent Semantic Analysis) for this purpose.
This encoding is not yet used in this project but it may be come handy in the future.

## Resources
Data-Mining:
  - Machine Learning In Action, Peter Harrington, Manning, 2012
  - http://www.borgelt.net

Apriori:
  - http://aimotion.blogspot.fr/2013/01/machine-learning-and-data-mining.html
  - https://www.kdnuggets.com/2016/04/association-rules-apriori-algorithm-tutorial.html
  - http://data-mining.philippe-fournier-viger.com/how-to-auto-adjust-the-minimum-support-threshold-according-to-the-data-size/

FPGrowth:
    - http://blog.khaledtannir.net/2012/07/lalgorithme-fp-growth-les-bases-13/
    - https://www.singularities.com/blog/2015/08/apriori-vs-fpgrowth-for-frequent-item-set-mining
    - http://www.borgelt.net/doc/fpgrowth/fpgrowth.html

Association rules:
  - https://en.wikipedia.org/wiki/Lift_(data_mining)

LSA (Latent Semantic Analysis):
  - http://www.datascienceassn.org/sites/default/files/users/user1/lsa_presentation_final.pdf
  - https://machinelearningmastery.com/clean-text-machine-learning-python/
