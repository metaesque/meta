"""Auto-generated test namespace for metax.test."""
import metax.test
import metax.test_test


class FakeFcntlTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class FakeFcntlTest"""


class FakeFcntlTest(metax.test.TestCase):
  """Auto-generated test class for metax.test.FakeFcntl"""
  __metaclass__ = FakeFcntlTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_fcntl(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_ioctl(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_flock(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_lockf(self):
    """here"""
    # noop
    # TODO(wmh): Is there a way to verify this method does nothing?
    pass

  def test_meta(self):
    """here"""
    # noop
    pass


class FakeFcntlMetaTest(metax.test.TestCase):
  """Auto-generated test class for auto-generated meta class metax.test.FakeFcntlMeta."""

  def test___init__(self):
    """here"""
    pass


class StubHolderTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class StubHolderTest"""


class StubHolderTest(metax.test.TestCase):
  """Auto-generated test class for metax.test.StubHolder"""
  __metaclass__ = StubHolderTestMeta

  def test___init__(self):
    """here"""
    pass

  def test___del__(self):
    """here"""
    pass

  def test___enter__(self):
    """here"""
    pass

  def test___exit__(self):
    """here"""
    pass

  def test_CleanUp(self):
    """here"""
    pass

  def test_SmartSet(self):
    """here"""
    pass

  def test_SmartUnsetAll(self):
    """here"""
    pass

  def test_Set(self):
    """here"""
    pass

  def test_UnsetAll(self):
    """here"""
    pass

  def test_meta(self):
    """here"""
    # noop
    pass


class StubHolderMetaTest(metax.test.TestCase):
  """Auto-generated test class for auto-generated meta class metax.test.StubHolderMeta."""


class TestCaseTestMeta(metax.test.TestCaseMeta):
  """Auto-generated meta class for auto-generated test class TestCaseTest"""


