goog.module('ex.cards.CardTest');
goog.setTestOnly('ex.cards.CardTest');

const Card = goog.require('ex.cards.Card');
var TestCase = goog.require('goog.testing.TestCase');

class CardTest extends TestCase {

  /** @param {string=} opt_name */
  constructor(opt_name) {
    super(opt_name);
    this.card = null;
  }

  /** @override */
  setUp() {
    this.card = new Card(2, 4);
  }

  test_Card() {
    assertEquals(2, this.card.rank());
    assertEquals(4, this.card.suit());
  }

  test_asStr() {
    assertEquals('2D', this.card.toString());
  }

}

var tc = new CardTest('CardTest');
var testSuite = goog.require('goog.testing.testSuite');
testSuite(tc);
