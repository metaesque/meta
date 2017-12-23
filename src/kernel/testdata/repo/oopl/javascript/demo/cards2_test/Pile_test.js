/**
 * @fileoverview
 */
goog.module('demo.cards2_test.PileTest');
goog.setTestOnly('demo.cards2_test.PileTest');
goog.module.declareLegacyNamespace();
const Pile = goog.require('demo.cards2.Pile');
const TestCase = goog.require('demo.cards2_test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaPileTest} = goog.require('demo.cards2_test.PileTestMeta');

/**
 * demo.cards2_test.PileTest
 *   Auto-generated test class for demo.cards2.Pile
 * @public
 */
class PileTest extends TestCase {

  /**
   * demo.cards2_test.PileTest.test_meta
   * @public
   */
  test_meta() {
    // noop
  };
}
exports = PileTest;

var tc = new PileTest('demo.cards2_test.PileTest');
tc.runSelfTests();
