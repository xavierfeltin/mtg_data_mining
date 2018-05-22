/**
 * Utilities
 */

import { Card } from './models/card';

export function compareCardsFn(a: Card, b: Card): number {
  //order by nb colors, color, manaCost and name
  let comparison = compareColors(a, b);
  if (comparison == 0) {
    comparison = compareBy('manaCost')(a, b);
  }
  if (comparison == 0) {
    comparison = compareBy('name')(a, b);
  }
  return comparison;
};

function compareColors(a: Card, b: Card): number {
  if (a.colors.length < b.colors.length) {return -1;}
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

function compareBy(prop: keyof Card): (a: Card, b: Card) => number {
  return (a: Card, b: Card) => {
    if (a[prop] < b[prop]) {return -1;}
    if (a[prop] > b[prop]) {return 1;}
    return 0;
  };
}

export function filterColorsTypesFn(card: Card, filterColors, filterTypes): boolean {
  let keepOnColor = true;
  if (filterColors.length > 0) {
    keepOnColor = false;
    for (const color of filterColors) {
      if (card.colors.includes(color)) {
        keepOnColor = true;
        break;
      }
    }
  }

  let keepOnType = true;
  if (filterTypes.length > 0) {
    keepOnType = false;
    for (const type of filterTypes) {
      if (card.types.includes(type)) {
        keepOnType = true;
        break;
      }
    }
  }
  return keepOnColor && keepOnType;
}
