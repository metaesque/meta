/**
 * @fileoverview
 */
goog.module('metax.root_test.ErrorTest');
goog.setTestOnly('metax.root_test.ErrorTest');
goog.module.declareLegacyNamespace();
const Error = goog.require('metax.root.Error');
const TestCase = goog.require('metax.test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaErrorTest} = goog.require('metax.root_test.ErrorTestMeta');

/**
 * metax.root_test.ErrorTest
 *   Auto-generated test class for metax.root.Error
 * @public
 */
class ErrorTest extends TestCase {
}
exports = ErrorTest;

var tc = new ErrorTest('metax.root_test.ErrorTest');
tc.runSelfTests();
