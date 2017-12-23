/**
 * @fileoverview
 */
goog.module('demo.cards2_test.TestCase');
goog.module.declareLegacyNamespace();
const TestCase = goog.require('metax.test.TestCase');

class TestCase_ extends TestCase {

  // field TestVar : int

  /**
   * demo.cards2_test.TestCase.TestVar/get
   * @return {!number}
   * @public
   */
  TestVar() {
    return this._TestVar;
  };

  /**
   * demo.cards2_test.TestCase.TestVarIs
   * @param {!number} value
   * @public
   */
  TestVarIs(value) {
    this._TestVar = value;
  };

  /**
   * demo.cards2_test.TestCase.TestVarRef
   * @return {!number}
   * @public
   */
  TestVarRef() {
    return this._TestVar;
  };

  /**
   * initializer
   * @param {!string} [meta__name=""]
   */
  constructor(meta__name="") {
    super(meta__name);
    this._TestVar = 0;
    /** @type {!number} */ this._TestVar;
    // User-provided code follows.
  };

  /**
   * demo.cards2_test.TestCase.setUp
   * @public
   * @override 
   */
  setUp() {
    super.setUp();
    // User-provided code follows.
    // https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript
    // The default Javascript random number generator does not support
    // setting the seed.
    // TOOD(wmh): Implement a random number generator that supports setting
    // the seed.
  };
}
exports = TestCase_;
