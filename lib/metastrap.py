# This file must be placed somewhere in one's PYTHONPATH. Bootstraps Meta.

# Provides following services:
#  - ensures that PYTHONPATH will resolve requests for metax.* properly
#    based on --meta_version
#  - ensures that PYTHONPATH will resolve requests for meta-generated
#    namespaces properly
#  - provides conditional support for auto-compilation of code.

import logging
import os
import re
import sys
import time

if sys.version_info.major == 3:
  import importlib.abc

# When metastrap.Setup() was invoked (unix epoch float)
TimeStamp = None

Verbose = False

# _Config: dict
#   A cache of key/value pairs parsed from ~/.config/metaxy/config.meta. Used
#   to optimize Config().
_Config = None

# Version: str
#   The version of Meta being used, as established by Setup().
Version = None

def Config(verbose=Verbose):
  """Parse the meta config file.

  NOTE: This method is needed *any* time Meta is used (either within the
  compiler, or via stand-alone use of meta-generated classes). To this end,
  metax.root.ObjectMeta imports metastrap and uses it to initialize its
  Config() field.

  Returns: tuple<dict,str>
  """
  # TODO(wmh): The return value should be available everywhere from within
  # all baselangs. There is a plan afoot to introduce the symbol Meta into
  # every namespace (it may be metax.root.MetaObject aka the singleton
  # instance of metax.root.ObjectMeta, or some other entity), but that would
  # be the right place to store this information.  In which case we would
  # NOT provide metameta2.Config() ... or would otherwise ensure that
  # Meta.Config() returns the same thing as metameta2.Config().
  global _Config
  result = _Config
  if result is None:
    configpath = ConfigPath()
    exists = os.path.exists(configpath)
    if verbose:
      print('NOTE: Reading %s' % configpath)
    result = {}
    _Config = result
    if exists:
      vre = re.compile(r'var\s+(?P<var>\S+)\s+=\s+(?P<val>\S+)')
      with open(configpath, 'r') as fp:
        for line in fp:
          m = vre.match(line)
          if m:
            result[m.group('var')] = os.path.expandvars(m.group('val'))
      result['config_path'] = configpath
    else:
      print('WARNING: %s does not exist' % configpath)
      print('PWD: %s' % os.getcwd())
      print('DIR: %s' % str(os.listdir(os.getcwd())))
      result['config_path'] = configpath

  # TODO(wmh): Generalize the syntax of config.meta to support the
  # initialization of dicts (either via default with literal dict value, or via
  # a simple block that contains individual key/value pairs. Replace following
  # hardcoded code with that more general solution, where the person specifies
  # the mapping in their ~/.config/metaxy/config.meta file.
  src_root = result['src_root']
  metalangs = {
    'meta': os.path.join(src_root, 'src', 'schema', 'meta', 'schema.meta'),
    'oopl': os.path.join(src_root, 'src', 'schema', 'oopl', 'schema.meta'),
    'doc': os.path.join(src_root, 'src', 'schema', 'doc', 'schema.meta'),
  }
  home = os.getenv('HOME')
  if home:
    metalangs.update({
      'bio': os.path.join(
        home, 'src', 'wmh', 'lib', 'python', 'wmh', 'meta', 'bio', 'schema.meta'),
      'food': os.path.join(
        home, 'src', 'wmh', 'lib', 'python', 'wmh', 'meta', 'food', 'schema.meta'),
      'family': os.path.join(
        home, 'src', 'wmh', 'lib', 'python', 'wmh', 'meta', 'family', 'schema.meta'),
      'story': os.path.join(
        home, 'src', 'wmx', 'lib', 'python', 'metarotica', 'story', 'meta', 'schema.meta'),
    })
  for k, v in metalangs.items():
    if not os.path.exists(v):
      print('ERROR: %s has non-existent path %s' % (k, v))
      sys.exit(1)
  result['metalangs'] = metalangs
  #import pprint
  # pprint.pprint(result)

  # logging.info('metastrap.Config() returns %s' % result)
  return result


def ConfigPath():
  """Obtain the path to the meta config file."""
  configpath = os.getenv('META_CONFIG')
  if not configpath:
    home = os.getenv('HOME')
    if not home:
      # Special hack to handle GAE.
      configpath = './data/config.gae'
      if not os.path.exists(configpath):
        raise Exception('Failed to find env.var HOME')
    else:
      meta_config_dir = os.path.join(home, '.config', 'metaxy')
      configpath = os.path.join(meta_config_dir, 'config.meta')
  return configpath


def ConfigureVersion(verbose=Verbose):
  # TODO(wmh): Remove when all references are renamed to Setup()
  return Setup(verbose=verbose)


