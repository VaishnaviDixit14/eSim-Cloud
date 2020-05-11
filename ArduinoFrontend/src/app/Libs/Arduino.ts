import { CircuitElement } from './CircuitElement';
import { Point } from './Point';

export class ArduinoUno extends CircuitElement {
  constructor(public canvas: any, x: number, y: number) {
    super('ArduinoUno', x, y, 'Arduino.json', canvas);
  }
  save() {
  }
  load(data: any): void {
  }
  getNode(x: number, y: number): Point {
    return null;
  }
  properties(): { keyName: string; id: number; body: HTMLElement; title: string; } {
    const body = document.createElement('div');
    return {
      keyName: this.keyName,
      id: this.id,
      title: 'Arduino Uno',
      body
    };
  }
  initSimulation(): void {
  }
  closeSimulation(): void {
  }
  simulate(): void {
  }

}