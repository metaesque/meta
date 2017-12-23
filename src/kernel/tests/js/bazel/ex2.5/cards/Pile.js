goog.module('ex2.cards.Pile');

const Card = goog.require('ex2.cards.Card');

class Pile {
  constructor() {
    this._cards = [];
  }

  /** @return {!Array.<?ex2.cards.Card>} */
  cards() { return this._cards; }
}

exports = Pile;
