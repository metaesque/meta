/**
 * @fileoverview
 */
goog.module('demo.cards2.Pile');
goog.module.declareLegacyNamespace();
const Card = goog.require('demo.cards2.Card');
const Object = goog.require('metax.root.Object');
const {MetaPile} = goog.require('demo.cards2.PileMeta');

/**
 * demo.cards2.Pile
 *   A set of cards that partially or completely overlap.
 * @public
 */
class Pile extends Object {

  /**
   * initializer
   */
  constructor() {
    super();
    this._cards = [];
    /** @type {!Array.<?demo.cards2.Card>} */ this._cards;
    // User-provided code follows.
  };

  // field cards : @vec<Card>
  //   The Card instances in this Pile

  /**
   * demo.cards2.Pile.cards/get
   * @return {!Array.<?demo.cards2.Card>}
   * @public
   */
  cards() {
    return this._cards;
  };

  /**
   * demo.cards2.Pile.cardsIs
   * @param {!Array.<?demo.cards2.Card>} value
   * @public
   */
  cardsIs(value) {
    this._cards = value;
  };

  /**
   * demo.cards2.Pile.cardsRef
   * @return {!Array.<?demo.cards2.Card>}
   * @public
   */
  cardsRef() {
    return this._cards;
  };

  /**
   * demo.cards2.Pile.meta
   * @return {?metax.root.ObjectMetaRoot}
   * @public
   * @override 
   */
  meta() {
    return MetaPile;
  };
}
exports = Pile;
