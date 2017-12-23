goog.module('ex2.cards.Card');

class Card {
  /**
   * @param {number} rank
   * @param {number} suit
   */
  constructor(rank, suit) {
    this._rank = rank;
    this._suit = suit;
  }

  /** @return {number} */
  rank() { return this._rank; }
  /** @return {number} */
  suit() { return this._suit; }
}

exports = Card;


