/**
 * @fileoverview
 */
goog.module('demo.cards2_test.CardTest');
goog.setTestOnly('demo.cards2_test.CardTest');
goog.module.declareLegacyNamespace();
const Card = goog.require('demo.cards2.Card');
const TestCase = goog.require('demo.cards2_test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaCardTest} = goog.require('demo.cards2_test.CardTestMeta');

/**
 * demo.cards2_test.CardTest
 *   Auto-generated test class for demo.cards2.Card
 * @public
 */
class CardTest extends TestCase {

  /**
   * demo.cards2_test.CardTest.test_constructor
   * @public
   */
  test_constructor() {
  };

  /**
   * demo.cards2_test.CardTest.test_meta
   * @public
   */
  test_meta() {
    // noop
  };
}
exports = CardTest;

var tc = new CardTest('demo.cards2_test.CardTest');
tc.runSelfTests();
