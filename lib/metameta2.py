# This file must be placed somewhere in one's PYTHONPATH. It is used to set
# up python paths to find meta source code. It relies on METAROOT being
# properly set.
import os
import re
import sys
import optparse   # TODO(wmh): Update to argparse or a meta-implemented version.

class Error(Exception):
  pass

Version = None
NewPythonPaths = []
NEWSUFFIX = '2'

_MetaFlagParser = None

def CheckEnv():
  """Ensure that various META-specific environment variables are defined."""
  # print 'Checking Meta environment...'

  # IMPORTANT: Code in various places assumes these checks have been made.
  # If you remove a variable from this list, audit the code to see if
  # a check needs to be added elsewhere.
  for envvar in (
    'METAREP',        # where baselang source code is written
    'META_VERSION',   # which version of the meta compiler to use
    'METAROOT',       # where the Meta source code resides
    # 'METAPATH',     # the colon-separate list of directories containing Meta source
    'META_METALANG',  # the default metalang
    'META_BASELANG'   # the default baselang
  ):
    if os.getenv(envvar, None) is None:
      raise Error('Failed to find required environment variable %s' % envvar)

  # We replace $METAREP/oopl/python in PYTHONPATH with $METAREP$NEWSUFFIX/oopl/python
  # TODO(wmh): Remove this when we are fully migrated to meta2.
  metarep_path = os.path.join(os.getenv('METAREP'), 'oopl', 'python')
  newrep_path = os.path.join(os.getenv('METAREP') + NEWSUFFIX, 'oopl', 'python')
  index = None
  for i, path in enumerate(sys.path):
    if path == metarep_path:
      index = i
      break
  if index is not None:
    sys.stderr.write(
      'WARNING: Replaced %s with %s in sys.path\n' %
      (metarep_path, newrep_path))
    sys.path[index] = newrep_path

# TODO(wmh): Determine if we ALWAYS want to invoke CheckEnv() whenever
# metameta is imported, or only selectively. If it is not always invoked,
# the code for modify sys.path needs to be pulled out and put someplace that
# *is* always executed.
# TODO(wmh): Remove the reliance on envars in favor of a single config file.
CheckEnv()


def ParseFlags(args=None):
  if args is None:
    args = sys.argv[1:]
  flags, args = FlagParser().parse_args(args)
  if flags.metalang == os.getenv('META_METALANG', 'oopl'):
    if flags.baselang == '':
      flags.baselang = os.getenv('META_BASELANG', '')
  return flags, args  


