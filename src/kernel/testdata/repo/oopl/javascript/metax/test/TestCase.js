/**
 * @fileoverview
 */
goog.module('metax.test.TestCase');
goog.module.declareLegacyNamespace();
const PropertyReplacer = goog.require('goog.testing.PropertyReplacer');
const TestCase = goog.require('goog.testing.TestCase');
const TestRunner = goog.require('goog.testing.TestRunner');
const {MetaTestCase} = goog.require('metax.test.TestCaseMeta');
goog.require('goog.asserts');
goog.require('goog.testing.asserts');

/**
 * metax.test.TestCase
 *   The JUnit testing infrastructure for Java (which came from a testing
 *   infrastructure for Smalltalk) has gained cross-language recognition, and
 *   there is an xUnit implementation for basically every OO language
 *   (e.g. CppUnit, JSUnit, python unit (unittest), etc.).
 *   
 *   See $METAROOT/UseGuide.wmd (/Meta/Meta From The Middle Ground/Unit Tests)
 *   for a discussion of xUnit and how Meta implements this testing paradigm
 *   across all baselangs.
 *   
 *   See the src/kernel/asserts.org file for details on alerts across
 *   baselangs.
 *   
 *   In javascript, the normal idiom for doing javascript testing using
 *   bazel and google closure is as follows:
 *    - unittests are implemented in some file ending in _test.js
 *    - the file must goog.require('goog.testing.jsunit'), which:
 *       - creates cached G_testRunner (if G_testRunner already exists, noop)
 *       - creates a window.onerror handler to report errors during test
 *         initialization
 *       - creates a window.onload handler so that when the page containing
 *         the *_test.js file is loaded:
 *          - invokes any already specified onload code
 *          - creates a timeout to execute the following after 500ms
 *            - if G_testRunner is not yet initialized:
 *               - create a TestCase instance 'testCase'
 *               - invoke goog.testing.TestCase.initializeTestRunner(testCase)
 *                  - invokes testCase.setOrder()
 *                  - invokes testCase.setTestsToRun() based on a parsing
 *                    of the 'runTests' parameter in the url found at
 *                    goog.global.location.search
 *                  - invokes gTestRunner.initialize(testCase)
 *                     - sets testCase and initialized fields
 *            - invokes G_testRunner.execute()
 *               - invokes this.testCase.setCompletedCallback()
 *               - invokes this.testCase.runTests()
 *                  - invokes testCase.setUpPage()
 *                  - invokes testCase.execute()
 *                     - invokes testCase.cycleTests()
 *                        ...
 *   
 *   In Meta<javascript>, the above control flow is changed as follows:
 *    - For user-defined class <C> in namespace <N>, Meta implicitly defines
 *      test class <N>_test.<C>Test in file <N>/<C>_test.js.
 *    - The <C>_test.js file does NOT goog.require('goog.testing.jsunit').
 *    - The <C>Test class inherits (directly or indirectly) from
 *      metax.test.TestCase (which inherits from goog.testing.TestCase),
 *      and has zero or more 'test_<M>*' methods defined for every user-defined
 *      method <M> defined on <C> depending on the presence of 'test' or 'tests'
 *      attributes on <M>.
 *    - In <C>_test.js file, after the definition of <C>Test, the following
 *      code exists:
 *        var testCase = new <N>.<C>Test('<N>.<C>Test');
 *        testCase.run();
 *    - The 'run' method (metax.test.TestCase.run) does the following:
 *       - Invokes jsunit(), which does similar work to what goog.testing.jsunit
 *         does.
 *       - Invokes setTestObj(), which does similar work to 
 *         goog.testing.TestCase.setTestObj()
 *       - Invokes gTestRunner.setStrict(false) to all 0 tests
 *       - Invokes goog.testing.TestCase.initializeTestRunner()
 *       - Invokes gTestRunner.execute()
 *           ...
 *   
 *   Modifications needed to io_bazel_rules_closure
 *    - created local repository at $WMH/src/google/rules_closure
 *      with
 *        % cd $WMH/src/google
 *        % git clone https://github.com/bazelbuild/rules_closure.git
 *        % cd rules_closure
 *    - modified
 *       closure/testing/phantomjs_harness.js
 *        - parse out optional --key=value args before the html file and .js files
 *        - create query string
 *        - add query string to url
 *        - change 'path == VIRTUAL_PAGE' to 'page.startsWith(VIRTUAL_PAGE)'
 *       closure/testing/phantomjs_test.bzl
 *        - based on --test_arg, insert values into the 'args' list before
 *          ctx.file.html.short_path.
 *        - TODO(wmh): How to get access to --test_arg (and/or --test_env)?
 *          ctx.configuration.default_shell_env doesn't store --test_env,
 *          and ctx.configuration.test_env doesn't even exist, contrary to
 *          https://bazel.build/versions/master/docs/skylark/lib/configuration.html
 * @public
 */
