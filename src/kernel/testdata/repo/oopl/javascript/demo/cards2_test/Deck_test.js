/**
 * @fileoverview
 */
goog.module('demo.cards2_test.DeckTest');
goog.setTestOnly('demo.cards2_test.DeckTest');
goog.module.declareLegacyNamespace();
const Deck = goog.require('demo.cards2.Deck');
const TestCase = goog.require('demo.cards2_test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaDeckTest} = goog.require('demo.cards2_test.DeckTestMeta');

/**
 * demo.cards2_test.DeckTest
 *   Auto-generated test class for demo.cards2.Deck
 * @public
 */
class DeckTest extends TestCase {

  /**
   * demo.cards2_test.DeckTest.test_shuffle
   * @public
   */
  test_shuffle() {
    // According to
    //   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
    // there is no way to set the seed used by Math.random().  Big problem!
  };

  /**
   * demo.cards2_test.DeckTest.test_meta
   * @public
   */
  test_meta() {
    // noop
  };
}
exports = DeckTest;

var tc = new DeckTest('demo.cards2_test.DeckTest');
tc.runSelfTests();
