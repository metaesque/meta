// A pre-determined collection of Card instances.
goog.provide('demo.cards2.Deck');
goog.require('demo.cards2.Deck__Meta');
goog.require('demo.cards2.Pile');

/**
 * demo.cards2.Deck.Deck
 * @public
 * @constructor
 * @extends {demo.cards2.Pile}
 */
demo.cards2.Deck = function() {
  demo.cards2.Deck.base(this, 'constructor');
  // User-provided code follows.
};
goog.inherits(demo.cards2.Deck, demo.cards2.Pile);

/**
 * demo.cards2.Deck.asStr
 *   Provide a string representation of a given card.
 * @param {?demo.cards2.Card} card
 * @return {?string}
 * @public
 */
demo.cards2.Deck.prototype.asStr = function(card) {
  return null;
};

/**
 * demo.cards2.Deck.shuffle
 *   http://wikipedia.org/wiki/Fisher-Yates_shuffle
 * @public
 */
demo.cards2.Deck.prototype.shuffle = function() {
  var cards = this.cards();
  var n = cards.length;
  for (var i = 0; i < n; ++i) {
    // 0 <= j <= i
    var j = Math.floor(Math.random() * (i+1));
    var tmp = cards[j];
    cards[j] = cards[i];
    cards[i] = tmp;
  }
};