def Setup(verbose=Verbose, auto=False):
  """Configure sys.path to support a meta version specified in sys.argv.

  Args:
    verbose: bool
     auto: bool
       If True, perform AutoCompile() functionality.

  SideEffect:
   - removes any element of sys.argv starting with '--meta_version='
   - removes any element of sys.argv equal to '--meta_version' and also
     removes the next element.

  Returns: tuple<str,str>
   0. the version
   1. the path from which the metax.c module should be obtained.
  """
  global TimeStamp
  if TimeStamp is None:
    TimeStamp = time.time()

  # TODO(wmh): Pass in argv, setting to sys.argv by default.
  # TODO(wmh): Modify argv, not sys.argv (so that if a non sys.argv argv is
  # is passed in, it is modified instead of sys.argv).
  config = Config()

  # The list of paths to add, in reverse order, to the beginning of sys.path.
  updates = []

  # Ensure that the Meta repository_path is the first place we look for code.
  #  - TODO(wmh): This may be too heavy-handed ... people want to have some
  #    control over the order in which python libraries are being found, and
  #    by always putting this first, we are saying that any top-level
  #    namespace defined in Meta takes absolute precedence over any other
  #    implementation of that namespace, without any recourse.
  #
  # Note that we are specifying where to find the code implementing Meta, which
  # happens in Meta(Oopl), and this 'meta2' script by definition means we want
  # the python implementation ... hence the hard-coding of metalang and baselang.
  repopath = os.path.join(config['repository_path'], 'oopl', 'python')
  metaxpath = repopath
  updates.append(repopath)

  # Establish the version of Meta library code to use
  version = 'beta'
  argv = sys.argv
  vflag = '--meta_version'
  for i, arg in enumerate(argv):
    if arg.startswith(vflag):
      if arg.startswith(vflag + '='):
        version = arg[len(vflag)+1:]
        sys.argv.pop(i)
      else:
        version = argv[i+1]
        sys.argv.pop(i)
        sys.argv.pop(i)
  if verbose:
    print("NOTE: Using meta version '%s'" % version)

  global Version
  Version = version

  if version != 'beta':
    # CODETANGLE(version_path): in meta2
    path = VersionPath(version)
    if not os.path.exists(path):
      raise IOError('Failed to find a Meta version in ' + path)
    metaxpath = path
    updates.append(path)

  UpdatePythonPath(updates, verbose=verbose)

  if auto:
    AutoCompile()

  return version, metaxpath


def UpdatePythonPath(updates, verbose=False):
  if updates:
    # We want the last element of updates to be first in sys.path, which
    # happens when we insert each at position 0, start to last.
    #
    # TODO(wmh): If any of the newpaths already exist in sys.path, should we
    # keep their existing position, or always add at the beginning of sys.path?
    for newpath in updates:
      sys.path.insert(0, newpath)
      if verbose:
        print('NOTE: Added %s to front of sys.path' % newpath)


def VersionPath(version):
  """Obtain the path to add to sys.path to load a given version of Meta.

  Args:
    version: str
      A subdir of <<src_root>>/lib/versions.
  """
  config = Config()
  result = os.path.join(config['src_root'], 'lib', 'versions', version, 'lib')
  if not os.path.exists(result):
    raise Exception(
      '%s does not exist (%s is an invalid version)' % (result, version))
  return result


def RegisterPath(path, verbose=False):
  # Ensure that 'path' is in sys.path.
  if not os.path.exists(path):
    print('ERROR in metameta.RegisterPath: Failed to find %s' % path)
    # raise Exception('here')

  #print('Adding %s to start of sys.path' % path)
  sys.path.insert(0, path)
  NewPythonPaths.append(path)
  if verbose:
    print('Adding %s to python path' % path)

  # Ensure that 'path' is in PYTHONPATH
  env = os.environ
  pypath = env.get('PYTHONPATH', '')
  pylist = pypath.split(':')
  if path not in pylist:
    pypath = '%s:%s' % (path, pypath) if pypath else path
    env['PYTHONPATH'] = pypath


