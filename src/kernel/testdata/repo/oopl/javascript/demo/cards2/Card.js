/**
 * @fileoverview
 */
goog.module('demo.cards2.Card');
goog.module.declareLegacyNamespace();
const Object = goog.require('metax.root.Object');
const {MetaCard} = goog.require('demo.cards2.CardMeta');

/**
 * demo.cards2.Card
 *   A card with suit and rank.
 *   
 *   In this implementation, Card instances do not know about the Deck they
 *   belong to. See cards3.meta2 for a version in which Card maintains a Deck
 *   (this introduces a circularity, as Deck needs Card and Card needs Deck).
 * @public
 */
class Card extends Object {

  // field rank : int
  //   Rank as simple integer. Deck assigns display semantics to rank values.

  /**
   * demo.cards2.Card.rank/get
   * @return {!number}
   * @public
   */
  rank() {
    return this._rank;
  };

  /**
   * demo.cards2.Card.rankIs
   * @param {!number} value
   * @public
   */
  rankIs(value) {
    this._rank = value;
  };

  /**
   * demo.cards2.Card.rankRef
   * @return {!number}
   * @public
   */
  rankRef() {
    return this._rank;
  };

  // field suit : int
  //   Suit as simple integer. Deck assigns display semantics to suit values.

  /**
   * demo.cards2.Card.suit/get
   * @return {!number}
   * @public
   */
  suit() {
    return this._suit;
  };

  /**
   * demo.cards2.Card.suitIs
   * @param {!number} value
   * @public
   */
  suitIs(value) {
    this._suit = value;
  };

  /**
   * demo.cards2.Card.suitRef
   * @return {!number}
   * @public
   */
  suitRef() {
    return this._suit;
  };

  /**
   * initializer
   *   It should not be necessary to create Card instances directly.
   *   Instead, one should create instances of Deck, and use the cards
   *   it contains.
   * @param {!number} rank
   * @param {!number} suit
   */
  constructor(rank, suit) {
    super();
    /** @type {!number} */ this._rank;
    /** @type {!number} */ this._suit;
    // User-provided code follows.
    this.rankIs(rank);
    this.suitIs(suit);
  };

  /**
   * demo.cards2.Card.meta
   * @return {?metax.root.ObjectMetaRoot}
   * @public
   * @override 
   */
  meta() {
    return MetaCard;
  };
}
exports = Card;
