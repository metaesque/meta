"""# Defines the front-ends"""
import StringIO
import cStringIO
import fcntl
import logging
import os
import pprint
import shutil
import stat
import sys
import tempfile
import types
import unittest

import fake_filesystem
import meta.root
import meta.testing
import mox

import cStringIO
cStringIOClass = cStringIO.StringIO().__class__
import copy
ENV = copy.copy(os.environ)


class TestCase(unittest.TestCase):
  """Every meta-generated class in every base language has an associated
  test class for testing the methods within the class. The test class
  inherits (directly or indirectly) from this class, meta.testing.TestCase.
  """

  STDOUT = sys.stdout
  STDERR = sys.stderr

  # Set this to True to enable interactive unit tests.
  Interactive = False

  # Set this to True to write golden files instead of comparing them.
  WriteGoldens = os.getenv('WRITE_GOLDENS', '') == 'true'

  def metaTestPath(self, metafile, *subpaths):
    """Obtain the path of a testdata file within the
    same directory as a specified .meta file.

    Args:
      metafile: str
        The path of the meta file defining the test.
      subpaths: *list
        The path within the directory containing the
        metafile.

    Returns: str
    """
    return os.path.join(os.path.dirname(metafile), *subpaths)

  @classmethod
  def Resource(cls, resource_id, fqn=None):
    """This method provides an interface by which a user an obtain a
    resource that was defined via the 'resource' construct within
    the 'assocs' attribute of a class.  Having this be a meta method allows
    us to:
     - store the links in class-specific directories without worrying that
       invocation from a subclass will break the naming.
     - allows resources from one class to be accessed from another class
     - will work with non-meta classes (assuming the non-meta BUILD
       files are properly defined).

    Args:
      resource_id: str
        The id of the resource (that is, the value of the primary attribute
        of the 'resource' construct that defines the resource.
      fqn: *str
        The fully qualified name of the class for which resources are
        desired.  If null, uses the receiver cls to determine fqn.

    Returns: str
    """
    return meta.root.Object.Resource(resource_id, fqn=fqn, test=True)

  def setUp(self):
    """no docstr"""
    super(TestCase, self).setUp()
    self._tmpfiles = []
    self._tmpdirs = []
    self._moxlist = []
    self._stdout = None
    self._stderr = None
    self._stdin = None

    # field fsinfo: dict
    #   Maps module names to dicts containing:
    #     module: the module itself
    #     fs: the fake filesystem for the module.
    self._fsinfo = {}

    # field fs: fake_filesystem.FakeFilesystem or None
    #   Only initialized if SetupSharedFilesystem() is invoked.
    self._fs = None

    # field stubs:
    #   Allows us to stub out methods and have them implicitly reverted.
    self._stubs = StubHolder()

    # field envars: dict
    #   Records environment variables modified during a test (so they
    #   can be reinstated.
    self._envars = {}

  def tearDown(self):
    """no docstr"""
    super(TestCase, self).tearDown()

    # Clean up moxes
    self.clearMoxes()

    # Remove stubs
    self._stubs.CleanUp()

    # Delete temporary files
    sys.stdout = TestCase.STDOUT
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

  def clearMoxes(self):
    """no docstr"""
    if self._moxlist:
      for m in self._moxlist:
        m.UnsetStubs()
      self._moxlist = []

  def setenv(self, evar, value):
    """no docstr

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

  def captureStdout(self):
    """no docstr"""
    self._stdout = cStringIO.StringIO()
    sys.stdout = self._stdout

  def getStdout(self):
    """no docstr"""
    # TODO(wmh): Use self._stdout to test.
    cls = sys.stdout.__class__
    if cls is cStringIOClass or isinstance(sys.stdout, StringIO.StringIO):
      result = sys.stdout.getvalue()
    else:
      result = None
    sys.stdout = TestCase.STDOUT
    self._stdout = None
    return result

  def captureStderr(self):
    """no docstr"""
    self._stderr = cStringIO.StringIO()
    sys.stderr = self._stderr

  def getStderr(self):
    """no docstr"""
    # TODO(wmh): Use self._stdout to test.
    cls = sys.stderr.__class__
    if cls is cStringIOClass or isinstance(sys.stderr, StringIO.StringIO):
      result = sys.stderr.getvalue()
    else:
      result = None
    sys.stderr = TestCase.STDERR
    self._stderr = None
    return result

  def newMox(self, *stubs):
    """Return a new mox.Mox, optionally stubbing out various entities.

    Args:
      stubs: *list
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
    """no docstr

    Args:
      content: any
    """
    if content:
      result = cStringIO.StringIO(content)
    else:
      result = cStringIO.StringIO()
    return result

  def tmpFile(self, create=True):
    """no docstr

    Args:
      create: any
    """
    fd, tmpfile = tempfile.mkstemp()
    os.close(fd)
    self._tmpfiles.append(tmpfile)
    if not create:
      os.unlink(tmpfile)
    return tmpfile

  def tmpDir(self, create=True):
    """no docstr

    Args:
      create: any
    """
    tmpdir = tempfile.mkdtemp()
    self._tmpdirs.append(tmpdir)
    if not create:
      os.rmdir(tmpdir)
    return tmpdir

  def fileContents(self, path):
    """no docstr

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

  def fp(self, content=None):
    """no docstr

    Args:
      content: any
    """
    if content is None:
      result = cStringIO.StringIO()
    else:
      result = cStringIO.StringIO(content)
    return result

  def isInteractive(self):
    """no docstr"""
    return TestCase.Interactive

  def assertFileEqual(self, file1, file2):
    """no docstr

    Args:
      file1: any
      file2: any
    """
    info = os.system('diff %s %s' % (file1, file2))
    signum = info & 0xff
    status = info >> 8
    self.assertTrue(
      status == 0, 'Files %s and %s differ' % (file1, file2))

  def assertDictContains(self, data, subdata):
    """no docstr

    Args:
      data: *dict
      subdata: *dict
    """
    for k, v in subdata.iteritems():
      if k not in data:
        self.fail('Failed to find %s in dict' % k)
      elif data[k] != v:
        self.fail('%s = %s != %s' % (k, data[k], v))

  def assertFloatEqual(self, f1, f2, delta=0.00001):
    """no docstr

    Args:
      f1: any
      f2: any
      delta: any
    """
    self.assertTrue(
      abs(f1 - f2) <= delta,
      '|%f - %f| = %f > %f' % (f1, f2, abs(f1 - f2), delta))

  def compareStrToGolden(self, content, golden):
    """no docstr

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
        self.assertFileEqual(golden, tmpfile)
        os.unlink(tmpfile)

  def compareFileToGolden(self, path, golden):
    """no docstr

    Args:
      path: any
      golden: any
    """
    if self.WriteGoldens:
      shutil.copyfile(path, golden)
      print 'Copied %s to %s' % (path, golden)
    else:
      self.assertFileEqual(golden, path)

  def assertStartsWith(self, strval, prefix):
    """no docstr

    Args:
      strval: any
      prefix: any
    """
    self.assertTrue(
      strval.startswith(prefix),
      'String\n  "%s"\ndoes not start with\n  "%s"' % (strval, prefix))

  def assertEndsWith(self, strval, suffix):
    """no docstr

    Args:
      strval: any
      suffix: any
    """
    self.assertTrue(
      strval.endswith(suffix),
      'String\n  "%s"\ndoes not end with\n  "%s"' % (strval, suffix))

  def assertContains(self, strval, text):
    """no docstr

    Args:
      strval: any
      text: any
    """
    self.assertTrue(
      text in strval,
      'String\n  "%s"\ndoes not contain\n  "%s"' % (strval, text))

  def setupSharedFilesystem(self, modules, path_specs=None):
    """Configure multiple modules to share the same fake filesystem.

    Args:
      modules: *list of module
        The modules to configure with the same fake filesystem.
      path_specs: *list
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
    """Configure module so that it uses a fake filesystem.

    Raises:
      Error: if the method is called on a module multiple times.
      Error: if from_module is not None and has not been setup.
    Returns fake_filesystem.FakeFilesystem

    Args:
      module: module
        The module to configure.
      path_specs: *list of {str_or_two-tuple_(str/_dict)}
        The paths to create.  If any element is a two-tuple, the
        first element is the path, and the second element is a dict
        of keyword args to send to fake_filesystem.CreateFile().
      from_module: *module
        If specified, the faux filesystem objects are obtained from
        the given module, rather than being created anew.  This means
        that the same filesystem objects are shared across multiple
        modules (arguably the most sensible way to test things).

    Returns: any
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
    """Create files within a fake filesystem.

    Raises:
      Error: if an illegal key is passed in path_specs subdata.

    Args:
      fs: fake_filesystem.FakeFilesystem
        The filesystem to populate.
      path_specs: *list of {str_or_two-tuple_(str/_dict)}
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
    """Obtain a fakefile instance.

    Raises:
      Error: If one invokes this method without first invoking
             SetupSharedFilesystem().
    Returns fake_filesystem.FakeFile

    Args:
      path: str
        The path to the file.

    Returns: any
    """
    if not self._fs:
      raise Error(
          'Attempt to invoke FakeFile() without first invoking '
          'SetupSharedFilesystem()')
    return self._fs.GetObject(path)

  def fakeFileExists(self, path):
    """Determine if a fake file exists.
    Returns bool

    Args:
      path: str
        The path to the file.

    Returns: any
    """
    return self._fs.Exists(path)

  def fakeContents(self, path):
    """Obtain the contents of a fake file.


    Raises:
      Error: If one invokes this method without first invoking
             SetupSharedFilesystem().
    Returns str (file contents)

    Args:
      path: str
        The path to the file.

    Returns: any
    """
    return self.fakeFile(path).contents

  def _readFile(self, filename):
    """Obtain contents of a file.
    Returns str

    Args:
      filename: str
        The path to the file.

    Returns: any
    """
    with open(filename, 'r') as fp:
      contents = fp.read()
    return contents

  def revertFilesystem(self, module):
    """no docstr

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

  def allowNetwork(self, guarding):
    """Used to guard tests that access the network.

    Args:
      guarding: any
    """
    result = os.getenv('ALLOW_NETWORK', '') == 'true'
    if not result:
      logging.info('NOT ' + guarding)
    return result

  def equal(self, expected, item, message=None):
    """no docstr

    Args:
      expected: any
      item: any
      message: any
    """
    if message is None:
      message = '%s != %s' % (str(expected), str(item))
    self.assertEqual(expected, item, message)

  def floatEqual(self, f1, f2, delta=0.00001):
    """no docstr

    Args:
      f1: any
      f2: any
      delta: any
    """
    return self.assertFloatEqual(f1, f2, delta=delta)

  def dictEqual(self, expected, data, message=None):
    """no docstr

    Args:
      expected: any
      data: any
      message: any
    """
    if expected != data:
      if message is None:
        message = '%s != %s' % (expected, data)

      def Trunc(val, width):
        val = str(val)
        if len(val) > width:
          val = val[:width - 1] + '$'
        return val

      notes = []
      for k in sorted(set(expected.keys() + data.keys())):
        expval = expected[k] if k in expected else '---'
        dval = data[k] if k in data else '---'
        sign = '  ' if (expval == dval) else '!='
        notes.append(
          '%-10s %-2s %-30s %-30s' %
          (Trunc(k, 10), sign, Trunc(expval, 32), Trunc(dval, 32)))
      self.fail(message + '\n' + '\n'.join(notes))

  def contains(self, container, element, *args):
    """no docstr

    Args:
      container: any
      element: any
      args: *list
    """
    # If container is str, element is str (a substr to look for)
    # If container is of type list, tuple, dict, etc, element is an instance
    # to search for in the container.
    self.assertTrue(element in container, *args)

  def equalText(self, *args, **kwds):
    """no docstr

    Args:
      args: *list
      kwds: *dict
    """
    self.assertMultiLineEqual(*args, **kwds)

  def raises(self, *args, **kwds):
    """no docstr

    Args:
      args: *list
      kwds: *dict
    """
    self.assertRaises(*args, **kwds)

  def identical(self, obj1, obj2):
    """no docstr

    Args:
      obj1: any
      obj2: any
    """
    self.assertTrue(obj1 is obj2, "%s is not %s" % (repr(obj1), repr(obj2)))

  def istrue(self, val, msg=None):
    """Note that we cannot use 'true' as a method because that is reserved in
    various languages (and we want a common interface across all languages).

    Args:
      val: bool
      msg: str
    """
    self.assertTrue(val, msg)

  def isfalse(self, val, msg=None):
    """Note that we cannot use 'false' as a method because that is reserved in
    various languages (and we want a common interface across all languages).

    Args:
      val: bool
      msg: str
    """
    self.assertFalse(val, msg)

  def instance(self, obj, cls):
    """no docstr

    Args:
      obj: any
      cls: any
    """
    self.assertTrue(
      isinstance(obj, cls),
      'Expecting %s to be an instance of %s' % (obj, cls))

  def endswith(self, expected, text):
    """no docstr

    Args:
      expected: any
      text: any
    """
    self.assertTrue(
      text.endswith(expected),
      'Expecting\n  %s\nto end with\n  %s' % (text, expected))


