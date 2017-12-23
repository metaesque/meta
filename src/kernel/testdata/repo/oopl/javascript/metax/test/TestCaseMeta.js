/**
 * @fileoverview
 */
goog.module('metax.test.TestCaseMeta');
goog.module.declareLegacyNamespace();
const ObjectMetaRoot = goog.require('metax.root.ObjectMetaRoot');

/**
 * metax.test.TestCaseMeta
 *   Auto-generated meta class for metax.test.TestCase.
 * @public
 */
class TestCaseMeta extends ObjectMetaRoot {

  // field Debug : bool
  //   What to initialize TestCase.debug to.

  /**
   * metax.test.TestCaseMeta.Debug/get
   * @return {!boolean}
   * @public
   */
  Debug() {
    return this._Debug;
  };

  /**
   * metax.test.TestCaseMeta.DebugIs
   * @param {!boolean} value
   * @public
   */
  DebugIs(value) {
    this._Debug = value;
  };

  /**
   * metax.test.TestCaseMeta.DebugRef
   * @return {!boolean}
   * @public
   */
  DebugRef() {
    return this._Debug;
  };

  // field InstanceCount : int
  //   Counts the number of instances created so we can assign unique ids.
  //   Useful for debugging purposes.

  /**
   * metax.test.TestCaseMeta.InstanceCount/get
   * @return {!number}
   * @public
   */
  InstanceCount() {
    return this._InstanceCount;
  };

  /**
   * metax.test.TestCaseMeta.InstanceCountIs
   * @param {!number} value
   * @public
   */
  InstanceCountIs(value) {
    this._InstanceCount = value;
  };

  /**
   * metax.test.TestCaseMeta.InstanceCountRef
   * @return {!number}
   * @public
   */
  InstanceCountRef() {
    return this._InstanceCount;
  };

  // field WriteGoldens : bool
  //   If true, methods that invoke iseqstrgold() or iseqfilegold() will
  //   update goldens instead of compare goldens.

  /**
   * metax.test.TestCaseMeta.WriteGoldens/get
   * @return {!boolean}
   * @public
   */
  WriteGoldens() {
    return this._WriteGoldens;
  };

  /**
   * metax.test.TestCaseMeta.WriteGoldensIs
   * @param {!boolean} value
   * @public
   */
  WriteGoldensIs(value) {
    this._WriteGoldens = value;
  };

  /**
   * metax.test.TestCaseMeta.WriteGoldensRef
   * @return {!boolean}
   * @public
   */
  WriteGoldensRef() {
    return this._WriteGoldens;
  };

  // field CanonicalStdout : ostream
  //   The 'normal' stdout.

  /**
   * metax.test.TestCaseMeta.CanonicalStdout/get
   * @return {?Object}
   * @public
   */
  CanonicalStdout() {
    return this._CanonicalStdout;
  };

  /**
   * metax.test.TestCaseMeta.CanonicalStdoutIs
   * @param {?Object} value
   * @public
   */
  CanonicalStdoutIs(value) {
    this._CanonicalStdout = value;
  };

  /**
   * metax.test.TestCaseMeta.CanonicalStdoutRef
   * @return {?Object}
   * @public
   */
  CanonicalStdoutRef() {
    return this._CanonicalStdout;
  };

  // field CanonicalStderr : ostream
  //   The 'normal' stderr.

  /**
   * metax.test.TestCaseMeta.CanonicalStderr/get
   * @return {?Object}
   * @public
   */
  CanonicalStderr() {
    return this._CanonicalStderr;
  };

  /**
   * metax.test.TestCaseMeta.CanonicalStderrIs
   * @param {?Object} value
   * @public
   */
  CanonicalStderrIs(value) {
    this._CanonicalStderr = value;
  };

  /**
   * metax.test.TestCaseMeta.CanonicalStderrRef
   * @return {?Object}
   * @public
   */
  CanonicalStderrRef() {
    return this._CanonicalStderr;
  };

  // field Interactive : bool
  //   Set this to True to enable interactive unit tests.      

  /**
   * metax.test.TestCaseMeta.Interactive/get
   * @return {!boolean}
   * @public
   */
  Interactive() {
    return this._Interactive;
  };

  /**
   * metax.test.TestCaseMeta.InteractiveIs
   * @param {!boolean} value
   * @public
   */
  InteractiveIs(value) {
    this._Interactive = value;
  };

  /**
   * metax.test.TestCaseMeta.InteractiveRef
   * @return {!boolean}
   * @public
   */
  InteractiveRef() {
    return this._Interactive;
  };

  /**
   * initializer
   *   Initialize class-level variables.  This includes variables for
   *   controlling golden writing, interactivity, debugging, etc, based on
   *   the value of envars.
   *   
   *   TODO(wmh): This should be added to the 'meta lifecycle' above, when
   *   support has been provided by Meta.
   * @param {!string} name
   * @param {!Array.<?Object>} bases
   * @param {!Object.<!string,?*>} symbols
   */
  constructor(name, bases, symbols) {
    super(name, bases, symbols);
    this._Debug = false;
    this._InstanceCount = 0;
    this._WriteGoldens = false;
    this._CanonicalStdout = null;
    this._CanonicalStderr = null;
    this._Interactive = false;
    /** @type {!boolean} */ this._Debug;
    /** @type {!number} */ this._InstanceCount;
    /** @type {!boolean} */ this._WriteGoldens;
    /** @type {?Object} */ this._CanonicalStdout;
    /** @type {?Object} */ this._CanonicalStderr;
    /** @type {!boolean} */ this._Interactive;
    // User-provided code follows.
    // TODO(wmh): Establish whether there is any way to emulate
    // class variables in Javascript other than adding them as
    // instance variables within the meta class.
  };
}
const MetaTestCase = new TestCaseMeta('TestCaseMeta', [], {});
exports = {MetaTestCase, TestCaseMeta};