class TestCase_ extends TestCase {

  // field debug : bool
  //   If True, prints out each invocation of the initializer, setup,
  //   teardown and finalizer methods.

  /**
   * metax.test.TestCase.debug/get
   * @return {!boolean}
   * @public
   */
  debug() {
    return this._debug;
  };

  /**
   * metax.test.TestCase.debugIs
   * @param {!boolean} value
   * @public
   */
  debugIs(value) {
    this._debug = value;
  };

  /**
   * metax.test.TestCase.debugRef
   * @return {!boolean}
   * @public
   */
  debugRef() {
    return this._debug;
  };

  // field uid : @str
  //   The name of the method that this instance of TestCase is
  //   responsible for testing. Although the parent initializer also
  //   stores this, each baselang uses a different name for the field.
  //   Rather than encoding this name in each baselang, we just store a
  //   new copy locally.

  /**
   * metax.test.TestCase.uid/get
   * @return {!string}
   * @public
   */
  uid() {
    return this._uid;
  };

  /**
   * metax.test.TestCase.uidIs
   * @param {!string} value
   * @public
   */
  uidIs(value) {
    this._uid = value;
  };

  /**
   * metax.test.TestCase.uidRef
   * @return {!string}
   * @public
   */
  uidRef() {
    return this._uid;
  };

  // field tmpfiles : @vec<str>
  //   The collection of temporary files created via tmpFile().

  /**
   * metax.test.TestCase.tmpfiles/get
   * @return {!Array.<?string>}
   * @public
   */
  tmpfiles() {
    return this._tmpfiles;
  };

  /**
   * metax.test.TestCase.tmpfilesIs
   * @param {!Array.<?string>} value
   * @public
   */
  tmpfilesIs(value) {
    this._tmpfiles = value;
  };

  /**
   * metax.test.TestCase.tmpfilesRef
   * @return {!Array.<?string>}
   * @public
   */
  tmpfilesRef() {
    return this._tmpfiles;
  };

  // field tmpdirs : @vec<str>
  //   The collection of temporary dirs created via tmpDir()

  /**
   * metax.test.TestCase.tmpdirs/get
   * @return {!Array.<?string>}
   * @public
   */
  tmpdirs() {
    return this._tmpdirs;
  };

  /**
   * metax.test.TestCase.tmpdirsIs
   * @param {!Array.<?string>} value
   * @public
   */
  tmpdirsIs(value) {
    this._tmpdirs = value;
  };

  /**
   * metax.test.TestCase.tmpdirsRef
   * @return {!Array.<?string>}
   * @public
   */
  tmpdirsRef() {
    return this._tmpdirs;
  };

  // field moxlist : @vec<any>
  //   The collection of mocking objects created via newMox.
  //   TODO(wmh): Rename this something non-python-centric.

  /**
   * metax.test.TestCase.moxlist/get
   * @return {!Array.<?*>}
   * @public
   */
  moxlist() {
    return this._moxlist;
  };

  /**
   * metax.test.TestCase.moxlistIs
   * @param {!Array.<?*>} value
   * @public
   */
  moxlistIs(value) {
    this._moxlist = value;
  };

  /**
   * metax.test.TestCase.moxlistRef
   * @return {!Array.<?*>}
   * @public
   */
  moxlistRef() {
    return this._moxlist;
  };

  // field stdout : ostream
  //   The current stream used for stdout.  If null, the default is used.

  /**
   * metax.test.TestCase.stdout/get
   * @return {?Object}
   * @public
   */
  stdout() {
    return this._stdout;
  };

  /**
   * metax.test.TestCase.stdoutIs
   * @param {?Object} value
   * @public
   */
  stdoutIs(value) {
    this._stdout = value;
  };

