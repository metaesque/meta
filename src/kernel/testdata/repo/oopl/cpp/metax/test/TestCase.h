#ifndef metax_test_TestCase_h
#define metax_test_TestCase_h 1

#include "gtest/gtest.h"
#include "metax/root/Error.h"
#include "metax/test/TestCaseMeta.h"
#include <sstream>
#include <typeinfo>

namespace metax {
namespace test {

// The JUnit testing infrastructure for Java (which came from a testing
// infrastructure for Smalltalk) has gained cross-language recognition, and
// there is an xUnit implementation for basically every OO language
// (e.g. CppUnit, JSUnit, python unit (unittest), etc.).
// 
// See $METAROOT/UseGuide.wmd (/Meta/Meta From The Middle Ground/Unit Tests)
// for a discussion of xUnit and how Meta implements this testing paradigm
// across all baselangs.
// 
// See the src/kernel/asserts.org file for details on alerts across
// baselangs.
// 
// In javascript, the normal idiom for doing javascript testing using
// bazel and google closure is as follows:
//  - unittests are implemented in some file ending in _test.js
//  - the file must goog.require('goog.testing.jsunit'), which:
//     - creates cached G_testRunner (if G_testRunner already exists, noop)
//     - creates a window.onerror handler to report errors during test
//       initialization
//     - creates a window.onload handler so that when the page containing
//       the *_test.js file is loaded:
//        - invokes any already specified onload code
//        - creates a timeout to execute the following after 500ms
//          - if G_testRunner is not yet initialized:
//             - create a TestCase instance 'testCase'
//             - invoke goog.testing.TestCase.initializeTestRunner(testCase)
//                - invokes testCase.setOrder()
//                - invokes testCase.setTestsToRun() based on a parsing
//                  of the 'runTests' parameter in the url found at
//                  goog.global.location.search
//                - invokes gTestRunner.initialize(testCase)
//                   - sets testCase and initialized fields
//          - invokes G_testRunner.execute()
//             - invokes this.testCase.setCompletedCallback()
//             - invokes this.testCase.runTests()
//                - invokes testCase.setUpPage()
//                - invokes testCase.execute()
//                   - invokes testCase.cycleTests()
//                      ...
// 
// In Meta<javascript>, the above control flow is changed as follows:
//  - For user-defined class <C> in namespace <N>, Meta implicitly defines
//    test class <N>_test.<C>Test in file <N>/<C>_test.js.
//  - The <C>_test.js file does NOT goog.require('goog.testing.jsunit').
//  - The <C>Test class inherits (directly or indirectly) from
//    metax.test.TestCase (which inherits from goog.testing.TestCase),
//    and has zero or more 'test_<M>*' methods defined for every user-defined
//    method <M> defined on <C> depending on the presence of 'test' or 'tests'
//    attributes on <M>.
//  - In <C>_test.js file, after the definition of <C>Test, the following
//    code exists:
//      var testCase = new <N>.<C>Test('<N>.<C>Test');
//      testCase.run();
//  - The 'run' method (metax.test.TestCase.run) does the following:
//     - Invokes jsunit(), which does similar work to what goog.testing.jsunit
//       does.
//     - Invokes setTestObj(), which does similar work to 
//       goog.testing.TestCase.setTestObj()
//     - Invokes gTestRunner.setStrict(false) to all 0 tests
//     - Invokes goog.testing.TestCase.initializeTestRunner()
//     - Invokes gTestRunner.execute()
//         ...
// 
// Modifications needed to io_bazel_rules_closure
//  - created local repository at $WMH/src/google/rules_closure
//    with
//      % cd $WMH/src/google
//      % git clone https://github.com/bazelbuild/rules_closure.git
//      % cd rules_closure
//  - modified
//     closure/testing/phantomjs_harness.js
//      - parse out optional --key=value args before the html file and .js files
//      - create query string
//      - add query string to url
//      - change 'path == VIRTUAL_PAGE' to 'page.startsWith(VIRTUAL_PAGE)'
//     closure/testing/phantomjs_test.bzl
//      - based on --test_arg, insert values into the 'args' list before
//        ctx.file.html.short_path.
//      - TODO(wmh): How to get access to --test_arg (and/or --test_env)?
//        ctx.configuration.default_shell_env doesn't store --test_env,
//        and ctx.configuration.test_env doesn't even exist, contrary to
//        https://bazel.build/versions/master/docs/skylark/lib/configuration.html
class TestCase : public ::testing::Test {