class Meta__TestCase(meta.root.Object):
  """Meta class of TestCase."""

  def Resource(self, resource_id, fqn=None):
    """This method provides an interface by which a user an obtain a
    resource that was defined via the 'resource' construct within
    the 'assocs' attribute of a class.  Having this be a meta method allows
    us to:
     - store the links in class-specific directories without worrying that
       invocation from a subclass will break the naming.
     - allows resources from one class to be accessed from another class
     - will work with non-meta classes (assuming the non-meta BUILD
       files are properly defined).

    Args:
      resource_id: str
        The id of the resource (that is, the value of the primary attribute
        of the 'resource' construct that defines the resource.
      fqn: *str
        The fully qualified name of the class for which resources are
        desired.  If null, uses the receiver cls to determine fqn.

    Returns: str
    """
    return meta.root.Object.Resource(resource_id, fqn=fqn, test=True)


class FakeFcntl(object):
  """A fake fcntl object."""

  LOCK_UN = fcntl.LOCK_UN
  LOCK_SH = fcntl.LOCK_SH
  LOCK_EX = fcntl.LOCK_EX

  # instance field _filesystem : any
  def filesystem(self): return self._filesystem
  def filesystemIs(self, value): self._filesystem = value; return self
  def filesystemRef(self): return self._filesystem

  def __init__(self, fs):
    """Initializer.

    Args:
      fs: any
    """
    super(FakeFcntl, self).__init__()
    # User-provided code follows.
    self._filesystem = fs

  def fcntl(self, fd, op, arg=0):
    """no docstr

    Args:
      fd: any
      op: any
      arg: any
    """
    pass

  def ioctl(self, fd, op, arg=0, mutate_flag=False):
    """no docstr

    Args:
      fd: any
      op: any
      arg: any
      mutate_flag: any
    """
    pass

  def flock(self, fd, op):
    """no docstr

    Args:
      fd: any
      op: any
    """
    pass

  def lockf(self, fd, op, length=0, start=0, whence=0):
    """no docstr

    Args:
      fd: any
      op: any
      length: any
      start: any
      whence: any
    """
    pass


