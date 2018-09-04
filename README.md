# Magic the gathering: Data Mining

This is an exploratory project on data mining.

The objective is to implement the concepts that may be used in a recommendation system for assisting players to build cards deck. 
Recommendations are made depending of the previously selected cards in the player's deck.

The project allows making different type of recommendations:
  - Cards with a content similar to a particular card (Latent semantic analysis)
  - Cards usually played with a particular card (Collaborative filtering)
  - Cards usually played with a set of cards (TopN recommendations)

The project is structured into different module each corresponding to a different approach. A web interface is as well developped in order to exploit the models with a concrete application. 

Important links:
  - **The wiki of this project**: https://github.com/xavierfeltin/mtg_data_mining/wiki
  - **The proof of concept (web interface)**: https://xavierfeltin.github.io/mtg_data_mining/

Technical information:
  - The scripts used to generate the recommendations is developped in Python 3.6
  - The web interface is developped in Angular 6 / Typescript

Thanks to [MTGDecks](http://mtgdecks.net) to provide sample of decks data for this project.

Special thanks to: 
  - [Guilhem Brouat](https://www.linkedin.com/in/guilhem-brouat-b09148a5/) for his mentoring on Angular
  - [Raphael Deau](https://www.linkedin.com/in/rapha%C3%ABl-deau-015a7712a/) for his feedbacks on Python
  - [Julien Zanon](https://www.linkedin.com/in/julien-zanon/) for his feedbacks on the project's content and the POC's UI
  
The web application used as proof of concept is compliant with the Fan Content policy of Wizards.

The project is under MIT License
Copyright (c) 2018 Xavier FOLCH
