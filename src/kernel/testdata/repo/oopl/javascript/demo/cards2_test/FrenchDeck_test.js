/**
 * @fileoverview
 */
goog.module('demo.cards2_test.FrenchDeckTest');
goog.setTestOnly('demo.cards2_test.FrenchDeckTest');
goog.module.declareLegacyNamespace();
const FrenchDeck = goog.require('demo.cards2.FrenchDeck');
const TestCase = goog.require('demo.cards2_test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaFrenchDeckTest} = goog.require('demo.cards2_test.FrenchDeckTestMeta');

/**
 * demo.cards2_test.FrenchDeckTest
 *   Auto-generated test class for demo.cards2.FrenchDeck
 * @public
 */
class FrenchDeckTest extends TestCase {

  /**
   * demo.cards2_test.FrenchDeckTest.test_constructor
   * @public
   */
  test_constructor() {
  };

  /**
   * demo.cards2_test.FrenchDeckTest.test_asStr
   * @public
   */
  test_asStr() {
    console.log('demo.cards2.FrenchDeck.asStr does not yet have a unittest');
  };

  /**
   * demo.cards2_test.FrenchDeckTest.test_meta
   * @public
   */
  test_meta() {
    // noop
  };
}
exports = FrenchDeckTest;

var tc = new FrenchDeckTest('demo.cards2_test.FrenchDeckTest');
tc.runSelfTests();
