# This file must be placed somewhere in one's PYTHONPATH. Bootstraps Meta.

# Provides following services:
#  - ensures that PYTHONPATH will resolve requests for metax.* properly
#    based on --meta_version
#  - ensures that PYTHONPATH will resolve requests for meta-generated
#    namespaces properly
#  - provides conditional support for auto-compilation of code.

# up python paths to find meta source code.
import os
import re
import sys

Verbose = False

# _Config: dict
#   A cache of key/value pairs parsed from ~/.config/metaxy/config.meta. Used
#   to optimize Config().
_Config = None

# Version: str
#   The version of Meta being used, as established by ConfigureVersion().
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
    # CODETANGLE(parse_config): Similar code exists in
    # <<src_root/src/kernel/parser.meta2.
    vre = re.compile(r'var\s+(?P<var>\S+)\s+=\s+(?P<val>\S+)')
    # TODO(wmh): Add a --config flag to metameta2.py!
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
    exists = os.path.exists(configpath)
    if verbose:
      print 'NOTE: Reading %s' % configpath
    result = {}
    _Config = result
    if exists:
      with open(configpath, 'r') as fp:
        for line in fp:
          m = vre.match(line)
          if m:
            result[m.group('var')] = os.path.expandvars(m.group('val'))
      result['config_path'] = configpath
    else:
      print 'WARNING: %s does not exist' % configpath
      print 'PWD: %s' % os.getcwd()
      print 'DIR: %s' % str(os.listdir(os.getcwd()))
      result['config_path'] = configpath
  return result


def ConfigureVersion(verbose=Verbose):
  return Setup(verbose=verbose)


def Setup(verbose=Verbose, auto=False):
  """Configure sys.path to support a meta version specified in sys.argv.

  Args:
    verbose: bool
     auto: bool
       If True, perform AutoCompile() functionality.

  SideEffect:
   - removes any element of sys.argv starting with '--meta_version='
   - removes any element of sys.argv matching '--meta_version' and also
     removes the next element.

  Returns: tuple<str,str>
   0. the version
   1. the path from which the metax.c module should be obtained.
  """
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
    print "NOTE: Using meta version '%s'" % version

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
        print 'NOTE: Added %s to front of sys.path' % newpath


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
    print 'ERROR in metameta.RegisterPath: Failed to find %s' % path
    # raise Exception('here')

  #print 'Adding %s to start of sys.path' % path
  sys.path.insert(0, path)
  NewPythonPaths.append(path)
  if verbose:
    print 'Adding %s to python path' % path

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
  if argv is None:
    argv = sys.argv
  # Issues this method addresses:
  #  - in order to create a metax.c.Compiler instance, we must first
  #    establish which version of the meta2 code is desired.
  #     - the beta version is available in <<repository_path>>/oopl/python/metax
  #     - named versions are available in <<src_root>>/lib/versions/v<version>
  #     - sys.path will always include <<repository_path>>/oopl/python
  #     - if a version other than beta is desired, we insert
  #       <<src_root>>/lib/versions/v<version>
  #    sys.path to use the user-specified version of the meta compiler

  # ConfigureVersion
  #   - modifies argv by removing --meta_version
  #   - modifies sys.path by adding <<repository_path>>/oopl/python and, if
  #     a version other than 'beta' was specified, another path BEFORE
  #     the above path, which provides access to metax.
  version, expected_metax_dir = ConfigureVersion()
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

  command, cli = ParseArgv(argv, metax.cli, root_module=metax.root)
  
  return metax.c.Compiler, command, cli