  // field debug : bool
  //   If True, prints out each invocation of the initializer, setup,
  //   teardown and finalizer methods.
  private: bool _debug;
  public: virtual bool debug() const { return this->_debug; }
  public: virtual void debugIs(bool value) { this->_debug = value; }
  public: virtual bool& debugRef() { return this->_debug; }

  // field uid : @str
  //   The name of the method that this instance of TestCase is
  //   responsible for testing. Although the parent initializer also
  //   stores this, each baselang uses a different name for the field.
  //   Rather than encoding this name in each baselang, we just store a
  //   new copy locally.
  private: std::string _uid;
  public: virtual const std::string& uid() const { return this->_uid; }
  public: virtual void uidIs(const std::string& value) { this->_uid = value; }
  public: virtual std::string& uidRef() { return this->_uid; }

  // field tmpfiles : @vec<str>
  //   The collection of temporary files created via tmpFile().
  private: std::vector<const std::string*> _tmpfiles;
  public: virtual const std::vector<const std::string*>& tmpfiles() const { return this->_tmpfiles; }
  public: virtual void tmpfilesIs(std::vector<const std::string*> value) { this->_tmpfiles = value; }
  public: virtual std::vector<const std::string*>& tmpfilesRef() { return this->_tmpfiles; }

  // field tmpdirs : @vec<str>
  //   The collection of temporary dirs created via tmpDir()
  private: std::vector<const std::string*> _tmpdirs;
  public: virtual const std::vector<const std::string*>& tmpdirs() const { return this->_tmpdirs; }
  public: virtual void tmpdirsIs(std::vector<const std::string*> value) { this->_tmpdirs = value; }
  public: virtual std::vector<const std::string*>& tmpdirsRef() { return this->_tmpdirs; }

  // field moxlist : @vec<any>
  //   The collection of mocking objects created via newMox.
  //   TODO(wmh): Rename this something non-python-centric.
  private: std::vector<void**> _moxlist;
  public: virtual const std::vector<void**>& moxlist() const { return this->_moxlist; }
  public: virtual void moxlistIs(std::vector<void**> value) { this->_moxlist = value; }
  public: virtual std::vector<void**>& moxlistRef() { return this->_moxlist; }

  // field stdout : ostream
  //   The current stream used for stdout.  If null, the default is used.
  private: std::ostream* _stdout;
  public: virtual const std::ostream*const stdout() const { return this->_stdout; }
  public: virtual void stdoutIs(std::ostream* value) { this->_stdout = value; }
  public: virtual std::ostream*& stdoutRef() { return this->_stdout; }

  // field stderr : ostream
  //   The current stream used for stderr.  If null, the default is used.
  private: std::ostream* _stderr;
  public: virtual const std::ostream*const stderr() const { return this->_stderr; }
  public: virtual void stderrIs(std::ostream* value) { this->_stderr = value; }
  public: virtual std::ostream*& stderrRef() { return this->_stderr; }

  // field stdin : istream
  //   The current stream used for stdin.  If null, the default is used.
  private: std::istream* _stdin;
  public: virtual const std::istream*const stdin() const { return this->_stdin; }
  public: virtual void stdinIs(std::istream* value) { this->_stdin = value; }
  public: virtual std::istream*& stdinRef() { return this->_stdin; }

  // field fsinfo : @map
  //   Maps module names to dicts containing:
  //     module: the module itself
  //     fs: the fake filesystem for the module.
  private: std::map<std::string,void**> _fsinfo;
  public: virtual const std::map<std::string,void**>& fsinfo() const { return this->_fsinfo; }
  public: virtual void fsinfoIs(std::map<std::string,void**> value) { this->_fsinfo = value; }
  public: virtual std::map<std::string,void**>& fsinfoRef() { return this->_fsinfo; }

  // field envars : @map
  //   Records environment variables modified during a test (so they
  //   can be reinstated).
  private: std::map<std::string,void**> _envars;
  public: virtual const std::map<std::string,void**>& envars() const { return this->_envars; }
  public: virtual void envarsIs(std::map<std::string,void**> value) { this->_envars = value; }
  public: virtual std::map<std::string,void**>& envarsRef() { return this->_envars; }