def ImportMeta(argv=None):
  """Configure sys.path to import the proper version of Meta, and import.

  Args:
    argv: vec<str>
      The command line args.  If null, sys.argv is used.
      Note that this vector is modified in place.

  Returns: tuple<class,metax.cli.Command,metax.cli.Values>
   1. The metax.c.Compiler class to use for interacting with Meta.
   2. The metax.cli.Command instance defining the top-level flags of Meta.
   3. The metax.cli.Values instance wrapping the instantiated metax.cli.Command
      (note that the wrapped command in (3) is usually NOT the same as (2) ...
      it will usually be a sub-command of (2)).
  """
  # Issues this method addresses:
  #  - in order to create a metax.c.Compiler instance, we must first
  #    establish which version of the Meta code is desired.
  #     - the beta version is available in <<repository_path>>/oopl/python/metax
  #     - named versions are available in <<src_root>>/lib/versions/v<version>
  #     - sys.path will always include <<repository_path>>/oopl/python
  #     - if a version other than beta is desired, we insert
  #         <<src_root>>/lib/versions/v<version>
  #       into sys.path to use the user-specified version of the meta compiler.
  if argv is None:
    argv = sys.argv

  # Setup
  #  - modifies argv by removing --meta_version
  #  - modifies sys.path by adding <<repository_path>>/oopl/python and, if
  #    a version other than 'beta' was specified, another path BEFORE
  #    the above path, which provides access to metax.
  version, expected_metax_dir = Setup()
  expected_metax_path = os.path.join(expected_metax_dir, 'metax', 'c')

  # Import some core metax modules and verify they have the desired version.
  import metax.c
  metax_path = os.path.dirname(metax.c.__file__)
  if metax_path != expected_metax_path:
    raise IOError(
      'Expecting metax.c to resolve to\n  %s\nnot\n  %s' %
      (expected_metax_path, metax.c.__path__[0]))
  import metax.root
  import metax.cli
  compiler_class = metax.c.Compiler

  # As of 2018-11-03, the ParseArgv code is deprated in favor of Compiler.MetaxCLI.
  # command, cli = ParseArgv(argv, metax.cli, root_module=metax.root)
  command, instcmd, cli = compiler_class.MetaxCLI(argv=argv)
  return compiler_class, command, cli

def RecoverMeta(e):
  # Invoked if invocation of a meta-generated entry point (MetaxEntry) raises
  # an exception.
  import io
  import traceback
  import metax.c
  import metax.root
  # assert metax.c.Compiler.CONFIG
  assert metax.root.MetaObject.Config()

  # Note that the current metax.root.Object.CLI() is for the command that
  # was invoked that is producing an exception. For the purposes of filtering
  # output, we need to update the CLI to be one containing all the metac
  # flags instead.
  compiler_class, command, cli = ImportMeta()
  metax.c.Compiler.Initialize()
  metax.root.Object.Init(cli=cli)
  metac = metax.c.Compiler(metal='oopl', basel='python')
  metax.c.Compiler.CurrentIs(metac)
  text = traceback.format_exc()
  if sys.version_info[0] == 2 and isinstance(text, str):
    text = u'' + text
  ifp = io.StringIO(text)
  baselang = metac.metalang().baselangNamed('python')
  metac.filterMetaOutput(baselang=baselang, ifp=ifp, debug=False)


def DynamicCompiler(metal, basel):
  orig_argv = sys.argv
  sys.argv = [metal, '-L', metal]
  Compiler, command, metacli = ImportMeta()
  Compiler.Initialize()
  # TODO(wmh): Should we only be initializing object cli to metacli if
  # metal is oopl?
  import metax.root
  metax.root.Object.Init(cli=metacli)
  result = Compiler(metal=metacli.metalang, basel=basel)
  sys.argv = orig_argv
  return result


