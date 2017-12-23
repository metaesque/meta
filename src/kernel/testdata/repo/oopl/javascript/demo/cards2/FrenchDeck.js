/**
 * @fileoverview
 */
goog.module('demo.cards2.FrenchDeck');
goog.module.declareLegacyNamespace();
const Card = goog.require('demo.cards2.Card');
const Deck = goog.require('demo.cards2.Deck');
const {MetaFrenchDeck} = goog.require('demo.cards2.FrenchDeckMeta');

/**
 * demo.cards2.FrenchDeck
 *   https://en.wikipedia.org/wiki/French_playing_cards
 * @public
 */
class FrenchDeck extends Deck {

  /**
   * initializer
   * @param {!boolean} [jokers=false]
   *   If true, the deck includes high and low joker.
   */
  constructor(jokers=false) {
    super();
    // User-provided code follows.
    var cards = this.cards();
    for (var suit = 1; suit < 5; ++suit) {
      for (var rank = 1; rank < 14; ++rank) {
        var card = new Card(rank, suit);
        cards.push(card);
      }
    }
    if (jokers) {
      var lowjoker = new Card(0, 0);
      cards.push(lowjoker);
      var highjoker = new Card(14, 0);
      cards.push(highjoker);
    }
  };

  /**
   * demo.cards2.FrenchDeck.asStr
   *   Provide a string representation of a given card.
   *   
   * @param {?demo.cards2.Card} card
   * @param {!boolean} [full=false]
   *   If true, result is '<rank> of <suit>'. If false,
   *   result is two letters.
   * @return {!string}
   *     Testing to see how things work.
   * @public
   * @override 
   * @suppress {reportUnknownTypes}
   */
  asStr(card, full=false) {
    var meta = MetaFrenchDeck;  /** TODO(wmh): Get this.meta() working */
    var suits = meta.Suits();
    var ranks = meta.Ranks();
    var result;
    if (full) {
      result = ranks[card.rank()] + ' of ' + suits[card.suit()];
    } else {
      result = ranks[card.rank()][0] + suits[card.suit()][0];
    }
    return result;
  };

  /**
   * demo.cards2.FrenchDeck.meta
   * @return {?metax.root.ObjectMetaRoot}
   * @public
   * @override 
   */
  meta() {
    return MetaFrenchDeck;
  };
}
exports = FrenchDeck;
