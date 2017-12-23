/**
 * @fileoverview
 */
goog.module('demo.cards2.Deck');
goog.module.declareLegacyNamespace();
const Pile = goog.require('demo.cards2.Pile');
const {MetaDeck} = goog.require('demo.cards2.DeckMeta');

/**
 * demo.cards2.Deck
 *   A pre-determined collection of Card instances.
 * @public
 */
class Deck extends Pile {

  /**
   * demo.cards2.Deck.asStr
   *   Provide a string representation of a given card.
   * @param {?demo.cards2.Card} card
   * @param {!boolean} [full=false]
   *   If true, result is '<rank> of <suit>'. If false,
   *   result is two letters.
   * @return {!string}
   * @public
   */
  asStr(card, full=false) {
    throw new Error('NotImplemented: demo.cards2.Deck.asStr');
  };

  /**
   * demo.cards2.Deck.shuffle
   *   http://wikipedia.org/wiki/Fisher-Yates_shuffle
   * @public
   */
  shuffle() {
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

  /**
   * demo.cards2.Deck.meta
   * @return {?metax.root.ObjectMetaRoot}
   * @public
   * @override 
   */
  meta() {
    return MetaDeck;
  };
}
exports = Deck;