  /**
   * metax.test.TestCase.stdoutRef
   * @return {?Object}
   * @public
   */
  stdoutRef() {
    return this._stdout;
  };

  // field stderr : ostream
  //   The current stream used for stderr.  If null, the default is used.

  /**
   * metax.test.TestCase.stderr/get
   * @return {?Object}
   * @public
   */
  stderr() {
    return this._stderr;
  };

  /**
   * metax.test.TestCase.stderrIs
   * @param {?Object} value
   * @public
   */
  stderrIs(value) {
    this._stderr = value;
  };

  /**
   * metax.test.TestCase.stderrRef
   * @return {?Object}
   * @public
   */
  stderrRef() {
    return this._stderr;
  };

  // field stdin : istream
  //   The current stream used for stdin.  If null, the default is used.

  /**
   * metax.test.TestCase.stdin/get
   * @return {?Object}
   * @public
   */
  stdin() {
    return this._stdin;
  };

  /**
   * metax.test.TestCase.stdinIs
   * @param {?Object} value
   * @public
   */
  stdinIs(value) {
    this._stdin = value;
  };

  /**
   * metax.test.TestCase.stdinRef
   * @return {?Object}
   * @public
   */
  stdinRef() {
    return this._stdin;
  };

  // field fsinfo : @map
  //   Maps module names to dicts containing:
  //     module: the module itself
  //     fs: the fake filesystem for the module.

  /**
   * metax.test.TestCase.fsinfo/get
   * @return {!Object.<!string,?*>}
   * @public
   */
  fsinfo() {
    return this._fsinfo;
  };

  /**
   * metax.test.TestCase.fsinfoIs
   * @param {!Object.<!string,?*>} value
   * @public
   */
  fsinfoIs(value) {
    this._fsinfo = value;
  };

  /**
   * metax.test.TestCase.fsinfoRef
   * @return {!Object.<!string,?*>}
   * @public
   */
  fsinfoRef() {
    return this._fsinfo;
  };

  // field envars : @map
  //   Records environment variables modified during a test (so they
  //   can be reinstated).

  /**
   * metax.test.TestCase.envars/get
   * @return {!Object.<!string,?*>}
   * @public
   */
  envars() {
    return this._envars;
  };

  /**
   * metax.test.TestCase.envarsIs
   * @param {!Object.<!string,?*>} value
   * @public
   */
  envarsIs(value) {
    this._envars = value;
  };

  /**
   * metax.test.TestCase.envarsRef
   * @return {!Object.<!string,?*>}
   * @public
   */
  envarsRef() {
    return this._envars;
  };

  // field fs : any
  //   Only initialized if SetupSharedFilesystem() is invoked.

  /**
   * metax.test.TestCase.fs/get
   * @return {?*}
   * @public
   */
  fs() {
    return this._fs;
  };

  /**
   * metax.test.TestCase.fsIs
   * @param {?*} value
   * @public
   */
  fsIs(value) {
    this._fs = value;
  };

  /**
   * metax.test.TestCase.fsRef
   * @return {?*}
   * @public
   */
  fsRef() {
    return this._fs;
  };

  // field stubs : goog.testing.PropertyReplacer
  //   Allows us to stub out methods and have them implicitly reverted.

  /**
   * metax.test.TestCase.stubs/get
   * @return {?goog.testing.PropertyReplacer}
   * @public
   */
  stubs() {
    return this._stubs;
  };

  /**
   * metax.test.TestCase.stubsIs
   * @param {?goog.testing.PropertyReplacer} value
   * @public
   */
  stubsIs(value) {
    this._stubs = value;
  };

  /**
   * metax.test.TestCase.stubsRef
   * @return {?goog.testing.PropertyReplacer}
   * @public
   */
  stubsRef() {
    return this._stubs;
  };

  // field method_name : @str
  //   The name of the method being tested.
  //   TODO(wmh): Redundant in Python and Javascript since the superclass
  //   defines a similar field. Need a way to define 'specific' fields
  //   for only certain baselangs.

  /**
   * metax.test.TestCase.method_name/get
   * @return {!string}
   * @public
   */
  method_name() {
    return this._method_name;
  };

  /**
   * metax.test.TestCase.method_nameIs
   * @param {!string} value
   * @public
   */
  method_nameIs(value) {
    this._method_name = value;
  };

