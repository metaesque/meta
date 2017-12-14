goog.module('ex.cards.Pile');

/** @class */
class Pile {
  constructor() {
    this._cards = [];
  }

  /** @return {Array.<Card>} */
  cards() {
    return this._cards;
  }

  /** 
   * @param {Array.<Card>} value
   * @return {!Pile}
   */
  cardsIs(value) {
    this._cards = value;
    return this;
  }

}

exports = Pile;
