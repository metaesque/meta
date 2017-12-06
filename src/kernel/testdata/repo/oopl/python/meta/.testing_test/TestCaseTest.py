# Imports for class TestCaseTest
import cStringIO                          # core meta: 635
import os                                 # core meta: 638
import sys                                # core meta: 644
import sys                                # core 
import unittest                           # core meta: 648

import fake_filesystem                    # target meta: 651 target: @pyfakefs//:fake_filesystem
import meta.testing                       # target meta: 632
import meta.testing                       # target meta: 632
import meta.testing_test                  # target 
import mox                                # target meta: 650 target: @moxlib//:main
# End imports for class TestCaseTest


class TestCaseTest(TestCase):
  """Unit tests for class TestCase."""
  __metaclass__ = TestCaseTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(TestCaseTest, self).__init__(meta__name)
    self._tc = None
    # User-provided code follows.

  # field _tc : meta.testing.TestCase

  def tc(self):
    """Returns: meta.testing.TestCase"""
    return self._tc

  def tcIs(self, value):
    """Setter for field tc

    Args:
      value: meta.testing.TestCase

    Returns: meta.testing_test.TestCaseTest
    """
    self._tc = value
    return self

  def setUp(self):
    self._tc = meta.testing.TestCase('captureStdout')
    self._tc.setUp()

  def tearDown(self):
    self._tc.tearDown()

  def test_setenv(self):
    # TODO(wmh): Work on this.
    return

    home = os.getenv('HOME', None)
    self._tc.setenv('HOME', '/home/bob')
    self.assertEqual('/home/bob', os.getenv('HOME', None))
    self._tc.tearDown()
    self.assertEqual(home, os.getenv('HOME', None))

  def test_captureStdout(self):
    self.assertTrue(sys.stdout is meta.testing.TestCase.STDOUT)
    self._tc.captureStdout()
    self.assertTrue(isinstance(sys.stdout, meta.testing.cStringIOClass))
    print 'hello world'
    out = self._tc.getStdout()
    self.assertTrue(sys.stdout is meta.testing.TestCase.STDOUT)
    self.assertEqual('hello world\n', out)

  def test_getStdout(self):
    # noop, tested in test_captureStdout()
    pass

  def test_captureStderr(self):
    self.assertTrue(sys.stderr is meta.testing.TestCase.STDERR)
    self._tc.captureStderr()
    self.assertTrue(isinstance(sys.stderr, meta.testing.cStringIOClass))
    sys.stderr.write('hello world\n')
    err = self._tc.getStderr()
    self.assertTrue(sys.stderr is meta.testing.TestCase.STDERR)
    self.assertEqual('hello world\n', err)

  def test_getStderr(self):
    # noop, tested in test_captureStderr()
    pass

  def test_newMox(self):
    tc = self._tc
    self.assertEqual(0, len(tc._moxlist))

    # Basic mox
    m1 = tc.newMox()
    self.assertEqual(1, len(tc._moxlist))
    m1.UnsetStubs()

    # Another mox, this time with a stub.
    m2 = tc.newMox(tc.tmpFile)
    tc.tmpFile().AndReturn('blah')
    m2.ReplayAll()
    res = tc.tmpFile()
    self.assertEqual('blah', res)
    m2.VerifyAll()

    # TODO(wmh): Add additional code for verifying static and
    # class method stubs?

    # Important to clean up tc here!
    tc.tearDown()

  def test_fp(self):
    pass

  def test_tmpFile(self):
    self.assertEqual([], self._tc._tmpfiles)
    tmpfile = self._tc.tmpFile()
    self.assertEqual([tmpfile], self._tc._tmpfiles)
    self.assertTrue(os.path.exists(tmpfile))
    tmpfile2 = self._tc.tmpFile(create=False)
    self.assertEqual([tmpfile, tmpfile2], self._tc._tmpfiles)
    self.assertFalse(os.path.exists(tmpfile2))
    self._tc.tearDown()
    self.assertFalse(os.path.exists(tmpfile))
    self.assertFalse(os.path.exists(tmpfile2))

  def test_tmpDir(self):
    self.assertEqual([], self._tc._tmpdirs)
    tmpdir = self._tc.tmpDir()
    self.assertEqual([tmpdir], self._tc._tmpdirs)
    self.assertTrue(os.path.exists(tmpdir))
    tmpdir2 = self._tc.tmpDir(create=False)
    self.assertEqual([tmpdir, tmpdir2], self._tc._tmpdirs)
    self.assertFalse(os.path.exists(tmpdir2))
    self._tc.tearDown()
    self.assertFalse(os.path.exists(tmpdir))
    self.assertFalse(os.path.exists(tmpdir2))

  def test_fileContents(self):
    # path = os.path.join(
    #   os.path.dirname('/Users/wmh/src/meta/src/kernel/root.meta'), './testdata/testing/cipherfile')
    path = meta.root.Object.Resource(
      'cipherfile', fqn='meta.testing.TestCase')
    self.assertEqual('aes-128-cbc\ntesting\n', self._tc.fileContents(path))

  def test_isInteractive(self):
    pass

  def test_setupSharedFilesystem(self):
    tc = self._tc
    self.assertEqual(None, tc._fs)

    modules = [meta.testing, sys.modules[__name__]]
    tc.setupSharedFilesystem(
        modules, [('/a/b/c', {'contents': 'blah'})])

    fsinfo = tc._fsinfo
    self.assertEqual(
        ['__main__', 'meta.testing'],
        sorted(fsinfo.keys()))
    self.assertTrue(
      fsinfo['__main__']['objs'] is
      fsinfo['meta.testing']['objs'])
    self.assertNotEqual(None, tc._fs)

  def test_setupFilesystem(self):
    test = self
    # User-provided code follows.
    tc = self._tc
    self.assertEqual({}, tc._fsinfo)
    tc.setupFilesystem(
        meta.testing,
        path_specs=[
            '/home/bob/file1',
            ('/home/bob/file2',
             {'contents': 'hello world\n', 'perms': 0640}),
            ('/home/bob/dir1', 'dir'),
            ('/home/bob/dir2', {'type': 'dir', 'perms': 0755}),
            ('/home/bob/link1',
             {'type': 'link', 'srcpath': '/home/bob/file1'}),
        ])

    # Verify that tc._fsinfo has been augmented.
    self.assertEqual(
        ['meta.testing'],
        tc._fsinfo.keys())

    # Basic test (more thorough testing in testPopulateFilesystem()).
    self.assertEqual(
        True, meta.testing.os.path.exists('/home/bob/file1'))
    stat_info = meta.testing.os.stat('/home/bob/file1')

    self.assertEqual(0, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)
    self.assertEqual(None, tc._fs)

  def test_populateFilesystem(self):
    test = self
    # User-provided code follows.
    tc = self._tc
    self.assertEqual({}, tc._fsinfo)

    if False:
      epath = os.path.join(
        os.path.dirname('/Users/wmh/src/meta/src/kernel/root.meta'),
        './testdata/regexp/entry.mre')
      with open(epath, 'r') as fp:
        contents = fp.read()
    else:
      epath = meta.root.Object.Resource(
        'entry_mre', fqn='meta.testing.TestCase')
      # print '**** HERE with epath=%s' % epath
      with open(epath, 'r') as fp:
        contents = fp.read()

    # We mock out the single call to meta.testing.TestCase._ReadFile() which
    # will be invoked for '/home/bob/file3'
    m = tc.newMox()
    m.StubOutWithMock(tc, '_readFile')
    tc._readFile(mox.IsA(str)).AndReturn(contents)
    m.ReplayAll()

    # Calling SetupFilesystem() will call PopulateFileSystem(), and it is
    # easier to test after fully initializing than to test in isolation.
    tc.setupFilesystem(
        meta.testing,
        path_specs=[
            '/home/bob/file1',
            ('/home/bob/file2',
             {'contents': 'hello world\n', 'perms': 0640}),
            ('/home/bob/dir1', 'dir'),
            ('/home/bob/dir2', {'type': 'dir', 'perms': 0755}),
            ('/home/bob/link1',
             {'type': 'link', 'srcpath': '/home/bob/file1'}),
            ('/home/bob/file3',
             {'contents_path': epath}),
        ])
    package = 'meta.testing'
    self.assertTrue(package in tc._fsinfo)
    self.assertTrue(meta.testing is tc._fsinfo[package]['module'])
    for k in ('fs', 'open', 'os', 'fcntl'):
      self.assertTrue(k in tc._fsinfo[package]['objs'])

    # file1 is a file with no content.
    self.assertEqual(
        True, meta.testing.os.path.exists('/home/bob/file1'))
    stat_info = meta.testing.os.stat('/home/bob/file1')
    self.assertEqual(0, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    # file2 is a file with content.
    fp = meta.testing.open('/home/bob/file2', 'r')
    self.assertEqual('hello world\n', fp.read())
    fp.close()
    stat_info = meta.testing.os.stat('/home/bob/file2')
    self.assertEqual('100640', '%o' % stat_info.st_mode)

    # dir1 is a directory with default permissions.
    self.assertEqual(
        True, meta.testing.os.path.isdir('/home/bob/dir1'))
    stat_info = meta.testing.os.stat('/home/bob/dir1')
    self.assertEqual('40777', '%o' % stat_info.st_mode)

    # dir2 is a directory with specific permissions.
    self.assertEqual(
        True, meta.testing.os.path.isdir('/home/bob/dir2'))
    stat_info = meta.testing.os.stat('/home/bob/dir2')
    self.assertEqual('40755', '%o' % stat_info.st_mode)

    # link1 is a symlink to file1
    stat_info = meta.testing.os.stat('/home/bob/link1')
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    # file3 has content initialized from a file.
    self.assertEqual(
        True, meta.testing.os.path.exists('/home/bob/file3'))
    stat_info = meta.testing.os.stat('/home/bob/file3')
    self.assertEqual(28, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    m.VerifyAll()

  def test_fakeFile(self):
    tc = self._tc

    # If we don't first call SetupSharedFilesystem, FakeFile() is an error.
    self.assertRaises(meta.testing.Error, tc.fakeFile, '/any/path')

    fs = tc.setupSharedFilesystem(
        [meta.testing], [('/a/b/c', {'contents': 'blah'})])
    fake = tc.fakeFile('/a/b/c')
    self.assertTrue(isinstance(fake, fake_filesystem.FakeFile))
    self.assertEqual('blah', fake.contents)

  def test_fakeFileExists(self):
    pass

  def test_fakeContents(self):
    tc = self._tc

    # If we don't first call SetupSharedFilesystem, FakeContent() is an error.
    self.assertRaises(meta.testing.Error, tc.fakeContents, '/any/path')

    fs = tc.setupSharedFilesystem(
        [meta.testing], [('/a/b/c', {'contents': 'blah'})])
    self.assertEqual('blah', tc.fakeContents('/a/b/c'))

  def test__readFile(self):
    pass

  def test_revertFilesystem(self):
    tc = self._tc
    mname = meta.testing.__name__
    self.assertFalse(mname in tc._fsinfo)
    unused_fs = tc.setupFilesystem(meta.testing)
    self.assertTrue(mname in tc._fsinfo)
    tc.revertFilesystem(meta.testing)
    self.assertFalse(mname in tc._fsinfo)

  def test_startswith(self):
    pass
