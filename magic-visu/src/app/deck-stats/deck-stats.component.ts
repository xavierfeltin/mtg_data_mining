import { Component, OnInit, ViewChild, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { Chart } from 'chart.js';
import { Card } from '../models/card';
import { LAND } from '../store/store-type';

@Component({
  selector: 'app-deck-stats',
  template: `
    <div class="hlayout">
      <div>
        <p class="information"> Mana Curve (avg: {{averageCost.toFixed(2) }}: ) </p>
        <canvas #myChart1 class="magic-chart"> {{ chart1 }} </canvas>              
      </div>
      <div>
        <p class="information"> Type Repartition: </p>
        <canvas #myChart2 class="magic-chart"> {{ chart2 }} </canvas>    
      </div>
    </div>
  `,
  styleUrls: ['./deck-stats.component.css']
})
export class DeckStatsComponent implements OnInit, OnChanges {
  @Input() cards: Card[] = [];
  @ViewChild('myChart1') private chartRef1;
  @ViewChild('myChart2') private chartRef2;
  
  chart1: Chart;
  chart2: Chart;
  averageCost: number = 0;
  private colors = [ 
  //source: https://www.rapidtables.com/web/color/RGB_Color.html
  "#4682B4", //Steel blue 
  "#FFA500", //orange
  "#32CD32", //lime green
  "#DC143C", //crimson
  "#8A2BE2", //blue violet
  "#FFE4C4", //bisque
  "#DAA520", //golden rod
  "#8B0000", //dark red
  "#3CB371", //medium sea green
  "#FA8072", //salmon
];

  constructor() { }

  ngOnInit() {
    const costs = this.serieCost;  
    this.averageCost = this.average;
    
    this.chart1 = this.addManaCurveChart(costs, this.chartRef1);
    this.chart2 = this.addTypeRepartitionChart(costs, this.chartRef2);
  }

  ngOnChanges(change: SimpleChanges) {
    if (change.cards.previousValue) {
      if (change.cards.previousValue.length != change.cards.currentValue.length) {
        this.averageCost = this.average;
        const serie = this.serieCost;
        this.updateManaCurveChart(serie);
        this.updateTypeRepartitionChart(serie);
      }
    }
  }

  get cardsbyCost() {
    let costs: {[key: string]: {[key: number]: number}} = {};        
    for(const card of this.cards) {
      if (!card.types.includes(LAND)) {
        const fullType = card.getFullType();
        if (!Object.keys(costs).includes(fullType)) {
          costs[fullType] = {};
        }

        if (!Object.keys(costs[fullType]).includes(card.manaCost.toString())) {
          costs[fullType][card.manaCost] = 1;
        }
        else {
          costs[fullType][card.manaCost] += 1;
        }
      }
    }
    return costs;
  }

  get serieCost() {      
    let repartition = this.cardsbyCost;
    
    //complete missing costs until maxCost included    
    let max = 0;
    Object.keys(repartition).forEach(type => {      
      const maxCost = Math.max(...Object.keys(repartition[type]).map(cost => Number.parseFloat(cost)));            
      if (maxCost > max) { max = maxCost; }
    });
    const range = Array.apply(null, {length: max+1}).map(Number.call, Number);

    Object.keys(repartition).forEach(type => {      
      for(const i of range) {
        if (!Object.keys(repartition[type]).includes(i.toString())) {
          repartition[type][i] = 0;
        }
      }
    })    
    return repartition;
  }

  get average() {
    const repartition = this.cardsbyCost;

    let total = 0;
    Object.keys(repartition).forEach(type => {      
      total += Object.keys(repartition[type])
                    .filter(cost => repartition[type][cost] > 0)
                    .map(cost => Number.parseFloat(cost) * repartition[type][cost])
                    .reduce((i1, i2) => i1 + i2);
    });    
    return (total == 0 ? 0 : (total / this.cards.filter(card => !card.types.includes(LAND)).length));
  }
  
  addManaCurveChart(serie: {[key: string]: {[key: number]: number}}, chartComponent: any): Chart {
    const formattedSerie = this.formatManaCurveDataset(serie);
      
    return new Chart(chartComponent.nativeElement, {
      type: 'bar',
      data: {
        labels: formattedSerie['labels'],        
        datasets: formattedSerie['dataset']
      },
      options: {
        legend: {
          position: 'right'
        },
        scales: {
          xAxes: [{
            display: true,
            stacked: true
          }],
          yAxes: [{
            display: true,
            stacked: true,
            ticks: {
              beginAtZero: true
            }
          }],
        }
      }
    });
  }

  addTypeRepartitionChart(serie: {[key: string]: {[key: number]: number}}, chartComponent: any): Chart {
    const formattedSerie = this.formatTypeRepartitionDataset(serie);
      
    return new Chart(chartComponent.nativeElement, {
      type: 'pie',
      data: {
        labels: formattedSerie['labels'],        
        datasets: formattedSerie['dataset']
      },
      options: {
        legend: {
          position: 'right'
        },
        scales: {
          xAxes: [{
            display: false
          }],
          yAxes: [{
            display: false
          }],
        }
      }
    });
  }
  
  updateManaCurveChart(serie: {[key: string]: {[key: number]: number}}) {
    const formattedSerie = this.formatManaCurveDataset(serie);    
    this.chart1.data.datasets = formattedSerie['dataset'];    
    this.chart1.data.labels = formattedSerie['labels'];
    this.chart1.update();
  }

  updateTypeRepartitionChart(serie: {[key: string]: {[key: number]: number}}) {
    const formattedSerie = this.formatTypeRepartitionDataset(serie);    
    this.chart2.data.datasets = formattedSerie['dataset'];    
    this.chart2.data.labels = formattedSerie['labels'];
    this.chart2.update();
  }

  formatManaCurveDataset(dataToFormat: {[key: string]: {[key: number]: number}}): {[key: string]: any[]} {
    let dataset = [];    
    let labels = [];
    const types = Object.keys(dataToFormat).sort();    
    
    types.forEach((type, i) => {
      let data = []
      let backgroundColors = [];
      Object.keys(dataToFormat[type]).forEach((key) => {
        if (!labels.includes(key)) {labels.push(key);}        
        data.push(dataToFormat[type][key]);
        backgroundColors.push(this.colors[i % this.colors.length]);
      });      
      dataset.push({data: data, backgroundColor: backgroundColors, label: type});
    });

    return {dataset: dataset, labels: labels};
  }

  formatTypeRepartitionDataset(dataToFormat: {[key: string]: {[key: number]: number}}): {[key: string]: any[]} {
    const types = Object.keys(dataToFormat).sort();    
    let data = []
    let backgroundColors = [];
    let labels = [...types];
    let dataset = [];          
    
    types.forEach((type, i) => {      
      let total = 0;
      Object.keys(dataToFormat[type]).forEach((key) => {
        total += dataToFormat[type][key];
      });
      data.push(total);
      backgroundColors.push(this.colors[i % this.colors.length]);      
    });
    console.log(backgroundColors);
    dataset.push({data: data, backgroundColor: backgroundColors});

    return {dataset: dataset, labels: labels};
  }
}