  // field fs : *void
  //   Only initialized if SetupSharedFilesystem() is invoked.
  private: void* _fs;
  public: virtual const void*const fs() const { return this->_fs; }
  public: virtual void fsIs(void* value) { this->_fs = value; }
  public: virtual void*& fsRef() { return this->_fs; }

  // field stubs : *void
  //   Allows us to stub out methods and have them implicitly reverted.
  private: void* _stubs;
  public: virtual const void*const stubs() const { return this->_stubs; }
  public: virtual void stubsIs(void* value) { this->_stubs = value; }
  public: virtual void*& stubsRef() { return this->_stubs; }

  // field method_name : @str
  //   The name of the method being tested.
  //   TODO(wmh): Redundant in Python and Javascript since the superclass
  //   defines a similar field. Need a way to define 'specific' fields
  //   for only certain baselangs.
  private: std::string _method_name;
  public: virtual const std::string& method_name() const { return this->_method_name; }
  public: virtual void method_nameIs(const std::string& value) { this->_method_name = value; }
  public: virtual std::string& method_nameRef() { return this->_method_name; }
  // In all XUnit testing environments, a TestCase is a class defining
  // a collection of test methods (methods starting with 'test') and
  // service methods (methods not starting with 'test'). There is a specific
  // order of operation for how these TestCases are executed.
  //  - the meta-level SetUp() method is invoked to perform one time
  //    initialization of the TestCase.
  //  - if there are N test methods in the Test Case, N instances of
  //    TestCase are created
  //  - for each instance created above:
  //     - invoke the setUp() method
  //     - invoke the test method that this instance was created to run
  //     - invoke the tearDown() method.
  //  - the finalizers for each instance of TestCase are invoked.
  //  - the meta-level TearDown() method is invoked to cleanup anything
  //    done in SetUp()
  // 
  // The exact names of the setUp, tearDown, SetUp and TearDown methods
  // vary across baselangs, which is why the 'lifecycle' construct exists ...
  // it knowns the underlying method names that need to be generated in
  // each baselang, allowing the user to focus simply on the
  // init/setup/teardown/finalize sequence.
  // 
  // Note that the javascript asserting methods are available in 
  //   $CLOSURE_ROOT/library/closure/goog-orig/testing/asserts.js
  // They are rather odd in having the optional message be the first argument
  // of the method (so we have to do some reversal to get the more intuitive
  // 'optional message as last arg' idiom.
  // 
  // Note that the 'location' feature attribute of the 'lifecycle' construct
  // specifies whether we are referring to an explicit class, the implicit meta
  // class associated with an explicit class, or the implicit test class
  // associated with an explicit class.  If the class itself has 'location'
  // meta, it doesn't make sense to have any of its 'lifecycle' instances
  // also have location 'meta' (a meta class does not have a meta class).
  // The same is true for 'test' (a test class does not have a test class).
  // However, a meta class can have a test class, and a test class has a
  // meta class.
  public: TestCase(const std::string& method_name);
  // The status of an individual test.
  // 
  // Returns:
  //   One of '', 'FAIL' or 'ERROR'.
  public: virtual const std::string& status();
  // Print out a Meta specific log message.
  public: virtual void deblog(const std::string& msg);
  // The name of this testcase.
  // See methname for the name of the method within the testcase.
  public: virtual const std::string& name();
  // The name of the method defined within a subclass of TestCase to be
  // invoked as the test.
  // 
  // Meta:suppress: visibility
  public: virtual const std::string& methname();
  public: virtual void setenv(const std::string* evar, const std::string* value);
  // Create a new string stream for use anywhere a istream or
  // ostream is required.
  public: virtual std::stringstream* newStr(const std::string* content = nullptr);
  // Create a new string stream for use anywhere a istream or
  // ostream is required.
  // 
  // TODO(wmh): Decide which of 'newStr' or 'fp' to keep.
  public: virtual std::stringstream* fp(const std::string* content = nullptr);
  // Create a temporary file and return its path.
  public: virtual void tmpFile(bool create = true);
  // Create a temporary directory and return its path.
  public: virtual void tmpDir(bool create = true);
  // Return the contents of a specified file.
  public: virtual void fileContents(void** path);
  // Determine whether this TestCase is marked as supporting tests that
  // require interactive responses from a user.
  public: virtual bool isInteractive();
  // Determine whether this TestCase is marked s supporting tests that
  // require network access.
  public: virtual bool allowNetwork(void** guarding);
  public: virtual void assertDictContains(std::map<std::string,void**>* data, std::map<std::string,void**>* subdata);
  public: virtual void startswith(const std::string* prefix, const std::string* strval);
  public: virtual void endswith(const std::string* suffix, const std::string* strval);
  public: virtual void contains(void** member, void** container, const std::string* msg = nullptr);
  // A string value matches a regexp. 
  public: virtual void matches(const std::string* restr, const std::string* value);
  // Compare an arbitrary two entities for equality (not pointer equality!)
  // 
  // NOTE: This method may not be implementable in C++. Decide whether we
  // want to keep it for use in other baselangs, or if allowing it
  // encourages people to use methods that won't work in <cc> and <*>.
  public: virtual void iseq(void** expected, void** item, void** message = nullptr);
  // Compare an arbitrary two entities for non-equality (not pointer equality!)
  // 
  // See comment in 'eq' about viability in C++ and ramifications on this
  // method.
  public: virtual void noteq(void** expected, void** item, void** message = nullptr);
  // Compare an arbitrary two entities for equality (not pointer equality!)
  // 
  // NOTE: This method may not be implementable in C++. Decide whether we
  // want to keep it for use in other baselangs, or if allowing it
  // encourages people to use methods that won't work in <cc> and <*>.
  public: virtual void iseqstr(const std::string& expected, const std::string& item, const std::string* message = nullptr);
  // Compare an arbitrary two entities for non-equality (not pointer equality!)
  public: virtual void noteqstr(const std::string& expected, const std::string& item, const std::string* message = nullptr);
  public: virtual void iseqvec(std::vector<void**>* expected, std::vector<void**>* items, const std::string* message = nullptr);
  public: virtual void iseqmap(void** expected, void** data, void** msg = nullptr, int32_t width = 30);
  public: virtual void iseqtext(const std::string* first, const std::string* second, const std::string* text = nullptr);
  public: virtual void iseqfile(void** file1, void** file2);
  public: virtual void iseqstrgold(void** content, void** golden);
  public: virtual void iseqfilegold(void** path, void** golden);
  // Compare two float values for closeness.
  public: virtual void isapprox(double f1, double f2, double delta = 0.00001, const std::string* msg = nullptr);
  public: virtual void islt(void** expected, void** item, void** message = nullptr);
  public: virtual void isle(void** expected, void** item, void** message = nullptr);
  public: virtual void isgt(void** expected, void** item, void** message = nullptr);
  public: virtual void isge(void** expected, void** item, void** message = nullptr);
  // Confirm that the given method raises an exception.
  // 
  // Note that the python version accepts arbitrary positional and
  // keyword args while the javascript version does not. Need to get 
  // varargs supported in javascript before we can try implementing it.
  public: virtual void raises(void** eclass, const void*& func, ...);
  public: virtual void issame(void** obj1, void** obj2);
  public: virtual void notsame(void** obj1, void** obj2);
  // Note that we cannot use 'true' as a method because that is reserved in
  // various languages (and we want a common interface across all languages).
  public: virtual void istrue(bool val, const std::string* msg = nullptr);
  // Note that we cannot use 'false' as a method because that is reserved in
  // various languages (and we want a common interface across all languages).
  public: virtual void isfalse(bool val, const std::string* msg = nullptr);
  // Confirm the arg is null.
  public: virtual void isnull(void** val, const std::string* msg = nullptr);
  // Confirm the arg is not null.
  public: virtual void notnull(void** val, const std::string* msg = nullptr);
  public: virtual void isinst(void** obj, void** cls);
  // # Invoked to indicate an unconditional failure.
  public: virtual void fail(const std::string* msg);
  public: virtual metax::root::ObjectMetaRoot* meta();
  public: virtual void SetUp();
  public: static void SetUpTestCase();
  public: virtual void TearDown();
  public: static void TearDownTestCase();
};

}  // test
}  // metax


#endif // metax_test_TestCase_h
