import cStringIO
import logging
import metax.test  # target=//metax/test:test
import re
import sys
import time
import unittest
##########  End Imports  ##########


class TestCase(unittest.TestCase):
  """The JUnit testing infrastructure for Java (which came from a testing
  infrastructure for Smalltalk) has gained cross-language recognition, and
  there is an xUnit implementation for basically every OO language
  (e.g. CppUnit, JSUnit, python unit (unittest), etc.).

  See $METAROOT/UseGuide.wmd (/Meta/Meta From The Middle Ground/Unit Tests)
  for a discussion of xUnit and how Meta implements this testing paradigm
  across all baselangs.

  See the src/kernel/asserts.org file for details on alerts across
  baselangs.

  In javascript, the normal idiom for doing javascript testing using
  bazel and google closure is as follows:
   - unittests are implemented in some file ending in _test.js
   - the file must goog.require('goog.testing.jsunit'), which:
      - creates cached G_testRunner (if G_testRunner already exists, noop)
      - creates a window.onerror handler to report errors during test
        initialization
      - creates a window.onload handler so that when the page containing
        the *_test.js file is loaded:
         - invokes any already specified onload code
         - creates a timeout to execute the following after 500ms
           - if G_testRunner is not yet initialized:
              - create a TestCase instance 'testCase'
              - invoke goog.testing.TestCase.initializeTestRunner(testCase)
                 - invokes testCase.setOrder()
                 - invokes testCase.setTestsToRun() based on a parsing
                   of the 'runTests' parameter in the url found at
                   goog.global.location.search
                 - invokes gTestRunner.initialize(testCase)
                    - sets testCase and initialized fields
           - invokes G_testRunner.execute()
              - invokes this.testCase.setCompletedCallback()
              - invokes this.testCase.runTests()
                 - invokes testCase.setUpPage()
                 - invokes testCase.execute()
                    - invokes testCase.cycleTests()
                       ...

  In Meta<javascript>, the above control flow is changed as follows:
   - For user-defined class <C> in namespace <N>, Meta implicitly defines
     test class <N>_test.<C>Test in file <N>/<C>_test.js.
   - The <C>_test.js file does NOT goog.require('goog.testing.jsunit').
   - The <C>Test class inherits (directly or indirectly) from
     metax.test.TestCase (which inherits from goog.testing.TestCase),
     and has zero or more 'test_<M>*' methods defined for every user-defined
     method <M> defined on <C> depending on the presence of 'test' or 'tests'
     attributes on <M>.
   - In <C>_test.js file, after the definition of <C>Test, the following
     code exists:
       var testCase = new <N>.<C>Test('<N>.<C>Test');
       testCase.run();
   - The 'run' method (metax.test.TestCase.run) does the following:
      - Invokes jsunit(), which does similar work to what goog.testing.jsunit
        does.
      - Invokes setTestObj(), which does similar work to 
        goog.testing.TestCase.setTestObj()
      - Invokes gTestRunner.setStrict(false) to all 0 tests
      - Invokes goog.testing.TestCase.initializeTestRunner()
      - Invokes gTestRunner.execute()
          ...

  Modifications needed to io_bazel_rules_closure
   - created local repository at $WMH/src/google/rules_closure
     with
       % cd $WMH/src/google
       % git clone https://github.com/bazelbuild/rules_closure.git
       % cd rules_closure
   - modified
      closure/testing/phantomjs_harness.js
       - parse out optional --key=value args before the html file and .js files
       - create query string
       - add query string to url
       - change 'path == VIRTUAL_PAGE' to 'page.startsWith(VIRTUAL_PAGE)'
      closure/testing/phantomjs_test.bzl
       - based on --test_arg, insert values into the 'args' list before
         ctx.file.html.short_path.
       - TODO(wmh): How to get access to --test_arg (and/or --test_env)?
         ctx.configuration.default_shell_env doesn't store --test_env,
         and ctx.configuration.test_env doesn't even exist, contrary to
         https://bazel.build/versions/master/docs/skylark/lib/configuration.html
  """
  __metaclass__ = TestCaseMeta

  # field debug : bool
  #   If True, prints out each invocation of the initializer, setup,
  #   teardown and finalizer methods.

  def debug(self):
    """here"""
    return self._debug

  def debugIs(self, value):
    """here

    Args:
      value: bool
    """
    self._debug = value

  def debugRef(self):
    """here"""
    return self._debug

  # field uid : @str
  #   The name of the method that this instance of TestCase is
  #   responsible for testing. Although the parent initializer also
  #   stores this, each baselang uses a different name for the field.
  #   Rather than encoding this name in each baselang, we just store a
  #   new copy locally.

  def uid(self):
    """here"""
    return self._uid

  def uidIs(self, value):
    """here

    Args:
      value: @str
    """
    self._uid = value

  def uidRef(self):
    """here"""
    return self._uid

  # field tmpfiles : @vec<str>
  #   The collection of temporary files created via tmpFile().

  def tmpfiles(self):
    """here"""
    return self._tmpfiles

  def tmpfilesIs(self, value):
    """here

    Args:
      value: @vec<str>
    """
    self._tmpfiles = value

  def tmpfilesRef(self):
    """here"""
    return self._tmpfiles

  # field tmpdirs : @vec<str>
  #   The collection of temporary dirs created via tmpDir()

  def tmpdirs(self):
    """here"""
    return self._tmpdirs

  def tmpdirsIs(self, value):
    """here

    Args:
      value: @vec<str>
    """
    self._tmpdirs = value

  def tmpdirsRef(self):
    """here"""
    return self._tmpdirs

  # field moxlist : @vec<any>
  #   The collection of mocking objects created via newMox.
  #   TODO(wmh): Rename this something non-python-centric.

  def moxlist(self):
    """here"""
    return self._moxlist

  def moxlistIs(self, value):
    """here

    Args:
      value: @vec<any>
    """
    self._moxlist = value

  def moxlistRef(self):
    """here"""
    return self._moxlist

  # field stdout : ostream
  #   The current stream used for stdout.  If null, the default is used.

  def stdout(self):
    """here"""
    return self._stdout

  def stdoutIs(self, value):
    """here

    Args:
      value: ostream
    """
    self._stdout = value

  def stdoutRef(self):
    """here"""
    return self._stdout

  # field stderr : ostream
  #   The current stream used for stderr.  If null, the default is used.

  def stderr(self):
    """here"""
    return self._stderr

  def stderrIs(self, value):
    """here

    Args:
      value: ostream
    """
    self._stderr = value

  def stderrRef(self):
    """here"""
    return self._stderr

  # field stdin : istream
  #   The current stream used for stdin.  If null, the default is used.

  def stdin(self):
    """here"""
    return self._stdin

  def stdinIs(self, value):
    """here

    Args:
      value: istream
    """
    self._stdin = value

  def stdinRef(self):
    """here"""
    return self._stdin

  # field fsinfo : @map
  #   Maps module names to dicts containing:
  #     module: the module itself
  #     fs: the fake filesystem for the module.

  def fsinfo(self):
    """here"""
    return self._fsinfo

  def fsinfoIs(self, value):
    """here

    Args:
      value: @map
    """
    self._fsinfo = value

  def fsinfoRef(self):
    """here"""
    return self._fsinfo

  # field envars : @map
  #   Records environment variables modified during a test (so they
  #   can be reinstated).

  def envars(self):
    """here"""
    return self._envars

  def envarsIs(self, value):
    """here

    Args:
      value: @map
    """
    self._envars = value

  def envarsRef(self):
    """here"""
    return self._envars

  # field fs : fake_filesystem.FakeFilesystem
  #   Only initialized if SetupSharedFilesystem() is invoked.

  def fs(self):
    """here"""
    return self._fs

  def fsIs(self, value):
    """here

    Args:
      value: fake_filesystem.FakeFilesystem
    """
    self._fs = value

  def fsRef(self):
    """here"""
    return self._fs

  # field stubs : any
  #   Allows us to stub out methods and have them implicitly reverted.

  def stubs(self):
    """here"""
    return self._stubs

  def stubsIs(self, value):
    """here

    Args:
      value: any
    """
    self._stubs = value

  def stubsRef(self):
    """here"""
    return self._stubs

  # field method_name : @str
  #   The name of the method being tested.
  #   TODO(wmh): Redundant in Python and Javascript since the superclass
  #   defines a similar field. Need a way to define 'specific' fields
  #   for only certain baselangs.

  def method_name(self):
    """here"""
    return self._method_name

  def method_nameIs(self, value):
    """here

    Args:
      value: @str
    """
    self._method_name = value

  def method_nameRef(self):
    """here"""
    return self._method_name

  def __init__(self, method_name):
    """here
    In all XUnit testing environments, a TestCase is a class defining
    a collection of test methods (methods starting with 'test') and
    service methods (methods not starting with 'test'). There is a specific
    order of operation for how these TestCases are executed.
     - the meta-level SetUp() method is invoked to perform one time
       initialization of the TestCase.
     - if there are N test methods in the Test Case, N instances of
       TestCase are created
     - for each instance created above:
        - invoke the setUp() method
        - invoke the test method that this instance was created to run
        - invoke the tearDown() method.
     - the finalizers for each instance of TestCase are invoked.
     - the meta-level TearDown() method is invoked to cleanup anything
       done in SetUp()

    The exact names of the setUp, tearDown, SetUp and TearDown methods
    vary across baselangs, which is why the 'lifecycle' construct exists ...
    it knowns the underlying method names that need to be generated in
    each baselang, allowing the user to focus simply on the
    init/setup/teardown/finalize sequence.

    Note that the javascript asserting methods are available in 
      $CLOSURE_ROOT/library/closure/goog-orig/testing/asserts.js
    They are rather odd in having the optional message be the first argument
    of the method (so we have to do some reversal to get the more intuitive
    'optional message as last arg' idiom.

    Note that the 'location' feature attribute of the 'lifecycle' construct
    specifies whether we are referring to an explicit class, the implicit meta
    class associated with an explicit class, or the implicit test class
    associated with an explicit class.  If the class itself has 'location'
    meta, it doesn't make sense to have any of its 'lifecycle' instances
    also have location 'meta' (a meta class does not have a meta class).
    The same is true for 'test' (a test class does not have a test class).
    However, a meta class can have a test class, and a test class has a
    meta class.

    Args:
      method_name: str
        A name for the test case.
        IMPORTANT: Since the Meta compiler implicitly adds a parameter to
        meta lifecycles of testcase classes, it is important that we ...???
    """
    super(TestCase, self).__init__(method_name)
    self._tmpfiles = []
    self._tmpdirs = []
    self._moxlist = []
    self._stdout = None
    self._stderr = None
    self._stdin = None
    self._fsinfo = {}
    self._envars = {}
    self._fs = None
    self._stubs = None
    # User-provided code follows.
    self.debugIs(self.__class__.Debug())
    count = metax.test.TestCase.InstanceCount() + 1
    metax.test.TestCase.InstanceCountIs(count)
    self.uidIs('%s:%d' % (method_name, count))
    self.deblog('Invoking %s initializer for %s' % (self.name(), method_name))
    self.method_nameIs(method_name)

  def status(self):
    """here
    The status of an individual test.


    Returns:
      One of '', 'FAIL' or 'ERROR'.
    """
    # TODO(wmh): This relies on a private method in unittest.TestCase, and
    # is thus inherently fragile. Can we do better?  Also, in python 3.4,
    # the field is _outcomeForDoCleanups. See
    #    https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method
    # for details.  I considered defining the method failureException(msg)
    # in metax.test.TestCase ... this would override the field
    #   self.failureException
    # introduced in unittest.case._AssertRaisesContext and inherited into
    # unittest.TestCase.  The code in case.py almost always uses this
    # field in the form:
    #   raise self.failureException(msg)
    # so defining it as a method that accepts a msg param and always returns
    # AssertionError should work (the method could then set state as
    # desired).  Unfortunately, unittest.TestCase.run() has a single
    # use of the field using
    #    except self.failureException:
    # which wouldn't work properly if it became a method.  But if we were
    # to make self.failureException a property, we could insert some
    # code in addiiton to returning AssertionError. Note that that approach
    # would be much more efficient than the following, which performs
    # O(N) searches thru two lists to find matches. However, the lists will
    # usually be very small (list of failures and errors). Also, the
    # property solution would not capture all failures (for example,
    # _UnexpectedSuccess exceptions).
    text_test_result = self._resultForDoCleanups
    for tst, err in text_test_result.failures:
      if self is tst:
        return 'FAIL'
    for tst, err in text_test_result.errors:
      if self is tst:
        return 'ERROR'
    return ''

  def deblog(self, msg):
    """here
    Print out a Meta specific log message.

    Args:
      msg: &str
    """
    if self.debug():
      print '%s: %s' % (self.uid(), msg)

  def name(self):
    """here
    The name of this testcase.
    See methname for the name of the method within the testcase.
    """
    return self.__class__.__name__

  def methname(self):
    """here
    The name of the method defined within a subclass of TestCase to be
    invoked as the test.

    """
    return self._testMethodName

  def clearMoxes(self):
    """here
    # Unset any Mox instances.
    """
    if self._moxlist:
      for m in self._moxlist:
        m.UnsetStubs()
      self._moxlist = []

  def setenv(self, evar, value):
    """here

    Args:
      evar: str
      value: str
    """
    raise Error('setenv() is not yet working properly (do not use)')
    current = os.environ.get(evar, None)
    if current != ENV.get(evar, None):
      raise Error(
        'Expecting evar = "%s" not "%s"' % (ENV.get(evar, None), current))
    os.environ[evar] = value
    self._envars[evar] = current

  def metaTestPath(self, metafile, *subpaths):
    """here
    Obtain the path of a testdata file within the
    same directory as a specified .meta file.

    TODO(wmh): Javascript does not yet properly handle varargs.

    scope<js>:
      var dirname = metafile.match(/.*//);
      var result = dirname;
      for (var i = 0; i < subpaths.length; ++i) {
        result += '/' + subpaths[i];
      }
      return result;

    Args:
      metafile: str
        The path of the meta file defining the test.
    """
    return os.path.join(os.path.dirname(metafile), *subpaths)

  def captureStdout(self):
    """here
    Capture all subsequent output written to stdout until getStdout() is
    invoked.
    """
    self._stdout = cStringIO.StringIO()
    sys.stdout = self._stdout

  def getStdout(self):
    """here
    Obtain the stdout captured since the last call to captureStdout().
    Resets stdout to what it was before captureStdout() was invoked.
    """
    # TODO(wmh): Use self._stdout to test.
    cls = sys.stdout.__class__
    if cls is TestCase.cStringIOClass or isinstance(sys.stdout, StringIO.StringIO):
      result = sys.stdout.getvalue()
    else:
      result = None
    sys.stdout = TestCase.CanonicalStdout()
    self._stdout = None
    return result

  def captureStderr(self):
    """here
    Capture all subsequent output written to stderr until getStderr() is
    invoked.
    """
    self._stderr = cStringIO.StringIO()
    sys.stderr = self._stderr

  def getStderr(self):
    """here
    Obtain the stderr captured since the last call to captureStderr().
    Resets stdout to what it was before captureStderr() was invoked.
    """
    # TODO(wmh): Use self._stdout to test.
    cls = sys.stderr.__class__
    if cls is TestCase.cStringIOClass or isinstance(sys.stderr, StringIO.StringIO):
      result = sys.stderr.getvalue()
    else:
      result = None
    sys.stderr = TestCase.CanonicalStderr()
    self._stderr = None
    return result

  def newMox(self, *stubs):
    """here
    Return a new mox.Mox, optionally stubbing out various entities.
    """
    # TODO(wmh): EXPERIMENTAL. This is meant to act as a more concise
    # and readable means of mocking out methods (and, perhaps,
    # invoking with emulation). The goal is to be able to pass in
    # objects, and from those objects, obtain the "container" and the
    # "name" of the object within "container", which would then be passed
    # to mox.StubOutWithMock.  However:
    #   - I do not know how to obtain the module object within which
    #     a class 'c' resides.  Note that 'c.__module__' returns the
    #     *name* of the module, not the module object.
    #   - I do not know how to obtain the class object within which
    #     a static function 's' resides.  Note that 's.__class__' returns the
    #     *name* of the class, not the class object.
    #
    # It is very possible this isn't the right solution to the problem of
    # mox readability, but more exploration is warranted.

    m = mox.Mox()

    # We stub out those methods (et.al.) specified in stubs.
    for item in stubs:
      if isinstance(item, tuple) and len(item) == 2:
        obj, name = item
      elif isinstance(item, (types.FunctionType, types.MethodType)):
        obj = item.im_class
        name = item.__name__
      else:
        raise Error('Unrecognized item %s' % item)
      logging.debug('Stubbing out %s within %s', name, obj)
      m.StubOutWithMock(obj, name)

    self._moxlist.append(m)
    return m

  def newStr(self, content=None):
    """here
    Create a new string stream for use anywhere a istream or
    ostream is required.

    Args:
      content: str
    """
    if content:
      result = cStringIO.StringIO(content)
    else:
      result = cStringIO.StringIO()
    return result

  def fp(self, content=None):
    """here
    Create a new string stream for use anywhere a istream or
    ostream is required.

    TODO(wmh): Decide which of 'newStr' or 'fp' to keep.

    Args:
      content: str
    """
    if content is None:
      result = cStringIO.StringIO()
    else:
      result = cStringIO.StringIO(content)
    return result

  def tmpFile(self, create=True):
    """here
    Create a temporary file and return its path.

    Args:
      create: bool
    """
    fd, tmpfile = tempfile.mkstemp()
    os.close(fd)
    self._tmpfiles.append(tmpfile)
    if not create:
      os.unlink(tmpfile)
    return tmpfile

  def tmpDir(self, create=True):
    """here
    Create a temporary directory and return its path.

    Args:
      create: bool
    """
    tmpdir = tempfile.mkdtemp()
    self._tmpdirs.append(tmpdir)
    if not create:
      os.rmdir(tmpdir)
    return tmpdir

  def fileContents(self, path):
    """here
    Return the contents of a specified file.

    Args:
      path: any
    """
    if os.path.exists(path):
      fp = open(path, 'r')
      result = fp.read()
      fp.close()
    else:
      result = None
    return result

  def isInteractive(self):
    """here
    Determine whether this TestCase is marked as supporting tests that
    require interactive responses from a user.
    """
    return TestCase.Interactive()

  def allowNetwork(self, guarding):
    """here
    Determine whether this TestCase is marked s supporting tests that
    require network access.

    Args:
      guarding: any
    """
    result = os.getenv('ALLOW_NETWORK', '') == 'true'
    if not result:
      logging.info('NOT ' + guarding)
    return result

  def setupSharedFilesystem(self, modules, path_specs=None):
    """here
    Configure multiple modules to share the same fake filesystem.

    Args:
      modules: vec
        The modules to configure with the same fake filesystem.
      path_specs: vec
        See SetupFilesystem for details.
    """
    first_module = modules[0]
    fs = self.setupFilesystem(first_module, path_specs=path_specs)
    for module in modules[1:]:
      fs2 = self.setupFilesystem(
          module, path_specs=None, from_module=first_module)
      if fs2 is not fs:
        raise Error("Shared filesystem isn't being shared.")
    self._fs = fs
    return fs

  def setupFilesystem(self, module, path_specs=None, from_module=None):
    """here
    Configure module so that it uses a fake filesystem.

    Raises:
      Error: if the method is called on a module multiple times.
      Error: if from_module is not None and has not been setup.
    Returns fake_filesystem.FakeFilesystem

    Args:
      module: any
        The module to configure.
      path_specs: *vec
        The paths to create. Each element is either a string (path) or
        a two-tuple, with the first element being the path, and the second
        element being a dict of keyword args to send to 
        fake_filesystem.CreateFile().
      from_module: any
        If specified, the faux filesystem objects are obtained from
        the given module, rather than being created anew.  This means
        that the same filesystem objects are shared across multiple
        modules (arguably the most sensible way to test things).
    """
    mname = module.__name__
    fsinfo = self._fsinfo
    if mname in fsinfo:
      raise Error(
          'Attempt to setupFilesystem on %s when it is already setup' %
          mname)

    fsinfo[mname] = {'module': module, 'objs': {}}
    info = fsinfo[mname]

    if from_module:
      oname = from_module.__name__
      if oname not in fsinfo:
        raise Error(
            'Request to setup faux filesystem for module %s based on module %s'
            ' which has not been set up.' % (mname, oname))
      info['objs'] = fsinfo[oname]['objs']
      objs = info['objs']
      fs = objs['fs']
    else:
      fs = fake_filesystem.FakeFilesystem()
      objs = info['objs']
      objs['fs'] = fs
      objs['fcntl'] = FakeFcntl(fs)
      objs['open'] = fake_filesystem.FakeFileOpen(fs)
      objs['os'] = fake_filesystem.FakeOsModule(fs)

    module.open = objs['open']
    for modname in ('os', 'fcntl'):
      if hasattr(module, modname):
        self._stubs.Set(module, modname, objs[modname])
    if path_specs:
      self.populateFilesystem(fs, path_specs)
    return fs

  def populateFilesystem(self, fs, path_specs):
    """here
    Create files within a fake filesystem.

    Raises:
      Error: if an illegal key is passed in path_specs subdata.

    Args:
      fs: fake_filesystem.FakeFilesystem
        The filesystem to populate.
      path_specs: vec
        The paths to create.  If any element is a two-tuple, the
        first element is the path, and the second element is a dict
        containing zero or more of these keys:
          type = str
            One of 'file', 'dir' or 'link'.  Default is 'file'.
          inode = int
            An inode for the file.  Ignored for 'link'.
          perms = int
            The stat.S_IF contant representing the file type.
          contents = str
            The entire contents of the file.
          contents_path = str
            A path to a file to use as the contents of this file.
          size = int
            The size of the file (only if contents or content_path
            are not specified).
          apply_umask = bool
            If True, apply current umask to st_mode
          srcpath = str
            Only valid if type == 'link', specifies the path to which
            the symlink points.
    """
    for path_info in path_specs:
      # path_info can be either:
      #   a) a string (specifies a path to a file)
      #   b) a two-tuple containing string (path of file) and string
      #      (one of 'file', 'dir' or 'link', indicating the file type).
      #   c) a two-tuple containing string (path of file) and dict
      #      where the dict specifies various key/value pairs for
      #      configuring the file.
      if isinstance(path_info, (list, tuple)):
        path, info = path_info
        if isinstance(info, dict):
          in_kwds = info
        else:
          in_kwds = {'type': info}
      else:
        path = path_info
        in_kwds = {}

      # Verify that in_kwds contains only legal keys.
      legal_keys = set([
          'type', 'inode', 'perms', 'contents', 'contents_path', 'size',
          'apply_umask', 'srcpath'])
      for key in in_kwds:
        if key not in legal_keys:
          raise Error(
              "Invalid key '%s' passed to path_specs arg in populateFilesystem"
              % key)

      type_ = in_kwds.get('type', 'file')
      kwds = {}
      if type_ == 'file':
        # Build up a kwds dict suitable for passing to
        # fake_filesystem.FakeFilesystem.CreateFile()
        if 'perms' in in_kwds:
          kwds['st_mode'] = stat.S_IFREG | in_kwds['perms']
        if 'contents_path' in in_kwds:
          kwds['contents'] = self._readFile(in_kwds['contents_path'])
        elif 'contents' in in_kwds:
          kwds['contents'] = in_kwds['contents']
        if 'inode' in in_kwds:
          kwds['inode'] = in_kwds['inode']
        if 'apply_umask' in in_kwds:
          kwds['apply_umask'] = in_kwds['apply_umask']
        kwds['create_missing_dirs'] = True
        fs.CreateFile(path, **kwds)

      elif type_ == 'dir':
        # Build up a kwds dict suitable for passing to
        # fake_filesystem.FakeFilesystem.CreateDir()
        if 'perms' in in_kwds:
          kwds['perm_bits'] = in_kwds['perms']
        if 'inode' in in_kwds:
          kwds['inode'] = in_kwds
        fs.CreateDirectory(path, **kwds)

      elif type_ == 'link':
        # Build up a kwds dict suitable for passing to
        # fake_filesystem.FakeFilesystem.CreateLink()
        if 'srcpath' not in in_kwds:
          raise Error('Request to create a symlink without a src file')
        link_target = in_kwds['srcpath']
        fs.CreateLink(path, link_target)
      else:
        raise Error("Invalid file type '%s'" % type_)

  def fakeFile(self, path):
    """here
    Obtain a fakefile instance.

    Raises:
      Error: If one invokes this method without first invoking
             SetupSharedFilesystem().
    Returns fake_filesystem.FakeFile

    Args:
      path: str
        The path to the file.
    """
    if not self._fs:
      raise Error(
          'Attempt to invoke FakeFile() without first invoking '
          'SetupSharedFilesystem()')
    return self._fs.GetObject(path)

  def fakeFileExists(self, path):
    """here
    Determine if a fake file exists.
    Returns bool

    Args:
      path: str
        The path to the file.
    """
    return self._fs.Exists(path)

  def fakeContents(self, path):
    """here
    Obtain the contents of a fake file.

    Raises:
      Error: If one invokes this method without first invoking
             SetupSharedFilesystem().
    Returns str (file contents)

    Args:
      path: str
        The path to the file.
    """
    return self.fakeFile(path).contents

  def _readFile(self, filename):
    """here
    Obtain contents of a file.
    Returns str

    Args:
      filename: str
        The path to the file.
    """
    with open(filename, 'r') as fp:
      contents = fp.read()
    return contents

  def revertFilesystem(self, module):
    """here
    Undo all stubs to create a faux filesystem.

    Args:
      module: any
    """
    fsinfo = self._fsinfo
    mname = module.__name__
    if mname not in fsinfo:
      raise Error(
          'Attempt to revert filesystem for %s when no filesystem set up'
          % mname)
    del module.open
    del fsinfo[mname]

  def assertDictContains(self, data, subdata):
    """here

    Args:
      data: map
      subdata: map
    """
    for k, v in subdata.iteritems():
      if k not in data:
        self.fail('Failed to find %s in dict' % k)
      elif data[k] != v:
        self.fail('%s = %s != %s' % (k, data[k], v))

  def startswith(self, prefix, strval):
    """here

    Args:
      prefix: str
      strval: str
    """
    self.assertTrue(
      strval.startswith(prefix),
      'String\n  "%s"\ndoes not start with\n  "%s"' % (strval, prefix))

  def endswith(self, suffix, strval):
    """here

    Args:
      suffix: str
      strval: str
    """
    self.assertTrue(
      strval.endswith(suffix),
      'String\n  "%s"\ndoes not end with\n  "%s"' % (strval, suffix))

  def contains(self, member, container, msg=None):
    """here

    Args:
      member: any
      container: any
      msg: str
    """
    self.assertIn(member, container, msg=msg);

  def matches(self, restr, value):
    """here
    A string value matches a regexp. 

    Args:
      restr: str
        The regexp to match against (as a string).
      value: str
        The value to match.
    """
    m = re.match(restr, value)
    if not m:
      self.fail('Expected match failed:\n  %s\n  %s' % (restr, value))

  def iseq(self, expected, item, message=None):
    """here
    Compare an arbitrary two entities for equality (not pointer equality!)

    NOTE: This method may not be implementable in C++. Decide whether we
    want to keep it for use in other baselangs, or if allowing it
    encourages people to use methods that won't work in <cc> and <*>.

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s != %s' % (str(expected), str(item))
    self.assertEqual(expected, item, message)

  def noteq(self, expected, item, message=None):
    """here
    Compare an arbitrary two entities for non-equality (not pointer equality!)

    See comment in 'eq' about viability in C++ and ramifications on this
    method.

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s == %s' % (str(expected), str(item))
    self.assertNotEqual(expected, item, message)

  def iseqstr(self, expected, item, message=None):
    """here
    Compare an arbitrary two entities for equality (not pointer equality!)

    NOTE: This method may not be implementable in C++. Decide whether we
    want to keep it for use in other baselangs, or if allowing it
    encourages people to use methods that won't work in <cc> and <*>.

    Args:
      expected: &str
      item: &str
      message: str
    """
    if message is None:
      message = '%s != %s' % (expected, item)
    self.assertEqual(expected, item, message)

  def noteqstr(self, expected, item, message=None):
    """here
    Compare an arbitrary two entities for non-equality (not pointer equality!)

    Args:
      expected: &str
      item: &str
      message: str
    """
    if message is None:
      message = '%s == %s' % (expected, item)
    self.assertNotEqual(expected, item, message)

  def iseqvec(self, expected, items, message=None):
    """here

    Args:
      expected: vec
      items: vec
      message: str
    """
    self.assertListEqual(expected, items, message)

  def iseqmap(self, expected, data, msg=None, width=30):
    """here

    Args:
      expected: any
      data: any
      msg: any
      width: int
    """
    if expected != data:
      if msg is None:
        msg = '%s != %s' % (expected, data)

      def Trunc(val, width):
        val = str(val)
        if len(val) > width:
          val = val[:width - 1] + '$'
        return val

      form = '%%-10s %%-2s %%-%ds %%-%ds' % (width, width)
      notes = []
      for k in sorted(set(expected.keys() + data.keys())):
        expval = expected[k] if k in expected else '---'
        dval = data[k] if k in data else '---'
        sign = '  ' if (expval == dval) else '!='
        notes.append(
          form % (
            Trunc(k, 10),
            sign,
            Trunc(expval, width + 2),
            Trunc(dval, width + 2)))
      self.fail(msg + '\n' + '\n'.join(notes))

  def iseqtext(self, first, second, text=None):
    """here

    Args:
      first: str
      second: str
      text: str
    """
    self.assertMultiLineEqual(first, second, msg=text)

  def iseqfile(self, file1, file2):
    """here

    Args:
      file1: any
      file2: any
    """
    info = os.system('diff %s %s' % (file1, file2))
    signum = info & 0xff
    status = info >> 8
    self.assertTrue(
      status == 0, 'Files %s and %s differ' % (file1, file2))

  def iseqstrgold(self, content, golden):
    """here

    Args:
      content: any
      golden: any
    """
    if self.WriteGoldens:
      with open(golden, 'w') as fp:
        fp.write(content)
      print 'Wrote %d bytes to golden %s' % (len(content), golden)
    else:
      if True:
        with open(golden, 'r') as fp:
          content2 = fp.read()
          self.assertMultiLineEqual(content, content2)
      else:
        fd, tmpfile = tempfile.mkstemp()
        os.write(fd, content)
        os.close(fd)
        self.iseqfile(golden, tmpfile)
        os.unlink(tmpfile)

  def iseqfilegold(self, path, golden):
    """here

    Args:
      path: any
      golden: any
    """
    if self.WriteGoldens:
      shutil.copyfile(path, golden)
      print 'Copied %s to %s' % (path, golden)
    else:
      self.iseqfile(golden, path)

  def isapprox(self, f1, f2, delta=0.00001, msg=None):
    """here
    Compare two float values for closeness.

    Args:
      f1: double
      f2: double
      delta: double
      msg: str
    """
    self.assertAlmostEqual(f1, f2, delta=delta, msg=msg)

  def islt(self, expected, item, message=None):
    """here

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s >= %s' % (str(expected), str(item))
    self.assertLess(expected, item, message)

  def isle(self, expected, item, message=None):
    """here

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s > %s' % (str(expected), str(item))
    self.assertLessEqual(expected, item, message)

  def isgt(self, expected, item, message=None):
    """here

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s <= %s' % (str(expected), str(item))
    self.assertGreater(expected, item, message)

  def isge(self, expected, item, message=None):
    """here

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s < %s' % (str(expected), str(item))
    self.assertGreaterEqual(expected, item, message)

  def raises(self, eclass, func, *args, **kwds):
    """here
    Confirm that the given method raises an exception.

    Note that the python version accepts arbitrary positional and
    keyword args while the javascript version does not. Need to get 
    varargs supported in javascript before we can try implementing it.

    Args:
      eclass: class
        The exception class raised
      func: &#function
        The callable object
    """
    self.assertRaises(eclass, func, *args, **kwds)

  def issame(self, obj1, obj2):
    """here

    Args:
      obj1: any
      obj2: any
    """
    self.assertTrue(obj1 is obj2, "%s is not %s" % (repr(obj1), repr(obj2)))

  def notsame(self, obj1, obj2):
    """here

    Args:
      obj1: any
      obj2: any
    """
    self.assertFalse(obj1 is obj2, "%s is %s" % (repr(obj1), repr(obj2)))

  def istrue(self, val, msg=None):
    """here
    Note that we cannot use 'true' as a method because that is reserved in
    various languages (and we want a common interface across all languages).

    Args:
      val: bool
      msg: str
    """
    self.assertTrue(val, msg)

  def isfalse(self, val, msg=None):
    """here
    Note that we cannot use 'false' as a method because that is reserved in
    various languages (and we want a common interface across all languages).

    Args:
      val: bool
      msg: str
    """
    self.assertFalse(val, msg)

  def isnull(self, val, msg=None):
    """here
    Confirm the arg is null.

    Args:
      val: any
      msg: str
    """
    self.assertIsNone(val, msg)

  def notnull(self, val, msg=None):
    """here
    Confirm the arg is not null.

    Args:
      val: any
      msg: str
    """
    self.assertIsNotNone(val, msg)

  def isinst(self, obj, cls):
    """here

    Args:
      obj: any
        The object to test.
      cls: any
        The class the object is expected to be an instance of.
        In javascript, this is the constructor function.
    """
    self.istrue(
      isinstance(obj, cls),
      'Expecting %s to be an instance of %s' % (obj, cls))

  def fail(self, msg):
    """here
    # Invoked to indicate an unconditional failure.

    Args:
      msg: str
    """
    super(TestCase, self).fail(msg);

  def meta(self):
    """here"""
    result = self.__class__
    assert result is TestCase
    assert result is MetaTestCase
    return result

  def setUp(self):
    """here"""
    super(TestCase, self).setUp()
    # User-provided code follows.
    self.deblog('Invoking %s setUp for %s' % (self.name(), self.methname()));
    testname = '%s.%s' % (self.name(), self.methname())
    username = re.sub(r'Test\.testx?_?', '.', testname)
    logging.info('Starting ' + testname)

    visname = username[:39] + '$' if len(username) > 40 else username
    sys.stdout.write('%-40s ...' % visname)
    self._start = time.time()
    # NOTE: Most fields have been initialized to their default values within
    # the initializer.
    self._stubs = StubHolder()
    self.maxDiff = None

  @classmethod
  def setUpClass(self):
    """here"""
    super(TestCase, self).setUpClass()
    # User-provided code follows.
    if self.Debug():
      print 'Invoking %s SetUp' % self.__name__

  def tearDown(self):
    """here"""
    # Reinstate I/O
    sys.stdout = TestCase.CanonicalStdout()
    sys.stderr = TestCase.CanonicalStderr()

    seconds = time.time() - self._start
    self.deblog('Invoking %s tearDown for %s' % (self.name(), self.methname()))
    status = self.status()
    sys.stdout.write('%8d us  %s\n' % (seconds * 1000000, status))

    # Clean up moxes
    self.clearMoxes()

    # Remove stubs
    self._stubs.CleanUp()

    # Delete temporary files
    for tmpfile in self._tmpfiles:
      if os.path.exists(tmpfile):
        logging.info('Deleting tmp file %s' % tmpfile)
        os.unlink(tmpfile)
    del self._tmpfiles[:]

    # Delete temporary dirs
    for tmpdir in self._tmpdirs:
      if os.path.exists(tmpdir):
        logging.info('Deleting tmp dir %s' % tmpdir)
        shutil.rmtree(tmpdir)
    del self._tmpdirs[:]

    # Restore filesystem.
    for modinfo in self._fsinfo.values():
      self.revertFilesystem(modinfo['module'])

    # Restore env.vars.
    for evar in self._envars:
      if evar in ENV:
        os.environ[evar] = ENV[evar]
      else:
        del os.environ[evar]
    super(TestCase, self).tearDown()

  @classmethod
  def tearDownClass(self):
    """here"""
    if self.Debug():
      print 'Invoking %s TearDown' % cls.__name__
    super(TestCase, self).tearDownClass()

MetaTestCase = TestCase

# The code needed to run the namespace level tests.
def main():
  import os
  tsd = os.getenv('TEST_SRCDIR', None)
  if tsd is None:
    # This code is NOT being executed via bazel.  In order to ensure that
    # meta.root.Object.Resource() works properly we set an envvar that
    # can be used to determine that we are running unittest code but
    # not in bazel.
    os.environ['IN_UNITTEST'] = 'true'
  else:
    # This code IS being executed via bazel
    pass
  # By passing verbosity=0, we disable unittest.TextTestRunner's default
  # behavior of printing out a '.' (or 'E' or 'F') for each test. Meta
  # provides its own output.
  unittest.main(verbosity=0)
