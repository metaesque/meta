goog.module('metax.root_test.ObjectTest');
goog.setTestOnly('metax.root_test.ObjectTest');
goog.module.declareLegacyNamespace();

const Object = goog.require('metax.root.Object');
const TestCase = goog.require('goog.testing.TestCase');
const testSuite = goog.require('goog.testing.testSuite');
const {MetaObjectTest} = goog.require('metax.root_test.ObjectTestMeta');

/** @extends TestCase */
class ObjectTest extends TestCase {

  /**
   * @return {?metax.root.Object}
   * @public
   */
  obj() {
    return this._obj;
  }

  /** @param {string=} opt_name */
  constructor(opt_name) {
    super(opt_name);
    // console.log('Here with ' + opt_name + ' and ' + this.getName());
    this._obj = /** @type {?metax.root.Object} */ (null);
  }

  /** @override */
  setUpPage() {
    console.log('Here in setUpPage4');
  }

  /** @override */
  setUp() {
    console.log('Here in setUp\nhow does it look?');
  }

  /** @export */
  test_meta() {
    var a = 1;
    assertEquals(a, 1);
    var obj = new metax.root.Object();
    var cls = obj.meta();
    console.log('Here with ' + Object.name + ' and ' + cls.constructor.name);
    console.log('In testMethod end');
  }

  meta() {
    return MetaObjectTest;
  }
}
exports = ObjectTest;

var tc = new ObjectTest('ObjectTest');
testSuite(tc);
