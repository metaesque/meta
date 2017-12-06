// https://en.wikipedia.org/wiki/French_playing_cards
goog.provide('demo.cards2.FrenchDeck');
goog.require('demo.cards2.Card');
goog.require('demo.cards2.Deck');
goog.require('demo.cards2.FrenchDeck__Meta');

/**
 * demo.cards2.FrenchDeck.FrenchDeck
 * @param {!boolean} [jokers=false]
 *   If true, the deck includes high and low joker.
 * @public
 * @constructor
 * @extends {demo.cards2.Deck}
 */
demo.cards2.FrenchDeck = function(jokers=false) {
  demo.cards2.FrenchDeck.base(this, 'constructor');
  // User-provided code follows.
  var cards = this.cards();
  for (var suit = 1; suit < 5; ++suit) {
    for (var rank = 1; rank < 14; ++rank) {
      var card = new demo.cards2.Card(self, rank, suit);
      cards.append(card);
    }
  }
  if (jokers) {
    var lowjoker = new demo.cards2.Card(self, 0, 0);
    cards.append(lowjoker);
    var highjoker = new demo.cards2.Card(self, 14, 0);
    cards.append(highjoker);
  }
};
goog.inherits(demo.cards2.FrenchDeck, demo.cards2.Deck);

/**
 * demo.cards2.FrenchDeck.asStr
 *   Provide a string representation of a given card.
 * @param {?demo.cards2.Card} card
 * @param {!boolean} [full=false]
 *   If true, result is '<rank> of <suit>'. If false,
 *   result is two letters.
 * @return {?string}
 * @public
 * @override 
 */
demo.cards2.FrenchDeck.prototype.asStr = function(card, full=false) {
  var meta = demo.cards2.FrenchDeckClass;
  var suits = meta.Suits();
  var ranks = meta.Ranks();
  var result;
  if (full) {
    result = meta.Ranks()[card.rank()] + ' of ' + meta.Suits()[card.suit()];
  } else {
    result = meta.Ranks()[card.rank()][0] + meta.Suits()[card.suit()][0];
  }
};
