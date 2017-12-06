// A set of cards that partially or completely overlap.
goog.provide('demo.cards2.Pile');
goog.require('demo.cards2.Card');
goog.require('demo.cards2.Pile__Meta');
goog.require('meta.root.Object');

/**
 * demo.cards2.Pile.Pile
 * @public
 * @constructor
 * @extends {meta.root.Object}
 */
demo.cards2.Pile = function() {
  demo.cards2.Pile.base(this, 'constructor');
  self._cards = [];
  /** @type {!Array<?demo.cards2.Card>} */ this._cards;
  // User-provided code follows.
};
goog.inherits(demo.cards2.Pile, meta.root.Object);

/**
 * demo.cards2.Pile.cards/get
 * @return {!Array<?demo.cards2.Card>}
 * @public
 */
demo.cards2.Pile.prototype.cards = function() {
  return this._cards;
};

/**
 * demo.cards2.Pile.cardsIs
 * @param {!Array<?demo.cards2.Card>} value
 * @return {?demo.cards2.Pile}
 * @public
 */
demo.cards2.Pile.prototype.cardsIs = function(value) {
  this._cards = value;
  return this;
};

/**
 * demo.cards2.Pile.cardsRef
 * @return {!Array<?demo.cards2.Card>}
 * @public
 */
demo.cards2.Pile.prototype.cardsRef = function() {
  return this._cards;
};