  /**
   * metax.test.TestCase.method_nameRef
   * @return {!string}
   * @public
   */
  method_nameRef() {
    return this._method_name;
  };

  /**
   * initializer
   *   In all XUnit testing environments, a TestCase is a class defining
   *   a collection of test methods (methods starting with 'test') and
   *   service methods (methods not starting with 'test'). There is a specific
   *   order of operation for how these TestCases are executed.
   *    - the meta-level SetUp() method is invoked to perform one time
   *      initialization of the TestCase.
   *    - if there are N test methods in the Test Case, N instances of
   *      TestCase are created
   *    - for each instance created above:
   *       - invoke the setUp() method
   *       - invoke the test method that this instance was created to run
   *       - invoke the tearDown() method.
   *    - the finalizers for each instance of TestCase are invoked.
   *    - the meta-level TearDown() method is invoked to cleanup anything
   *      done in SetUp()
   *   
   *   The exact names of the setUp, tearDown, SetUp and TearDown methods
   *   vary across baselangs, which is why the 'lifecycle' construct exists ...
   *   it knowns the underlying method names that need to be generated in
   *   each baselang, allowing the user to focus simply on the
   *   init/setup/teardown/finalize sequence.
   *   
   *   Note that the javascript asserting methods are available in 
   *     $CLOSURE_ROOT/library/closure/goog-orig/testing/asserts.js
   *   They are rather odd in having the optional message be the first argument
   *   of the method (so we have to do some reversal to get the more intuitive
   *   'optional message as last arg' idiom.
   *   
   *   Note that the 'location' feature attribute of the 'lifecycle' construct
   *   specifies whether we are referring to an explicit class, the implicit meta
   *   class associated with an explicit class, or the implicit test class
   *   associated with an explicit class.  If the class itself has 'location'
   *   meta, it doesn't make sense to have any of its 'lifecycle' instances
   *   also have location 'meta' (a meta class does not have a meta class).
   *   The same is true for 'test' (a test class does not have a test class).
   *   However, a meta class can have a test class, and a test class has a
   *   meta class.
   * @param {!string} method_name
   *   A name for the test case.
   *   IMPORTANT: Since the Meta compiler implicitly adds a parameter to
   *   meta lifecycles of testcase classes, it is important that we ...???
   */
  constructor(method_name) {
    super(method_name);
    this._debug = false;
    this._tmpfiles = [];
    this._tmpdirs = [];
    this._moxlist = [];
    this._stdout = null;
    this._stderr = null;
    this._stdin = null;
    this._fsinfo = {};
    this._envars = {};
    this._fs = null;
    this._stubs = null;
    /** @type {!boolean} */ this._debug;
    /** @type {!string} */ this._uid;
    /** @type {!Array.<?string>} */ this._tmpfiles;
    /** @type {!Array.<?string>} */ this._tmpdirs;
    /** @type {!Array.<?*>} */ this._moxlist;
    /** @type {?Object} */ this._stdout;
    /** @type {?Object} */ this._stderr;
    /** @type {?Object} */ this._stdin;
    /** @type {!Object.<!string,?*>} */ this._fsinfo;
    /** @type {!Object.<!string,?*>} */ this._envars;
    /** @type {?*} */ this._fs;
    /** @type {?goog.testing.PropertyReplacer} */ this._stubs;
    /** @type {!string} */ this._method_name;
    // User-provided code follows.
    var count = MetaTestCase.InstanceCount() + 1;
    MetaTestCase.InstanceCountIs(count);
    console.log('Here with ' + method_name + ' and ' + this.methname());
    this.uidIs(method_name + ':' + count);
    this.deblog(
        'Invoking ' + this.name() + ' initializer for ' + method_name);
    this.method_nameIs(method_name);
  };

