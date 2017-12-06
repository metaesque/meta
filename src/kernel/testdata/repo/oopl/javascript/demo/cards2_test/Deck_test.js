// Auto-generated test class for demo.cards2.Deck
goog.setTestOnly('demo.cards2_test.DeckTest');
goog.require('demo.cards2.Deck');
goog.require('demo.cards2_test.DeckTest__Meta');
goog.require('meta.testing.TestCase');

demo = demo || {};
/** @type {?Object} */ demo.cards2_test;  // find cleaner way
demo.cards2_test = demo.cards2_test || {};

/**
 * demo.cards2_test.DeckTest.DeckTest
 * @param {!string} meta__name
 * @public
 * @constructor
 * @extends {meta.testing.TestCase}
 */
demo.cards2_test.DeckTest = function(meta__name) {
  demo.cards2_test.DeckTest.base(this, 'constructor', meta__name);
  // User-provided code follows.
};
goog.inherits(demo.cards2_test.DeckTest, meta.testing.TestCase);

/**
 * demo.cards2_test.DeckTest.test_shuffle
 * @public
 */
demo.cards2_test.DeckTest.prototype.test_shuffle = function() {
  // According to
  //   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
  // there is no way to set the seed used by Math.random().  Big problem!
};

var testCase = new demo.cards2_test.DeckTest('demo.cards2_test.DeckTest');
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