class Meta__FakeFcntl(meta.root.Object):
  """Meta class of FakeFcntl."""
  pass


class StubHolder(object):
  """Support class for stubbing methods out for unit testing.

  Sample Usage:

  You want os.path.exists() to always return true during testing.

     stubs = StubHolder()
     stubs.Set(os.path, 'exists', lambda x: 1)
       ...
     stubs.CleanUp()

  The above changes os.path.exists into a lambda that returns 1.  Once
  the ... part of the code finishes, the CleanUp() looks up the old
  value of os.path.exists and restores it.
  """

  def __init__(self):
    """Initializer."""
    super(StubHolder, self).__init__()
    # User-provided code follows.
    self.cache = []
    self.stubs = []

  def __del__(self):
    """Do not rely on the destructor to undo your stubs.

    You cannot guarantee exactly when the destructor will get called without
    relying on implementation details of a Python VM that may change.
    """
    self.CleanUp()

  def __enter__(self):
    """no docstr"""
    return self

  def __exit__(self, unused_exc_type, unused_exc_value, unused_tb):
    """no docstr

    Args:
      unused_exc_type: any
      unused_exc_value: any
      unused_tb: any
    """
    self.CleanUp()

  def CleanUp(self):
    """Undoes all SmartSet() & Set() calls, restoring original definitions."""
    self.SmartUnsetAll()
    self.UnsetAll()

  def SmartSet(self, obj, attr_name, new_attr):
    """Replace obj.attr_name with new_attr.

    This method is smart and works at the module, class, and instance level
    while preserving proper inheritance. It will not stub out C types however
    unless that has been explicitly allowed by the type.

    This method supports the case where attr_name is a staticmethod or a
    classmethod of obj.

    Notes:
     - If obj is an instance, then it is its class that will actually be
       stubbed. Note that the method Set() does not do that: if obj is
       an instance, it (and not its class) will be stubbed.
     - The stubbing is using the builtin getattr and setattr. So, the __get__
       and __set__ will be called when stubbing.

    Raises:
      AttributeError: If the attribute cannot be found.

    Args:
      obj: any
        The object whose attributes we want to modify.
      attr_name: str
        The name of the attribute to modify.
      new_attr: any
        The new value for the attribute.
    """
    if (inspect.ismodule(obj) or
        (not inspect.isclass(obj) and attr_name in obj.__dict__)):
      orig_obj = obj
      orig_attr = getattr(obj, attr_name)
    else:
      if not inspect.isclass(obj):
        mro = list(inspect.getmro(obj.__class__))
      else:
        mro = list(inspect.getmro(obj))

      mro.reverse()

      orig_attr = None
      found_attr = False

      for cls in mro:
        try:
          orig_obj = cls
          orig_attr = getattr(obj, attr_name)
          found_attr = True
        except AttributeError:
          continue

      if not found_attr:
        raise AttributeError('Attribute not found.')

    # Calling getattr() on a staticmethod transforms it to a 'normal' function.
    # We need to ensure that we put it back as a staticmethod.
    old_attribute = obj.__dict__.get(attr_name)
    if old_attribute is not None and isinstance(old_attribute, staticmethod):
      orig_attr = staticmethod(orig_attr)

    self.stubs.append((orig_obj, attr_name, orig_attr))
    setattr(orig_obj, attr_name, new_attr)

  def SmartUnsetAll(self):
    """Reverses SmartSet() calls, restoring things to original definitions.

    This method is automatically called when the StubOutForTesting()
    object is deleted; there is no need to call it explicitly.

    It is okay to call SmartUnsetAll() repeatedly, as later calls have
    no effect if no SmartSet() calls have been made.
    """
    for args in reversed(self.stubs):
      setattr(*args)

    self.stubs = []

  def Set(self, parent, child_name, new_child):
    """In parent, replace child_name's old definition with new_child.

    The parent could be a module when the child is a function at
    module scope.  Or the parent could be a class when a class' method
    is being replaced.  The named child is set to new_child, while the
    prior definition is saved away for later, when UnsetAll() is
    called.

    This method supports the case where child_name is a staticmethod or a
    classmethod of parent.

    Args:
      parent: *any
        The_context_in_which_the_attribute_child_name_is_to_be_changed.
      child_name: *any
        The_name_of_the_attribute_to_change.
      new_child: *any
        The_new_value_of_the_attribute
    """
    old_child = getattr(parent, child_name)

    old_attribute = parent.__dict__.get(child_name)
    if old_attribute is not None and isinstance(old_attribute, staticmethod):
      old_child = staticmethod(old_child)

    self.cache.append((parent, old_child, child_name))
    setattr(parent, child_name, new_child)

  def UnsetAll(self):
    """Reverses Set() calls, restoring things to their original definitions.

    This method is automatically called when the StubOutForTesting()
    object is deleted; there is no need to call it explicitly.

    It is okay to call UnsetAll() repeatedly, as later calls have no
    effect if no Set() calls have been made.
    """
    # Undo calls to Set() in reverse order, in case Set() was called on the
    # same arguments repeatedly (want the original call to be last one undone)
    for (parent, old_child, child_name) in reversed(self.cache):
      setattr(parent, child_name, old_child)
    self.cache = []


class Meta__StubHolder(meta.root.Object):
  """Meta class of StubHolder."""
  pass

def main():
  unittest.main()