def FlagParser():
  global _MetaFlagParser
  result = _MetaFlagParser
  if not result:
    options = optparse.OptionParser()

    options.add_option(
      '-A', '--debug', dest='debug', default=0, type='int',
      help='Control debugging level')

    options.add_option(
      '-b', '--baselang', dest='baselang', default='',
      help='The base language to compile into.')

    options.add_option(
      '--basic', action='store_true', dest='basic', default=False,
      help=(
        'Execute metapy without filtering (if not present, invokes a subshell that '
        'executes this same command with --basic, and processes stderr with '
        'metafilt'))

    options.add_option(
      '--batch', action='store_true', dest='batch', default=False,
      help='Whenever interactive prompts would occur, assume answer is yes.')

    options.add_option(
      '-c', '--compile', action='store_true', dest='compile', default=False,
      help='If True, compile meta source code into a base language.')

    options.add_option(
      '-C', '--confirm', action='store_true', dest='verify', default=False,
      help='Confirm/verify whatever action is being performed.')

    options.add_option(
      '--class_re', dest='class_re', default=None,
      help=(
        'Only consider classes that contain this regexp '
        '(when printing repository status, etc)'))

    options.add_option(
      '--clean', dest='clean', default=None,
      help=(
        'comma-separated list of classes to clean from repository'))

    options.add_option(
      '--cwd', dest='cwd', default=None,
      help='The directory to use to resolve relative paths.')

    options.add_option(
      '--debug_level', dest='debug_level', default='max', type='choice',
      choices=['off', 'low', 'avg', 'high', 'max'],
      help='The amount of debugging to enable compiled files.')

    options.add_option(
      '--display', action='store_true', dest='display', default=False,
      help='Used anywhere one can display or not display something.')

    options.add_option(
      '--dryrun', action='store_true', dest='dryrun', default=False,
      help='If True, print out actions but do not execute them.')
    
    # TODO(wmh): When we move to meta2, --emacs can be removed in favor of
    # command 'emacs'
    options.add_option(
      '--emacs', action='store_true', dest='emacs', default=False,
      help='If True, generate an emacs major mode for specified metalang')

    # TODO(wmh): The --expand flag stays in meta2, but is something that
    # augments certain commands rather than being its own command. In
    # particular, if the command is 'canonical', --expand means show the
    # canonical version AFTER expandMeta() has been invoked (by default,
    # canonical shows the version with expanding).
    options.add_option(
      '-E', '--expand', action='store_true', dest='expand', default=False,
      help='Show expanded meta file.')

    options.add_option(
      '--experiment1', action='store_true', dest='experiment1', default=False,
      help='Used to enable experiments.')

    options.add_option(
      '--experiment2', action='store_true', dest='experiment2', default=False,
      help='Used to enable experiments.')

    options.add_option(
      '--find', dest='find', default='',
      help=(
        'Parse but do not compiler, instead reporting all locations matching '
        'specified regexp'))

    options.add_option(
      '--xfind', dest='xfind', default='',
      help=(
        'Only applies if --find also included. Specifies a regexp to ignore, '
        'among those matched by --find.'))

    options.add_option(
      '--findcons', dest='findcons', default='',
      help=(
        'A comma-or-space-separated list of construct kinds to search '
        '(or, if preceeded by a hyphen (-), to exclude.'))

    options.add_option(
      '--findattr', dest='findattr', default='',
      help=(
        'A comma-or-space-separated list of attribute keys to search '
        '(or, if preceeded by a hyphen (-), to exclude.'))

    options.add_option(
      '--lintfull', action='store_true', dest='lintfull', default=False,
      help='If true, turn on various reminder warnings that should be rare.')

    options.add_option(
      '--generate_bootstraps', action='store_true', dest='generate_bootstraps', default=False,
      help='If True, generate the auto/bootstrap.py file and exit.')

    # TODO(wmh): When we move to meta2, --html can be removed in favor of
    # command 'html'
    options.add_option(
      '-H', '--html', action='store_true', dest='html', default=False,
      help='If True, generate html showing Meta implementation progress.')

    options.add_option(
      '--hack1', dest='hack1', default=None,
      # TODO(wmh): Figure out how to get --test_arg available in test code!
      help='Javascript test method regexp str.')

    options.add_option(
      '--info', action='store_true', dest='info', default=False,
      help='If True, print out some general info about the meta env.')

    options.add_option(
      '--inline_level', dest='inline_level', default='off', type='choice',
      choices=['off', 'low', 'avg', 'high', 'max'],
      help='The amount of inlining to enable compiled files.')

    # TODO(wmh): When we move to meta2, --log can be removed in favor of
    # command 'log'
    options.add_option(
      '-l', '--log', action='store_true', dest='log', default=False,
      help='If True, log actions to stdout (by default, they are logged elsewhere).')

    options.add_option(
      '-L', '--metalang', dest='metalang', default=os.getenv('META_METALANG', 'oopl'),
      help='The meta language we are compiling')

    options.add_option(
      '-M', '--inmemory', action='store_true', dest='inmemory', default=False,
      help='If True, use memory filesystem instead of disk filesystem.')

    options.add_option(
      '--metadir', dest='metadir', default='.meta',
      help='The subdir to write code to')

    options.add_option(
      '--namespace_re', dest='namespace_re', default=None,
      help=(
        'Only consider namespaces that contain this regexp '
        '(when printing repository status, etc)'))

    options.add_option(
      '-O', '--optimize_level', dest='optimize_level', default='high', type='choice',
      choices=['off', 'low', 'avg', 'high', 'max'],
      help='The amount of optimization to enable compiled files.')

    options.add_option(
      '--oldcode', action='store_true', dest='oldcode', default=False,
      help='Used when migrating to new code and wanting ability to back off.')

    options.add_option(
      '--profile_level', dest='profile_level', default='off', type='choice',
      choices=['off', 'low', 'avg', 'high', 'max'],
      help='The amount of profiling to enable compiled files.')

    options.add_option(
      '--quiet', action='store_true', dest='quiet', default=False,
      help='For situations where verbosity is the default.')

    options.add_option(
      '--raw', action='store_true', dest='raw', default=False,
      help='If True, do not convert file references to meta (keep baselang paths).')

    options.add_option(
      '--unfilt', action='store_true', dest='unfilt', default=False,
      help='If True, do not filter test output via Compiler.parseBazelOutput')

    options.add_option(
      '-r', '--rawtests', action='store_true', dest='rawtests', default=False,
      help=(
        'If True, do not use bazel to run tests. Instead, invoke underlying '
        'test harness directly. May not be available in all baselangs.'))

    # TODO(wmh): When we move to meta2, --reverse can be removed in favor of
    # command 'reverse'
    options.add_option(
      '-R', '--reverse', action='store_true', dest='reverse', default=False,
      help='Reverse compile a baselang file into a .meta file')

    options.add_option(
      '--show_expanded', action='store_true', dest='show_expanded', default=False,
      help='Print out the expanded version of every metafile.')

    options.add_option(
      '-t', '--test', action='store_true', dest='test', default=False,
      help='Run unittests on compiled code.')

    options.add_option(
      '--test_output', dest='test_output', default='all',
      help=(
        'How much output to produce in tests. Values include '
        'all, streamed, errors, summary'))

    options.add_option(
      '--umlvars', dest='umlvars', default='',
      help='Comma-separated list of key=value pairs defining a uml config dict.')

    options.add_option(
      '-v', '--verbose', action='store_true', dest='verbose', default=False,
      help='If True, print out extra diagnostics.')

    options.add_option(
      '-V', '--version', action='store', dest='version', default='',
      help='Which version of the meta library to use (beta, current, previous).')

    options.add_option(
      '--warn_level', dest='warn_level', default='max', type='choice',
      choices=['off', 'low', 'avg', 'high', 'max'],
      help='The amount of warning to enable compiled files.')

    # TODO(wmh): When we move to meta2, --canonicalize can be removed in favor
    # of command 'canonical'
    options.add_option(
      '-z', '--canonicalize', action='store_true', dest='canonical', default=False,
      help='If True, print out a canonical version of source files.')

    result = options
    _MetaFlagParser = result
  return result


