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
#   A cache of key/value pairs parsed from ~/.config/metameta. Used
#   to optimize Config().
_Config = None

def Config(verbose=Verbose):
  """Parse the meta config file.

  NOTE: This method is needed *any* time Meta is used (either within the
  compiler, or via stand-alone use of meta-generated classes). To this end,
  metax.root.ObjectMeta imports metastrap and uses it to initialize its
  Config() field.

  Returns: dict
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
    configpath = os.path.join(os.getenv('HOME'), '.config', 'metameta')
    if verbose:
      print 'NOTE: Reading %s' % configpath
    result = {}
    _Config = result
    if os.path.exists(configpath):
      with open(configpath, 'r') as fp:
        for line in fp:
          m = vre.match(line)
          if m:
            result[m.group('var')] = os.path.expandvars(m.group('val'))
  return result


def ConfigureVersion(verbose=Verbose):
  """Configure sys.path to support a meta version specified in sys.argv.

  SideEffect:
   - removes any element of sys.argv starting with '--meta_version='
   - removes any element of sys.argv matching '--meta_version' and also
     removes the next element.

  Returns: tuple<str,str>
   0. the version
   1. the path from which the metax.c module should be obtained.
  """
  config = Config()

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
  sys.path.insert(0, repopath)
  metaxpath = repopath
  if verbose:
    print 'NOTE: Added %s to front of sys.path' % repopath

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
        
  if version != 'beta':
    # CODETANGLE(version_path): in meta2
    path = os.path.join(config['src_root'], 'lib', 'versions', version, 'lib')
    if not os.path.exists(path):
      raise IOError('Failed to find a Meta version in ' + path)
    sys.path.insert(0, path)
    metaxpath = path
    if verbose:
      print 'NOTE: Added %s to front of sys.path' % path
        
  return version, metaxpath


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
    path = Config()['repository_path']
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
    # meta-generated files reside in cls.METAREP/oopl/python. If we end up
    # supporting multiple such dirs we'll need to generalize this code.
    if fullname in cache:
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
  # Note that sys.meta_path has nothing to do with Meta ... it is a generic
  # python concept: https://docs.python.org/2/library/sys.html#sys.meta_path
  sys.meta_path.append(MetaImporter.Instance())
