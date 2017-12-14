goog.module('ex.cards_test.PileTest');
goog.setTestOnly('ex.cards_test.PileTest');

var TestCase = goog.require('goog.testing.TestCase');
var testSuite = goog.require('goog.testing.testSuite');

/** @extends TestCase */
class PileTest extends TestCase {

  /** @export */
  testMethod() {
    var a = 1;
    assertEquals(a, 1);
    console.log('In testMethod end');
  }

  /** @override */
  setUp() {
    console.log('Here!');
  }
}

var tc = new PileTest();
console.log(tc.setUp);
testSuite(tc);
