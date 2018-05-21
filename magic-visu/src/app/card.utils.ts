/**
 * Utilities
 */

 import { Card } from './models/card';

export function compareCardsFn(a: Card, b: Card): number {
    //order by nb colors, color, manaCost and name
    let comparison = compareColors(a,b);
    if (comparison == 0) {
        comparison = compareManaCost(a,b);        
    }
    if (comparison == 0) {
        comparison = compareName(a,b);
    }
    return comparison;             
};

function compareColors(a: Card, b: Card): number {
    if (a.colors.length < b.colors.length){return -1;}
    else if (a.colors.length > b.colors.length) {return 1;}    
    else {
      let comparison = 0;
      const nbColors = a.colors.length;
      let i = 0;
      while (i < nbColors && comparison == 0) {
        if (a.colors[i] < b.colors[i]) {
          comparison = -1;      
        }
        else if (a.colors[i] > b.colors[i]) {
          comparison = 1;
        }
        i++;
      } 
      return comparison;     
    }       
};

function compareManaCost(a: Card, b: Card): number {
    if (a.manaCost < b.manaCost) {return -1;}
    else if (a.manaCost > b.manaCost) {return 1;}
    else return 0;
};

function compareName(a: Card, b: Card): number {
    if (a.name < b.name) {return -1;}
    else if (a.name > b.name) {return 1;}
    else return 0;
};