def ParseArgv(argv, cli_module, root_module=None):
  """Parse low-level command-line args into a metax.cli.Command instance.

  Args:
    argv: vec<str>
      The command-line args to parse. Index 0 is the executable.
    cli_module: module (required)
      The metax.cli module to use.
    root_module: module (optional)
      The metax.root module to use. If not null, root_module.Initialize(cli)
      is invoked to set the global CLI instance.

  Returns: tuple<metax.cli.Command,metax.cli.Values>
   1. The top-level Command instance. Never null.
   2. The Values wrapper around the instantiated Command instance. Null on error.
  """
  # Define the metax.cli.Command instance that describes top-level Meta compiler
  # flags. These are the only flags that general Metax compiler code will rely
  # on.
  command = cli_module.Command('meta2')
  command.newFlag(
    'baselang', 'str', default='python', aliases='b',
    summary='The baselang to compile into.',
    desc='If this is <special>, a metalang-specific default is used')
  command.newFlag(
    'debug', 'int', default=0, aliases='A',
    summary='Controls meta parsing debug level.')
  command.newFlag(
    'implicit_scopes', 'bool', default='false',
    summary='If true, methods without scopes are given a default body.',
    desc='By default, methods without scopes produce an error.')
  command.newFlag(
    'inmemory', 'bool', default='false',
    summary='If true, use memory filesystem instead of disk filesystem.')
  command.newFlag(
    'metadir', 'str', default='.meta2',
    summary='The subdir to write code to.',
    desc="A value of .meta2 is treaed specially, being symlinked to repo")
  command.newFlag(
    'metalang', 'str', default='oopl', aliases='L',
    summary='The metalang the code is defined in.')
  command.newFlag(
    'optimize_level', 'enum<off|low|avg|high|max>', default='high', aliases='O',
    summary='The amount of optimization to enable compiled files.',
    desc='')
  command.newFlag(
    'raw', 'bool', default='false',
    summary=(
      'If True, do not convert file references to meta '
      '(keep baselang paths).'))
  command.newFlag(
    'rawtests', 'bool', default='false', aliases='r',
    summary='If true, do not use bazel to run tests.',
    desc=(
      'Some baselangs can invoke the test harness without bazel, and for such\n'
      'baselangs this flag disables bazel. Can yield significantly faster\n'
      'test runtimes.'))
  command.newFlag(
    'showfs', 'bool', default='false',
    summary='If true, print out filesystem after compilation.')
  command.newFlag(
    'test', 'bool', default='false', aliases='t',
    summary='If true, invoke unit tests on all namespaces in all metafiles processed.')
  command.newFlag(
    'verbose', 'bool', default='false', aliases='v',
    summary='If true, print out additional diagnostics.')
  command.newFlag(
    'verbosity', 'int', default='0', aliases='V',
    summary='Levels of verbosity. Tied to --verbose.')
  command.newFlag(
    'write_goldens', 'bool', default='false', aliases='W',
    summary='If true, tests involving goldens write instead of compare.')
  command.newFlag(
    'disable_imports', 'bool', default='false', 
    summary='If true, do not invoke importMeta during compilation.')
  command.newFlag(
    'hack', 'bool', default='false', 
    summary='If true, enable some special code (used during prototyping)')
  command.newArg(
    'args', multi=True, summary='All other args')

  # Instantiate the command line args against the above Command, putting all
  # unknown args/flags into 'args'.
  instantiated = command.instantiate(argv, start=True)
  if instantiated:
    cli = instantiated.asValues()
    if cli.verbose and cli.verbosity == 0:
      cli.verbosity = 1
    elif cli.verbosity > 0 and not cli.verbose:
      cli.verbose = True
    # Initialize metax.root.MetaObject
    if root_module:
      #print root_module
      #root_module.Object.Initialize2(cli=cli)
      root_module.Object.Init(cli=cli)
  else:
    cli = None

  return command, cli


# http://dangerontheranger.blogspot.com/2012/07/how-to-use-sysmetapath-with-python.html
class MetaImporter(object):
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

    # We create an instance of the Meta compiler so that we can dynamically
    # compile meta code without having to invoke a subprocess (we want to be
    # as fast as possible here).
    Compiler, command, cli = ImportMeta(
      ['metac', '--metalang', 'oopl', '--baselang', 'python'])
    Compiler.Initialize()
    metac = Compiler(metal=cli.metalang, basel='python')
    # print 'NOTE: Created %s' % str(metac)

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
      subpath = fullname.replace('.', '/')
      repdir = os.path.join(MetaImporter.METAREP, 'oopl', 'python')
      pyfile = os.path.join(repdir, subpath, '__init__.py')
      if os.path.exists(pyfile):
        # fullname is a module generated by Meta. We determine whether its'
        # associated metafile needs recompiling.
        if not self._metac.maybeRecompileMeta(pyfile):
          # If errors were found, we exit.
          print 'Exiting due to errors'
          sys.exit(1)
        
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
  sys.meta_path.append(MetaImporter.Instance())