# http://dangerontheranger.blogspot.com/2012/07/how-to-use-sysmetapath-with-python.html
class MetaImporter(object if sys.version_info.major < 3 else importlib.abc.MetaPathFinder):
  """Auto-compile meta files newer than imported python files.

  Since Meta generates python files, we want to ensure that anytime a python
  module is imported and that module comes from Meta, if the meta source file
  is newer than the python .py file, we recompile the .meta file to regenerate
  the .py file before importation occurs.
  """

  METAREP = None
  PATH_RE = None
  _Instance = None

  @classmethod
  def Initialize(cls):
    config = Config()
    path = config['repository_path']
    cls.METAREP = path
    cls.PATH_RE = re.compile('^%s/' % re.escape(path))

  @classmethod
  def Instance(cls):
    result = cls._Instance
    if result is None:
      cls.Initialize()
      result = cls()
      cls._Instance = result
    return result

  def __init__(self):
    if self.__class__._Instance:
      raise Error(
        'Use MetaImporter.Instance() to obtain the singleton instance')
    # print('HERE creating MetaImporter')

    # We create an instance of the Meta compiler so that we can dynamically
    # compile meta code without having to invoke a subprocess (we want to be
    # as fast as possible here).
    Compiler, command, cli = ImportMeta(
      ['metac', '--metalang', 'oopl', '--baselang', 'python'])
    Compiler.Initialize()
    # print('**** HERE with cli=%s' % cli)
    # command.show()
    import metax.root
    metax.root.Object.Init(cli=cli)
    metac = Compiler(metal=cli.metalang, basel='python')
    # print('NOTE: Created %s' % str(metac))

    # field metac: parser.Compiler
    #   The Meta compiler.
    self._metac = metac
    self._cli = cli

    # field cache: dict
    #   Maintains information on process paths so that we do not need to
    #   continually recheck the same paths.  Keys are fullnames and values
    #   are bool (True if the fullname is meta-based, False if not). Whether
    #   true or false, the existence of a fullname in the cache is sufficient
    #   to avoid having to process it again.
    self._cache = {}

    # field baselang: OoplPython
    #   The OoplPython singleton instance
    self._baselang = metac.metalang().baselangNamed('python')

  def cache(self):
    return self._cache

  def dump(self, fp=sys.stdout):
    cache = self._cache
    for key in sorted(cache):
      if cache[key]:
        fp.write('%s\n' % key)
      #fp.write('%s: %s\n' % (key, cache[key]))

  def find_spec(self, fullname, path, target=None):
    """This method is supposedly called by Python3 if this class is on
    sys.meta_path, but it is not currently work.

    https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder.find_spec

    I've experimented with making this class a subclass of
    importlib.abc.MetaPathFinder in python3, but that doesn't fix the issue.
    """
    return self.maybeRecompileMeta(fullname, path, target=target)

  def find_module(self, fullname, path=None):
    """This method is called by Python if this class is on sys.path.

    This method will be called every time an import statement is detected (or
    __import__ is called), before Python's built-in package/module-finding code
    kicks in.

    Args:
      fullname: str
        The fully-qualified name of the module to look for.
      path: list of str or None
        Either __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

    Returns: loader or None
      If fullname is the name of a module/package that we want to report as
      found, then we need to return a loader object.
    """
    return self.maybeRecompileMeta(fullname, path)

  def maybeRecompileMeta(self, fullname, path, target=None):
    """A method shared by find_module() and find_spec().

    This method never actually finds a module (it always returns None), but
    may dynamically recompile a .meta file if the .meta file associated with
    a python module is newer than the python .py/.pyc files.

    Args:
      fullname: str
        The fully-qualified name of the module to look for.
      path: list of str or None
        Either __path__ (for submodules and subpackages) or None (for
        a top-level module/package).
      target: str or None
        Used as a hint. Only in python3, not python2.
    """
    # print('Checking if %s involves a Meta recompile' % fullname)
    cache = self._cache

    # TODO(wmh): Determine if we can rely on path (which is usually a list of
    # one path, or None).  I initially assumed it was the first directory in
    # sys.path matching fullname, but that doesn't explain:
    #   1) why it is a list instead of a single string value
    #   2) why top-level module/packages pass in None
    # so I must be interpreting this incorrectly.  For now, we don't rely on
    # path at all.

    # We determine if this is a meta file. For now, we assume that all
    # meta-generated files reside in cls.METAREP/oopl/python. If we end up
    # supporting multiple such dirs we'll need to generalize this code.
    if fullname in cache:
      pass
    else:
      cli = self._metac.cli()
      # print('cli=%s' % id(cli))
      # assert cli
      subpath = fullname.replace('.', '/')
      repdir = os.path.join(MetaImporter.METAREP, 'oopl', 'python')
      pyfile = os.path.join(repdir, subpath, '__init__.py')
      if os.path.exists(pyfile):
        # fullname is a module generated by Meta. We determine whether its'
        # associated metafile needs recompiling.
        res = self._metac.maybeRecompileMeta(pyfile)
        # res is None if no recompilation occurred, True if compilation
        # occurred successfully, and False if it ocurred unsuccessfully.
        if res is False:
          # If errors were found, we exit.
          raise Exception('Exiting due to errors')

        ismeta = True
      else:
        ismeta = False
      cache[fullname] = ismeta

    # If fullname is the name of a module/package that we want to report as
    # found, then we need to return a loader object. If we don't provide the
    # requested module, return None, as per PEP #302. In meta, we do not
    # currently need to ever return a loader object, we simply want to
    # recompile the python code if the associated meta file is newer. So we
    # always return None
    return None

  def load_module(self, fullname):
    """Called if CustomImporter.find_module does not return None.

    Args:
      fullname: str
        The fully-qualified name of the module/package that was requested.

    Raises: ImportError
      If the requested module/package couldn't be loaded.

    Returns: module
    """
    if True:
      # Raise ImportError as per PEP #302 if the requested module/package
      # couldn't be loaded. This should never be reached in this code,
      # because find_module() always returns None
      raise ImportError(fullname)

    # PEP#302 says to return the module if the loader object (i.e, this
    # class) successfully loaded the module. Note that a regular class works
    # just fine as a module.
    class VirtualModule(object):
      def hello(self):
        return 'Hello World!'
    return VirtualModule()


def AutoCompile():
  """Ensure that meta files are compiled for python imports.

  This should be invoked before main(), or at least before any 'import'
  statements are found that could refer to meta-generated code.
  """
  # Note that sys.meta_path has nothing to do with Meta ... it is a generic
  # python concept: https://docs.python.org/2/library/sys.html#sys.meta_path
  sys.meta_path.insert(0, MetaImporter.Instance())