  /**
   * metax.test.TestCase.runSelfTests
   *   Initializes the test runner.
   *   
   *   The suggested mechanism for running unittests on a goog.module() is
   *   discussed in https://github.com/google/closure-library/wiki/goog.module:-an-ES6-module-like-alternative-to-goog.provide#how-do-i-write-a-unit-test-for-a-googmodule
   *     goog.module('goog.baseModuleTest');
   *     goog.setTestOnly('goog.baseModuleTest');
   *   
   *     var jsunit = goog.require('goog.testing.jsunit');
   *     var testSuite = goog.require('goog.testing.testSuite');
   *   
   *     testSuite({
   *       testMethod: function() {},
   *     });
   *   
   *   The object passed into testSuite() is the object that defines all the
   *   test methods and related infrastructure (any executable starting with
   *   'test' is assumed to be a test method).  The code of testSuite() is
   *   in $CLOSURE_ROOT/library/closure/goog-orig/testing/testsuite.js:
   *       // Runs the lifecycle methods (setUp, tearDown, etc.) and test* methods from
   *       // the given object. For use in tests that are written as JavaScript modules
   *       // or goog.modules.
   *       //
   *       // @param {!Object<string, function()>} obj An object with one or more test
   *       //     methods, and optional setUp, tearDown and getTestName methods, etc.
   *      goog.testing.testSuite = function(obj) {
   *        var testCase = goog.labs.testing.Environment.getTestCaseIfActive() ||
   *            new goog.testing.TestCase(document.title);
   *        testCase.setTestObj(obj);
   *        goog.testing.TestCase.initializeTestRunner(testCase);
   *      };
   *   
   *   Note that it creates a new TestCase instance, and passes an independent
   *   object to that testcase. In Meta, however, the testcase class itself
   *   is the object defining the tests.  So in Meta we invoke unittests
   *   slightly differently:
   *     goog.module('nm.sp.FooTest');
   *     goog.setTestOnly('nm.sp.FooTest');
   *     const TestCase = goog.require('metax.test.TestCase');
   *   
   *     class FooTest extends TestCase { ... }
   *     var tc = new FooTest('nm.sp.FooTest');
   *     tc.runSelfTests();
   * @public
   */
  runSelfTests() {
    // The object defining the test methods is this TestCase subclass
    // instance.
    this.setTestObj(this);
    TestCase.initializeTestRunner(this);
    var testrunner = /** @type {?TestRunner} */ (goog.global['G_testRunner']);
    testrunner.setStrict(false);
  };

  /**
   * metax.test.TestCase.status
   *   The status of an individual test.
   *   
   * @return {!string}
   *     One of '', 'FAIL' or 'ERROR'.
   * @public
   */
  status() {
    // console.log('Fix TestCase.status in Javascript');
    return 'FIXME';
  };

  /**
   * metax.test.TestCase.deblog
   *   Print out a Meta specific log message.
   * @param {!string} msg
   * @public
   */
  deblog(msg) {
    if (this.debug()) {
      this.log(this.uid() + ': ' + msg);
    }
  };

  /**
   * metax.test.TestCase.name
   *   The name of this testcase.
   *   See methname for the name of the method within the testcase.
   * @return {!string}
   * @public
   */
  name() {
    return this.constructor.name;
  };

  /**
   * metax.test.TestCase.methname
   *   The name of the method defined within a subclass of TestCase to be
   *   invoked as the test.
   *   
   * @return {!string}
   * @public
   * @suppress {visibility}
   */
  methname() {
    return this.name_;
  };

  /**
   * metax.test.TestCase.setenv
   * @param {?string} evar
   * @param {?string} value
   * @public
   */
  setenv(evar, value) {
    throw new Error('TestCase.setenv() not yet implemented');
  };

  /**
   * metax.test.TestCase.newStr
   *   Create a new string stream for use anywhere a istream or
   *   ostream is required.
   * @param {?string} [content=null]
   * @return {?Object}
   * @public
   */
  newStr(content=null) {
    throw new Error('TestCase.newStr() not yet implemented');
  };

  /**
   * metax.test.TestCase.fp
   *   Create a new string stream for use anywhere a istream or
   *   ostream is required.
   *   
   *   TODO(wmh): Decide which of 'newStr' or 'fp' to keep.
   * @param {?string} [content=null]
   * @return {?Object}
   * @public
   */
  fp(content=null) {
    throw new Error('TestCase.fp() not yet implemented');
  };

  /**
   * metax.test.TestCase.tmpFile
   *   Create a temporary file and return its path.
   * @param {!boolean} [create=true]
   * @public
   */
  tmpFile(create=true) {
    throw new Error('TestCase.tmpFile() not yet implemented');
  };

