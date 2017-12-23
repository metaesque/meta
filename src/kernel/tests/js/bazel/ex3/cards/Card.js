goog.module('ex.cards.Card');
//goog.module.declareLegacyNamespace();

class Card {
  /**
   * Create a Card.
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

  /** 
   * @override
   * @return {!string}
   */
  toString() { return Card.Ranks[this._rank] + Card.Suits[this._suit]; }
}

Card.Suits = {
    1: 'S', 2: 'H', 3: 'C', 4: 'D'};
Card.Ranks = {
    1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'T', 11: 'J', 12: 'Q', 13: 'K'};

exports = Card;