def Metastrap(version=None, verbose=False):
  """Ensure that sys.path includes paths for the specified version of Meta.

  Args:
    version: str or None
      The version to establish.  If None, use the value of META_VERSION envvar.
    verbose: bool
      If True, print what actions are being performed.
  """
  global Version
  if Version is None:
    if verbose:
      print 'Invoked metameta.Metastrap(version=\'%s\', verbose=%s)' % (
        version, verbose)
    metaroot = os.getenv('METAROOT')
    if metaroot is None:
      raise Error('METAROOT must be set to the root of the Meta directory.')
    if not version:
      version = os.getenv('META_VERSION', 'current')

    if verbose:
      print 'Loading %s version of metac' % version
    path1 = os.path.join(metaroot, 'lib', version, 'meta')
    path2 = os.path.join(metaroot, 'lib', version, 'python')
    for path in (path2, path1):
      RegisterPath(path, verbose=verbose)
    Version = version
  else:
    # We've already bootstrapped, and don't need to do so again.
    if version and version != Version:
      raise Error(
        'Metastrap called with version %s when env already strapped with %s' %
        (version, Version))
    pass


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
  

def SwapStreams():
  """Swap stdout and stderr.

  Useful when wanting to filter python errors to remap to meta files ...
  errors are usually written to stderr, and unix pipes only operate on
  stdout, not stderr.
  """
  tmp = sys.stdout
  sys.stdout = sys.stderr
  sys.stderr = tmp


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
    path = os.getenv('METAREP', None)
    if not path:
      raise Error('Failed to find METAREP')
    path += NEWSUFFIX  # TODO(wmh): Remove the suffix when we are fully migrated.
    # TODO(wmh): What was the purpose of METAREPATH and is it used anymore?
    # Should it be a colon-separated list of directories containing
    # meta-generated code?
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
    # TODO(wmh): Decide how to control the version used here.  Should we always
    # use beta, or usually use current, or base it on some envvar?
    Metastrap(version='beta', verbose=False)
    import metaboot.parser
    flags, args = ParseFlags(sys.argv)
    compiler_class = metaboot.parser.Compiler
    metac = compiler_class(metal='oopl', basel='python', flags=flags)
    # print 'NOTE: Created %s' % str(metac)

    # field cache: dict
    #   Maintains information on process paths so that we do not need to
    #   continually recheck the same paths.  Keys are fullnames and values
    #   are bool (True if the fullname is meta-based, False if not). Whether
    #   true or false, the existence of a fullname in the cache is sufficient
    #   to avoid having to process it again.
    self._cache = {}

    # field metac: parser.Compiler
    #   The Meta compiler.
    self._metac = metac

    # field baselang: OoplPython
    #   The OoplPython singleton instance
    self._baselang = self._metac.metalang().baselangNamed('python')
    
  def cache(self):
    return self._cache

  def dump(self, fp=sys.stdout):
    cache = self._cache
    for key in sorted(cache):
      if cache[key]:
        fp.write('%s\n' % key)
      #fp.write('%s: %s\n' % (key, cache[key]))

  def find_module(self, fullname, path):
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
    # meta-generated files reside in ${METAREP}2.  If we end up supporting
    # multiple such dirs (is that what METAREPATH was for?), we'll need to
    # generalize this code.
    if fullname in cache:
      #print 'REPEAT: ' + fullname
      pass
    else:
      subpath = fullname.replace('.', '/')
      repdir = os.path.join(MetaImporter.METAREP, 'oopl', 'python')
      pyfile = os.path.join(repdir, subpath + '.py')
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
  sys.meta_path.append(MetaImporter.Instance())


def MonitorImports():
  print '#' * 70
  print 'WARNING: Please use metameta.AutoCompile() instead of metameta.MonitorImports()'
  print '#' * 70
  AutoCompile()