  /**
   * metax.test.TestCase.tmpDir
   *   Create a temporary directory and return its path.
   * @param {!boolean} [create=true]
   * @public
   */
  tmpDir(create=true) {
    throw new Error('TestCase.tmpDir() not yet implemented');
  };

  /**
   * metax.test.TestCase.fileContents
   *   Return the contents of a specified file.
   * @param {?*} path
   * @public
   */
  fileContents(path) {
    throw new Error('TestCase.fileContents() not yet implemented');
  };

  /**
   * metax.test.TestCase.isInteractive
   *   Determine whether this TestCase is marked as supporting tests that
   *   require interactive responses from a user.
   * @return {!boolean}
   * @public
   */
  isInteractive() {
    return MetaTestCase.Interactive();
  };

  /**
   * metax.test.TestCase.allowNetwork
   *   Determine whether this TestCase is marked s supporting tests that
   *   require network access.
   * @param {?*} guarding
   * @return {!boolean}
   * @public
   */
  allowNetwork(guarding) {
    throw new Error('TestCase.allowNetwork() not yet implemented');
  };

  /**
   * metax.test.TestCase.assertDictContains
   * @param {?Object.<!string,?*>} data
   * @param {?Object.<!string,?*>} subdata
   * @public
   */
  assertDictContains(data, subdata) {
    throw new Error('TestCase.assertDictContains() not yet implemented');
  };

  /**
   * metax.test.TestCase.startswith
   * @param {?string} prefix
   * @param {?string} strval
   * @public
   */
  startswith(prefix, strval) {
    assertTrue(
      'String\n  \"' + strval + '\"\ndoes not start with\n  \"' + prefix + '\"',
      strval.startsWith(/** @type {!string} */ (prefix)));
  };

  /**
   * metax.test.TestCase.endswith
   * @param {?string} suffix
   * @param {?string} strval
   * @public
   */
  endswith(suffix, strval) {
    assertTrue(
      'String\n  \"' + strval + '\"\ndoes not end with\n  \"' + suffix + '\"',
      strval.endsWith(/** @type {!string} */ (suffix)));
  };

  /**
   * metax.test.TestCase.contains
   * @param {?*} member
   * @param {?*} container
   * @param {?string} [msg=null]
   * @public
   */
  contains(member, container, msg=null) {
    if (msg) {
      assertContains(msg, member, container);
    } else {
      assertContains(member, container);
    }
  };

  /**
   * metax.test.TestCase.matches
   *   A string value matches a regexp. 
   * @param {?string} restr
   *   The regexp to match against (as a string).
   * @param {?string} value
   *   The value to match.
   * @public
   */
  matches(restr, value) {
    console.log('Fix TestCase.matches in Javascript');
  };

  /**
   * metax.test.TestCase.iseq
   *   Compare an arbitrary two entities for equality (not pointer equality!)
   *   
   *   NOTE: This method may not be implementable in C++. Decide whether we
   *   want to keep it for use in other baselangs, or if allowing it
   *   encourages people to use methods that won't work in <cc> and <*>.
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  iseq(expected, item, message=null) {
    if (message == null) {
      assertEquals(expected, item);
    } else {
      assertEquals(message, expected, item);
    }
  };

  /**
   * metax.test.TestCase.noteq
   *   Compare an arbitrary two entities for non-equality (not pointer equality!)
   *   
   *   See comment in 'eq' about viability in C++ and ramifications on this
   *   method.
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  noteq(expected, item, message=null) {
    if (message == null) {
      assertNotEquals(expected, item);
    } else {
      assertNotEquals(message, expected, item);
    }
  };

  /**
   * metax.test.TestCase.iseqstr
   *   Compare an arbitrary two entities for equality (not pointer equality!)
   *   
   *   NOTE: This method may not be implementable in C++. Decide whether we
   *   want to keep it for use in other baselangs, or if allowing it
   *   encourages people to use methods that won't work in <cc> and <*>.
   * @param {!string} expected
   * @param {!string} item
   * @param {?string} [message=null]
   * @public
   */
  iseqstr(expected, item, message=null) {
    if (message == null) {
      assertEquals(expected, item);
    } else {
      assertEquals(message, expected, item);
    }
  };

