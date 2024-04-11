import {Shape} from './Shape.mjs';

export class Rectangle extends Shape {

  width() { return this._width; }
  height() { return this._height; }

  constructor(width, height) {
    super();
    this._width = width;
    this._height = height;
  }

  area() {
    return this.width() * this.height();
  }
}
