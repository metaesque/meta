/**
 * @fileoverview
 */
goog.module('metax.test_test.TestCaseMetaTest');
goog.setTestOnly('metax.test_test.TestCaseMetaTest');
goog.module.declareLegacyNamespace();
const TestCase = goog.require('metax.test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {TestCaseMeta} = goog.require('metax.test.TestCaseMeta');

/**
 * metax.test_test.TestCaseMetaTest
 *   Auto-generated test class for auto-generated meta class metax.test.TestCaseMeta.
 * @public
 */
class TestCaseMetaTest extends TestCase {

  /**
   * metax.test_test.TestCaseMetaTest.test_constructor
   * @public
   */
  test_constructor() {
  };
}
exports = TestCaseMetaTest;

var tc = new TestCaseMetaTest('metax.test_test.TestCaseMetaTest');
tc.runSelfTests();