  /**
   * metax.test.TestCase.noteqstr
   *   Compare an arbitrary two entities for non-equality (not pointer equality!)
   * @param {!string} expected
   * @param {!string} item
   * @param {?string} [message=null]
   * @public
   */
  noteqstr(expected, item, message=null) {
    if (message == null) {
      assertNotEquals(expected, item);
    } else {
      assertNotEquals(message, expected, item);
    }
  };

  /**
   * metax.test.TestCase.iseqvec
   * @param {?Array.<?*>} expected
   * @param {?Array.<?*>} items
   * @param {?string} [message=null]
   * @public
   */
  iseqvec(expected, items, message=null) {
    if (message == null) {
      assertElementsEquals(expected, items);
    } else {
      assertElementsEquals(message, expected, items);
    }
  };

  /**
   * metax.test.TestCase.iseqmap
   * @param {?*} expected
   * @param {?*} data
   * @param {?*} [msg=null]
   * @param {!number} [width=30]
   * @public
   */
  iseqmap(expected, data, msg=null, width=30) {
    if (msg) {
      assertHashEquals(msg, expected, data);
    } else {
      assertHashEquals(expected, data);
    }
  };

  /**
   * metax.test.TestCase.iseqtext
   * @param {?string} first
   * @param {?string} second
   * @param {?string} [text=null]
   * @public
   */
  iseqtext(first, second, text=null) {
    if (text === null) {
      assertEquals(first, second);
    } else {
      assertEquals(text, first, second);
    }
  };

  /**
   * metax.test.TestCase.iseqfile
   * @param {?*} file1
   * @param {?*} file2
   * @public
   */
  iseqfile(file1, file2) {
    throw new Error('TestCase.() not yet implemented');
  };

  /**
   * metax.test.TestCase.iseqstrgold
   * @param {?*} content
   * @param {?*} golden
   * @public
   */
  iseqstrgold(content, golden) {
    throw new Error('TestCase.() not yet implemented');
  };

  /**
   * metax.test.TestCase.iseqfilegold
   * @param {?*} path
   * @param {?*} golden
   * @public
   */
  iseqfilegold(path, golden) {
    throw new Error('TestCase.() not yet implemented');
  };

  /**
   * metax.test.TestCase.isapprox
   *   Compare two float values for closeness.
   * @param {!number} f1
   * @param {!number} f2
   * @param {!number} [delta=0.00001]
   * @param {?string} [msg=null]
   * @public
   */
  isapprox(f1, f2, delta=0.00001, msg=null) {
    if (msg) {
      assertRoughlyEquals(msg, f1, f2, delta);
    } else {
      assertRoughlyEquals(f1, f2, delta);
    }
  };

  /**
   * metax.test.TestCase.islt
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  islt(expected, item, message=null) {
    if (message == null) {
      message = '' + expected + ' >= ' + item;
    }
    assertTrue(message, expected < item);
  };

  /**
   * metax.test.TestCase.isle
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  isle(expected, item, message=null) {
    if (message == null) {
      message = '' + expected + ' > ' + item;
    }
    assertTrue(message, expected <= item);
  };

  /**
   * metax.test.TestCase.isgt
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  isgt(expected, item, message=null) {
    if (message == null) {
      message = '' + expected + ' <= ' + item;
    }
    assertTrue(message, expected > item);
  };

  /**
   * metax.test.TestCase.isge
   * @param {?*} expected
   * @param {?*} item
   * @param {?*} [message=null]
   * @public
   */
  isge(expected, item, message=null) {
    if (message == null) {
      message = '' + expected + ' < ' + item;
    }
    assertTrue(message, expected >= item);
  };

  /**
   * metax.test.TestCase.raises
   *   Confirm that the given method raises an exception.
   *   
   *   Note that the python version accepts arbitrary positional and
   *   keyword args while the javascript version does not. Need to get 
   *   varargs supported in javascript before we can try implementing it.
   * @param {?Object} eclass
   *   The exception class raised
   * @param {(!Function|!string)} func
   *   The callable object
   * @param {*} varargs
   * @public
   */
  raises(eclass, func, varargs) {
    // TODO(wmh): goog.testing.asserts.assertThrows() is rather limited:
    //  - it only handles methods that that don't require any args
    //  - it only detects whether any exception is raised, not whether a
    //    specific exception is raised.
    // A better version of assertThrows() is certainly possible. Implement
    // it.
    var e = assertThrows(func);
    // TODO(wmh): At the very least, we can compare the exception 'e' against
    // expected 'eclass'.
  };

