// A card with suit and rank, belonging to a Deck.
// 
// The Deck is responsible for display functionality.
goog.provide('demo.cards2.Card');
goog.require('demo.cards2.Card__Meta');
goog.require('demo.cards2.Deck');
goog.require('meta.root.Object');

/**
 * demo.cards2.Card.Card
 *   It should not be necessary to create Card instances directly.
 *   Instead, one should create instances of Deck, and use the cards
 *   it contains.
 * @param {?demo.cards2.Deck} deck
 * @param {!number} rank
 * @param {!number} suit
 * @public
 * @constructor
 * @extends {meta.root.Object}
 */
demo.cards2.Card = function(deck, rank, suit) {
  demo.cards2.Card.base(this, 'constructor');
  /** @type {!number} */ this._rank;
  /** @type {!number} */ this._suit;
  /** @type {?demo.cards2.Deck} */ this._deck;
  // User-provided code follows.
  this.deckIs(deck);
  this.rankIs(rank);
  this.suitIs(suit);
};
goog.inherits(demo.cards2.Card, meta.root.Object);

/**
 * demo.cards2.Card.rank/get
 * @return {!number}
 * @public
 */
demo.cards2.Card.prototype.rank = function() {
  return this._rank;
};

/**
 * demo.cards2.Card.rankIs
 * @param {!number} value
 * @return {?demo.cards2.Card}
 * @public
 */
demo.cards2.Card.prototype.rankIs = function(value) {
  this._rank = value;
  return this;
};

/**
 * demo.cards2.Card.rankRef
 * @return {!number}
 * @public
 */
demo.cards2.Card.prototype.rankRef = function() {
  return this._rank;
};

/**
 * demo.cards2.Card.suit/get
 * @return {!number}
 * @public
 */
demo.cards2.Card.prototype.suit = function() {
  return this._suit;
};

/**
 * demo.cards2.Card.suitIs
 * @param {!number} value
 * @return {?demo.cards2.Card}
 * @public
 */
demo.cards2.Card.prototype.suitIs = function(value) {
  this._suit = value;
  return this;
};

/**
 * demo.cards2.Card.suitRef
 * @return {!number}
 * @public
 */
demo.cards2.Card.prototype.suitRef = function() {
  return this._suit;
};

/**
 * demo.cards2.Card.deck/get
 * @return {?demo.cards2.Deck}
 * @public
 */
demo.cards2.Card.prototype.deck = function() {
  return this._deck;
};

/**
 * demo.cards2.Card.deckIs
 * @param {?demo.cards2.Deck} value
 * @return {?demo.cards2.Card}
 * @public
 */
demo.cards2.Card.prototype.deckIs = function(value) {
  this._deck = value;
  return this;
};

/**
 * demo.cards2.Card.deckRef
 * @return {?demo.cards2.Deck}
 * @public
 */
demo.cards2.Card.prototype.deckRef = function() {
  return this._deck;
};
