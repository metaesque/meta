// Auto-generated test class for auto-generated meta class demo.cards2.FrenchDeck__Meta
goog.setTestOnly('demo.cards2_test.FrenchDeck__MetaTest');
goog.require('demo.cards2.FrenchDeck__Meta');
goog.require('meta.testing.TestCase');

demo = demo || {};
/** @type {?Object} */ demo.cards2_test;  // find cleaner way
demo.cards2_test = demo.cards2_test || {};

/**
 * demo.cards2_test.FrenchDeck__MetaTest.FrenchDeck__MetaTest
 * @param {!string} meta__name
 * @public
 * @constructor
 * @extends {meta.testing.TestCase}
 */
demo.cards2_test.FrenchDeck__MetaTest = function(meta__name) {
  demo.cards2_test.FrenchDeck__MetaTest.base(this, 'constructor', meta__name);
  // User-provided code follows.
};
goog.inherits(demo.cards2_test.FrenchDeck__MetaTest, meta.testing.TestCase);

/**
 * demo.cards2_test.FrenchDeck__MetaTest.test_FrenchDeck__Meta
 * @public
 */
demo.cards2_test.FrenchDeck__MetaTest.prototype.test_FrenchDeck__Meta = function() {
};

var testCase = new demo.cards2_test.FrenchDeck__MetaTest('demo.cards2_test.FrenchDeck__MetaTest');
// TODO(wmh): Look into
//    $CLOSURE_ROOT/library/closure/goog-orig/testing/jsunit.js.
// We may be able to create a goog.testing.TestRunner and execute it
// without needing to include goog.testing.jsunit.  Would give us more
// control over whether tests are invoked per file or across multiple files.
//
// TODO(wmh): Determine how to access the arguments specified to
// bazel test via --test_arg within the javascript test code. The first
// arg, if provided, should be a regexp limiting which test methods get
// invoked. It should be passed as the arg to run(). For now, we provide
// a hacked solution by passing in a value to metac (which is totally
// the wrong place to be doing this!)
testCase.run();
