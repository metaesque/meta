goog.module('ex.cards_test.CardTest');
goog.setTestOnly('ex.cards_test.CardTest');

const Card = goog.require('ex.cards.Card');

var TestCase = goog.require('goog.testing.TestCase');
var testSuite = goog.require('goog.testing.testSuite');

/** @extends TestCase */
class CardTest extends TestCase {
  /** @param {string=} opt_name */
  constructor(opt_name) {
    super(opt_name);
    // console.log('Here with ' + opt_name + ' and ' + this.getName());

    /** @type {?Card} */ this.card = null;
  }

  /** @override */
  setUpPage() {
    console.log('Here in setUpPage');
  }

  /** @override */
  setUp() {
    console.log('Here in setUp\nhow does it look?');
    this.card = new Card(null, 2, 2);
  }

  /** @export */
  testMethod() {
    var a = 1;
    assertEquals(a, 1);
    console.log('In testMethod end');
  }

  /** @export */
  testMethod2() {
    var a = this.card.val;
    assertEquals(a, 1);
    this.card.val = 10;
    assertEquals(this.card.val, 10);
    console.log('In testMethod2 end');
  }

}

var tc = new CardTest('CardTest');
testSuite(tc);