  /**
   * metax.test.TestCase.issame
   * @param {?*} obj1
   * @param {?*} obj2
   * @public
   */
  issame(obj1, obj2) {
    assertTrue(obj1 + ' is not ' + obj2, obj1 === obj2);
  };

  /**
   * metax.test.TestCase.notsame
   * @param {?*} obj1
   * @param {?*} obj2
   * @public
   */
  notsame(obj1, obj2) {
    assertFalse(obj1 + ' is ' + obj2, obj1 === obj2);
  };

  /**
   * metax.test.TestCase.istrue
   *   Note that we cannot use 'true' as a method because that is reserved in
   *   various languages (and we want a common interface across all languages).
   * @param {!boolean} val
   * @param {?string} [msg=null]
   * @public
   */
  istrue(val, msg=null) {
    if (msg == null) {
      assertTrue(val);
    } else {
      assertTrue(msg, val);
    }
  };

  /**
   * metax.test.TestCase.isfalse
   *   Note that we cannot use 'false' as a method because that is reserved in
   *   various languages (and we want a common interface across all languages).
   * @param {!boolean} val
   * @param {?string} [msg=null]
   * @public
   */
  isfalse(val, msg=null) {
    if (msg) {
      assertFalse(msg, val);
    } else {
      assertFalse(val);
    }
  };

  /**
   * metax.test.TestCase.isnull
   *   Confirm the arg is null.
   * @param {?*} val
   * @param {?string} [msg=null]
   * @public
   */
  isnull(val, msg=null) {
    if (msg) {
      assertNull(msg, val);
    } else {
      assertNull(val);
    }
  };

  /**
   * metax.test.TestCase.notnull
   *   Confirm the arg is not null.
   * @param {?*} val
   * @param {?string} [msg=null]
   * @public
   */
  notnull(val, msg=null) {
    if (msg) {
      assertNotNull(msg, val);
    } else {
      assertNotNull(val);
    }
  };

  /**
   * metax.test.TestCase.isinst
   * @param {?*} obj
   *   The object to test.
   * @param {?*} cls
   *   The class the object is expected to be an instance of.
   *   In javascript, this is the constructor function.
   * @public
   */
  isinst(obj, cls) {
    this.istrue(
      typeof obj == cls,
      'Expecting ' + obj + ' to be an instance of ' + cls);
  };

  /**
   * metax.test.TestCase.fail
   *   # Invoked to indicate an unconditional failure.
   * @param {?string} msg
   * @public
   */
  fail(msg) {
    this.istrue(false, msg);
  };

  /**
   * metax.test.TestCase.meta
   * @return {?metax.root.ObjectMetaRoot}
   * @public
   */
  meta() {
    return MetaTestCase;
  };

  /**
   * metax.test.TestCase.setUp
   * @public
   * @override 
   */
  setUp() {
    super.setUp();
    // User-provided code follows.
    this.deblog('Invoking ' + this.name() + ' setUp for ' + this.methname());
    // TODO(wmh): Look into the stub mechanism provided by
    // goog.testing.propertyreplacer.js
    this._stubs = new /* goog.testing.*/ PropertyReplacer();
  };

  /**
   * metax.test.TestCase.setUpPage
   * @public
   * @override 
   */
  setUpPage() {
    super.setUpPage();
    // User-provided code follows.
    if (/* metax.test.*/ MetaTestCase.Debug()) {
      console.log('Invoking ' + this.constructor.name + ' SetUp');
    }
  };

  /**
   * metax.test.TestCase.tearDown
   * @public
   * @override 
   */
  tearDown() {
    // $CLOSURE_ROOT/library/closure/goog-orig/testing/testcase.js
    this.deblog(
      'Invoking ' + this.name() + ' tearDown for ' + this.methname());
    // From goog.testing.propertyreplacer.js
    // this._stubs.reset();
    super.tearDown();
  };

  /**
   * metax.test.TestCase.tearDownPage
   * @public
   * @override 
   */
  tearDownPage() {
    if (MetaTestCase.Debug()) {
      console.log('Invoking ' + this.constructor.name + ' TearDown');
    }
    super.tearDownPage();
  };
}
exports = TestCase_;
