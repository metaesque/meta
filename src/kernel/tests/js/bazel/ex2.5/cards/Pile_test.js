goog.module('ex2.cards.PileTest');
goog.setTestOnly('ex2.cards.PileTest');

const Pile = goog.require('ex2.cards.Pile');
const TestCase = goog.require('goog.testing.TestCase');

class PileTest extends TestCase {

  constructor() {
    super();
    this.pile = /** @type {?Pile} */ (null);
  }

  /** @override */
  setUp() {
    this.pile = new Pile();
  }

  test_Pile() {
    console.log('Here');
  }

}

const testSuite = goog.require('goog.testing.testSuite');
testSuite(new PileTest());   // run all the tests.
