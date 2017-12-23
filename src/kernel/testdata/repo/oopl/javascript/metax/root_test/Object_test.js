/**
 * @fileoverview
 */
goog.module('metax.root_test.ObjectTest');
goog.setTestOnly('metax.root_test.ObjectTest');
goog.module.declareLegacyNamespace();
const Object = goog.require('metax.root.Object');
const TestCase = goog.require('metax.test.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaObjectTest} = goog.require('metax.root_test.ObjectTestMeta');

/**
 * metax.root_test.ObjectTest
 *   Auto-generated test class for metax.root.Object
 * @public
 */
class ObjectTest extends TestCase {

  /**
   * metax.root_test.ObjectTest.test_constructor
   * @public
   */
  test_constructor() {
  };

  /**
   * metax.root_test.ObjectTest.test_meta
   * @public
   */
  test_meta() {
    // noop
  };
}
exports = ObjectTest;

var tc = new ObjectTest('metax.root_test.ObjectTest');
tc.runSelfTests();
