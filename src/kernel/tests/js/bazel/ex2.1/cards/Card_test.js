goog.module('ex2.cards.CardTest');
goog.setTestOnly('ex2.cards.CardTest');

const Card = goog.require('ex2.cards.Card');
const TestCase = goog.require('goog.testing.TestCase');

class CardTest extends TestCase {

  constructor() {
    super();
    this.card = /** @type {?Card} */ (null);
  }

  /** @override */
  setUp() {
    this.card = new Card(2, 4);
  }

  test_Card() {
    assertEquals(2, this.card.rank());
    assertEquals(4, this.card.suit());
  }

}

const testSuite = goog.require('goog.testing.testSuite');
testSuite(new CardTest());   // run all the tests.
