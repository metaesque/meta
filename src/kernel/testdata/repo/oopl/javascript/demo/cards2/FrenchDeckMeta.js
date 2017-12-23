/**
 * @fileoverview
 */
goog.module('demo.cards2.FrenchDeckMeta');
goog.module.declareLegacyNamespace();
const {DeckMeta} = goog.require('demo.cards2.DeckMeta');

/**
 * demo.cards2.FrenchDeckMeta
 *   Auto-generated meta class for demo.cards2.FrenchDeck.
 * @public
 */
class FrenchDeckMeta extends DeckMeta {

  // field Suits : @vec<@str>
  //   Indices are suit integers, values are suit names.

  /**
   * demo.cards2.FrenchDeckMeta.Suits/get
   * @return {!Array.<!string>}
   * @public
   */
  Suits() {
    return this._Suits;
  };

  /**
   * demo.cards2.FrenchDeckMeta.SuitsIs
   * @param {!Array.<!string>} value
   * @public
   */
  SuitsIs(value) {
    this._Suits = value;
  };

  /**
   * demo.cards2.FrenchDeckMeta.SuitsRef
   * @return {!Array.<!string>}
   * @public
   */
  SuitsRef() {
    return this._Suits;
  };

  // field Ranks : @vec<@str>
  //   Indices are suit integers, values are suit names.

  /**
   * demo.cards2.FrenchDeckMeta.Ranks/get
   * @return {!Array.<!string>}
   * @public
   */
  Ranks() {
    return this._Ranks;
  };

  /**
   * demo.cards2.FrenchDeckMeta.RanksIs
   * @param {!Array.<!string>} value
   * @public
   */
  RanksIs(value) {
    this._Ranks = value;
  };

  /**
   * demo.cards2.FrenchDeckMeta.RanksRef
   * @return {!Array.<!string>}
   * @public
   */
  RanksRef() {
    return this._Ranks;
  };

  /**
   * initializer
   * @param {!string} name
   * @param {!Array.<?Object>} bases
   * @param {!Object.<!string,?*>} symbols
   */
  constructor(name, bases, symbols) {
    super(name, bases, symbols);
    /** @type {!Array.<!string>} */ this._Suits;
    /** @type {!Array.<!string>} */ this._Ranks;
    // User-provided code follows.
    this._Suits = [
      'Joker', 'Spades', 'Diamonds', 'Clubs', 'Hearts'
    ];
    this._Ranks = [
      'Low',
      'Ace', '2', '3', '4', '5', '6', '7', '8', '9',
      'Ten', 'Jack', 'Queen', 'King',
      'High'
    ];
  };
}
const MetaFrenchDeck = new FrenchDeckMeta('FrenchDeckMeta', [], {});
exports = {MetaFrenchDeck, FrenchDeckMeta};
