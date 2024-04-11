export class Shape {
  constructor() {
  }

  area() {
    throw new Error("Shape.area must be implemented by subclasses.");
  }
};