class TestCaseTest(metax.test.TestCase):
  """Auto-generated test class for metax.test.TestCase"""
  __metaclass__ = TestCaseTestMeta

  def test___init__(self):
    """here"""
    pass

  def test_setUp(self):
    """here"""
    print "metax.self.TestCase.setUp does not yet have a unittest"

  def test_setUpClass(self):
    """here"""
    print "metax.self.TestCase.setUpClass does not yet have a unittest"

  def test_tearDown(self):
    """here"""
    print "metax.self.TestCase.tearDown does not yet have a unittest"

  def test_tearDownClass(self):
    """here"""
    print "metax.self.TestCase.tearDownClass does not yet have a unittest"

  def test_status(self):
    """here"""
    print "metax.self.TestCase.status does not yet have a unittest"

  def test_deblog(self):
    """here"""
    print "metax.self.TestCase.deblog does not yet have a unittest"

  def test_name(self):
    """here"""
    print "metax.self.TestCase.name does not yet have a unittest"

  def test_methname(self):
    """here"""
    print "metax.self.TestCase.methname does not yet have a unittest"

  def test_clearMoxes(self):
    """here"""
    print "metax.self.TestCase.clearMoxes does not yet have a unittest"

  def test_setenv(self):
    """here"""
    # TODO(wmh): Work on this.
    return

    home = os.getenv('HOME', None)
    self._tc.setenv('HOME', '/home/bob')
    self.assertEqual('/home/bob', os.getenv('HOME', None))
    self._tc.tearDown()
    self.assertEqual(home, os.getenv('HOME', None))

  def test_metaTestPath(self):
    """here"""
    print "metax.self.TestCase.metaTestPath does not yet have a unittest"

  def test_captureStdout(self):
    """here"""
    self.assertTrue(sys.stdout is metax.self.TestCase.CanonicalStdout())
    self._tc.captureStdout()
    self.assertTrue(isinstance(sys.stdout, metax.self.cStringIOClass))
    print 'hello world'
    out = self._tc.getStdout()
    self.assertTrue(sys.stdout is metax.self.TestCase.CanonicalStdout())
    self.assertEqual('hello world\n', out)

  def test_getStdout(self):
    """here"""
    # noop, tested in test_captureStdout()
    pass

  def test_captureStderr(self):
    """here"""
    self.assertTrue(sys.stderr is metax.self.TestCase.CanonicalStderr())
    self._tc.captureStderr()
    self.assertTrue(isinstance(sys.stderr, metax.self.cStringIOClass))
    sys.stderr.write('hello world\n')
    err = self._tc.getStderr()
    self.assertTrue(sys.stderr is metax.self.TestCase.CanonicalStderr())
    self.assertEqual('hello world\n', err)

  def test_getStderr(self):
    """here"""
    # noop, tested in test_captureStderr()
    pass

  def test_newMox(self):
    """here"""
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

  def test_newStr(self):
    """here"""
    print "metax.self.TestCase.newStr does not yet have a unittest"

  def test_fp(self):
    """here"""
    pass

  def test_tmpFile(self):
    """here"""
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
    """here"""
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
    """here"""
    # path = os.path.join(
    #   os.path.dirname(__metafile__), './testdata/testing/cipherfile')
    path = metax.root.Object.Resource(
      'cipherfile', fqn='metax.self.TestCase')
    self.assertEqual('aes-128-cbc\ntesting\n', self._tc.fileContents(path))

  def test_isInteractive(self):
    """here"""
    pass

  def test_allowNetwork(self):
    """here"""
    print "metax.self.TestCase.allowNetwork does not yet have a unittest"

  def test_setupSharedFilesystem(self):
    """here"""
    tc = self._tc
    self.assertEqual(None, tc._fs)

    modules = [metax.test, sys.modules[__name__]]
    tc.setupSharedFilesystem(
        modules, [('/a/b/c', {'contents': 'blah'})])

    fsinfo = tc._fsinfo
    self.assertEqual(
        ['__main__', 'metax.test'],
        sorted(fsinfo.keys()))
    self.assertTrue(
      fsinfo['__main__']['objs'] is
      fsinfo['metax.test']['objs'])
    self.assertNotEqual(None, tc._fs)

  def test_setupFilesystem(self):
    """here"""
    tc = self._tc
    self.assertEqual({}, tc._fsinfo)
    tc.setupFilesystem(
        metax.test,
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
        ['metax.test'],
        tc._fsinfo.keys())

    # Basic test (more thorough testing in testPopulateFilesystem()).
    self.assertEqual(
        True, metax.self.os.path.exists('/home/bob/file1'))
    stat_info = metax.self.os.stat('/home/bob/file1')

    self.assertEqual(0, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)
    self.assertEqual(None, tc._fs)

  def test_populateFilesystem(self):
    """here"""
    tc = self._tc
    self.assertEqual({}, tc._fsinfo)

    if False:
      epath = os.path.join(
        os.path.dirname(__metafile__),
        './testdata/regexp/entry.mre')
      with open(epath, 'r') as fp:
        contents = fp.read()
    else:
      epath = meta.root.Object.Resource(
        'entry_mre', fqn='metax.self.TestCase')
      # print '**** HERE with epath=%s' % epath
      with open(epath, 'r') as fp:
        contents = fp.read()

    # We mock out the single call to metax.self.TestCase._ReadFile() which
    # will be invoked for '/home/bob/file3'
    m = tc.newMox()
    m.StubOutWithMock(tc, '_readFile')
    tc._readFile(mox.IsA(str)).AndReturn(contents)
    m.ReplayAll()

    # Calling SetupFilesystem() will call PopulateFileSystem(), and it is
    # easier to test after fully initializing than to test in isolation.
    tc.setupFilesystem(
        metax.test,
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
    package = 'metax.test'
    self.assertTrue(package in tc._fsinfo)
    self.assertTrue(metax.test is tc._fsinfo[package]['module'])
    for k in ('fs', 'open', 'os', 'fcntl'):
      self.assertTrue(k in tc._fsinfo[package]['objs'])

    # file1 is a file with no content.
    self.assertEqual(
        True, metax.self.os.path.exists('/home/bob/file1'))
    stat_info = metax.self.os.stat('/home/bob/file1')
    self.assertEqual(0, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    # file2 is a file with content.
    fp = metax.self.open('/home/bob/file2', 'r')
    self.assertEqual('hello world\n', fp.read())
    fp.close()
    stat_info = metax.self.os.stat('/home/bob/file2')
    self.assertEqual('100640', '%o' % stat_info.st_mode)

    # dir1 is a directory with default permissions.
    self.assertEqual(
        True, metax.self.os.path.isdir('/home/bob/dir1'))
    stat_info = metax.self.os.stat('/home/bob/dir1')
    self.assertEqual('40777', '%o' % stat_info.st_mode)

    # dir2 is a directory with specific permissions.
    self.assertEqual(
        True, metax.self.os.path.isdir('/home/bob/dir2'))
    stat_info = metax.self.os.stat('/home/bob/dir2')
    self.assertEqual('40755', '%o' % stat_info.st_mode)

    # link1 is a symlink to file1
    stat_info = metax.self.os.stat('/home/bob/link1')
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    # file3 has content initialized from a file.
    self.assertEqual(
        True, metax.self.os.path.exists('/home/bob/file3'))
    stat_info = metax.self.os.stat('/home/bob/file3')
    self.assertEqual(28, stat_info.st_size)
    self.assertEqual('100666', '%o' % stat_info.st_mode)

    m.VerifyAll()

  def test_fakeFile(self):
    """here"""
    tc = self._tc

    # If we don't first call SetupSharedFilesystem, FakeFile() is an error.
    self.assertRaises(metax.self.Error, tc.fakeFile, '/any/path')

    fs = tc.setupSharedFilesystem(
        [metax.test], [('/a/b/c', {'contents': 'blah'})])
    fake = tc.fakeFile('/a/b/c')
    self.assertTrue(isinstance(fake, fake_filesystem.FakeFile))
    self.assertEqual('blah', fake.contents)

  def test_fakeFileExists(self):
    """here"""
    pass

  def test_fakeContents(self):
    """here"""
    tc = self._tc

    # If we don't first call SetupSharedFilesystem, FakeContent() is an error.
    self.assertRaises(metax.self.Error, tc.fakeContents, '/any/path')

    fs = tc.setupSharedFilesystem(
        [metax.test], [('/a/b/c', {'contents': 'blah'})])
    self.assertEqual('blah', tc.fakeContents('/a/b/c'))

  def test__readFile(self):
    """here"""
    pass

  def test_revertFilesystem(self):
    """here"""
    tc = self._tc
    mname = metax.self.__name__
    self.assertFalse(mname in tc._fsinfo)
    unused_fs = tc.setupFilesystem(metax.test)
    self.assertTrue(mname in tc._fsinfo)
    tc.revertFilesystem(metax.test)
    self.assertFalse(mname in tc._fsinfo)

  def test_assertDictContains(self):
    """here"""
    print "metax.self.TestCase.assertDictContains does not yet have a unittest"

  def test_startswith(self):
    """here"""
    pass

  def test_endswith(self):
    """here"""
    print "metax.self.TestCase.endswith does not yet have a unittest"

  def test_contains(self):
    """here"""
    print "metax.self.TestCase.contains does not yet have a unittest"

  def test_matches(self):
    """here"""
    print "metax.self.TestCase.matches does not yet have a unittest"

  def test_iseq(self):
    """here"""
    print "metax.self.TestCase.iseq does not yet have a unittest"

  def test_noteq(self):
    """here"""
    print "metax.self.TestCase.noteq does not yet have a unittest"

  def test_iseqstr(self):
    """here"""
    print "metax.self.TestCase.iseqstr does not yet have a unittest"

  def test_noteqstr(self):
    """here"""
    print "metax.self.TestCase.noteqstr does not yet have a unittest"

  def test_iseqvec(self):
    """here"""
    print "metax.self.TestCase.iseqvec does not yet have a unittest"

  def test_iseqmap(self):
    """here"""
    print "metax.self.TestCase.iseqmap does not yet have a unittest"

  def test_iseqtext(self):
    """here"""
    print "metax.self.TestCase.iseqtext does not yet have a unittest"

  def test_iseqfile(self):
    """here"""
    print "metax.self.TestCase.iseqfile does not yet have a unittest"

  def test_iseqstrgold(self):
    """here"""
    print "metax.self.TestCase.iseqstrgold does not yet have a unittest"

  def test_iseqfilegold(self):
    """here"""
    print "metax.self.TestCase.iseqfilegold does not yet have a unittest"

  def test_isapprox(self):
    """here"""
    print "metax.self.TestCase.isapprox does not yet have a unittest"

  def test_islt(self):
    """here"""
    print "metax.self.TestCase.islt does not yet have a unittest"

  def test_isle(self):
    """here"""
    print "metax.self.TestCase.isle does not yet have a unittest"

  def test_isgt(self):
    """here"""
    print "metax.self.TestCase.isgt does not yet have a unittest"

  def test_isge(self):
    """here"""
    print "metax.self.TestCase.isge does not yet have a unittest"

  def test_raises(self):
    """here"""
    print "metax.self.TestCase.raises does not yet have a unittest"

  def test_issame(self):
    """here"""
    print "metax.self.TestCase.issame does not yet have a unittest"

  def test_notsame(self):
    """here"""
    print "metax.self.TestCase.notsame does not yet have a unittest"

  def test_istrue(self):
    """here"""
    print "metax.self.TestCase.istrue does not yet have a unittest"

  def test_isfalse(self):
    """here"""
    print "metax.self.TestCase.isfalse does not yet have a unittest"

  def test_isnull(self):
    """here"""
    print "metax.self.TestCase.isnull does not yet have a unittest"

  def test_notnull(self):
    """here"""
    print "metax.self.TestCase.notnull does not yet have a unittest"

  def test_isinst(self):
    """here"""
    print "metax.self.TestCase.isinst does not yet have a unittest"

  def test_fail(self):
    """here"""
    print "metax.self.TestCase.fail does not yet have a unittest"

  def test_meta(self):
    """here"""
    # noop
    pass


class TestCaseMetaTest(metax.test.TestCase):
  """Auto-generated test class for auto-generated meta class metax.test.TestCaseMeta."""

  def test___init__(self):
    """here"""
    pass


if __name__ == '__main__':  metax.test.main()
