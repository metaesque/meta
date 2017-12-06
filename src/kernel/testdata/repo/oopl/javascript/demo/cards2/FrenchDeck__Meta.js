// Auto-generated meta class for demo.cards2.FrenchDeck
goog.provide('demo.cards2.FrenchDeck__Meta');
goog.require('demo.cards2.Deck__Meta');

/**
 * demo.cards2.FrenchDeck__Meta.FrenchDeck__Meta
 * @public
 * @constructor
 * @extends {demo.cards2.Deck__Meta}
 */
demo.cards2.FrenchDeck__Meta = function() {
  demo.cards2.FrenchDeck__Meta.base(this, 'constructor');
  /** @type {?Array<?string>} */ this._Suits;
  /** @type {?Array<?string>} */ this._Ranks;
  // User-provided code follows.
  meta.SuitsIs(
    ['Joker', 'Spades', 'Diamonds', 'Clubs', 'Hearts']);
  meta.RanksIs([
    'Low',
    'Ace', '2', '3', '4', '5', '6', '7', '8', '9',
    'Ten', 'Jack', 'Queen', 'King',
    'High']);
};
goog.inherits(demo.cards2.FrenchDeck__Meta, demo.cards2.Deck__Meta);

/**
 * demo.cards2.FrenchDeck__Meta.Suits/get
 * @return {?Array<?string>}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.Suits = function() {
  return this._Suits;
};

/**
 * demo.cards2.FrenchDeck__Meta.SuitsIs
 * @param {?Array<?string>} value
 * @return {?demo.cards2.FrenchDeck__Meta}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.SuitsIs = function(value) {
  this._Suits = value;
  return this;
};

/**
 * demo.cards2.FrenchDeck__Meta.SuitsRef
 * @return {?Array<?string>}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.SuitsRef = function() {
  return this._Suits;
};

/**
 * demo.cards2.FrenchDeck__Meta.Ranks/get
 * @return {?Array<?string>}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.Ranks = function() {
  return this._Ranks;
};

/**
 * demo.cards2.FrenchDeck__Meta.RanksIs
 * @param {?Array<?string>} value
 * @return {?demo.cards2.FrenchDeck__Meta}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.RanksIs = function(value) {
  this._Ranks = value;
  return this;
};

/**
 * demo.cards2.FrenchDeck__Meta.RanksRef
 * @return {?Array<?string>}
 * @public
 */
demo.cards2.FrenchDeck__Meta.prototype.RanksRef = function() {
  return this._Ranks;
};
