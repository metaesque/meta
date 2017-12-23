import metax.root  # target=//metax/root:root
##########  End Imports  ##########


class TestCaseMeta(metax.root.ObjectMetaRoot):
  """Auto-generated meta class for metax.test.TestCase."""

  # field Debug : bool
  #   What to initialize TestCase.debug to.

  def Debug(cls):
    """here"""
    return cls._Debug

  def DebugIs(cls, value):
    """here

    Args:
      value: bool
    """
    cls._Debug = value

  def DebugRef(cls):
    """here"""
    return cls._Debug

  # field InstanceCount : int
  #   Counts the number of instances created so we can assign unique ids.
  #   Useful for debugging purposes.

  def InstanceCount(cls):
    """here"""
    return cls._InstanceCount

  def InstanceCountIs(cls, value):
    """here

    Args:
      value: int
    """
    cls._InstanceCount = value

  def InstanceCountRef(cls):
    """here"""
    return cls._InstanceCount

  # field WriteGoldens : bool
  #   If true, methods that invoke iseqstrgold() or iseqfilegold() will
  #   update goldens instead of compare goldens.

  def WriteGoldens(cls):
    """here"""
    return cls._WriteGoldens

  def WriteGoldensIs(cls, value):
    """here

    Args:
      value: bool
    """
    cls._WriteGoldens = value

  def WriteGoldensRef(cls):
    """here"""
    return cls._WriteGoldens

  # field CanonicalStdout : ostream
  #   The 'normal' stdout.

  def CanonicalStdout(cls):
    """here"""
    return cls._CanonicalStdout

  def CanonicalStdoutIs(cls, value):
    """here

    Args:
      value: ostream
    """
    cls._CanonicalStdout = value

  def CanonicalStdoutRef(cls):
    """here"""
    return cls._CanonicalStdout

  # field CanonicalStderr : ostream
  #   The 'normal' stderr.

  def CanonicalStderr(cls):
    """here"""
    return cls._CanonicalStderr

  def CanonicalStderrIs(cls, value):
    """here

    Args:
      value: ostream
    """
    cls._CanonicalStderr = value

  def CanonicalStderrRef(cls):
    """here"""
    return cls._CanonicalStderr

  # field Interactive : bool
  #   Set this to True to enable interactive unit tests.      

  def Interactive(cls):
    """here"""
    return cls._Interactive

  def InteractiveIs(cls, value):
    """here

    Args:
      value: bool
    """
    cls._Interactive = value

  def InteractiveRef(cls):
    """here"""
    return cls._Interactive

  def __init__(cls, name, bases, symbols):
    """here
    Initialize class-level variables.  This includes variables for
    controlling golden writing, interactivity, debugging, etc, based on
    the value of envars.

    TODO(wmh): This should be added to the 'meta lifecycle' above, when
    support has been provided by Meta.

    Args:
      name: &str
      bases: &vec<class>
      symbols: &map
    """
    super(TestCaseMeta, cls).__init__(name, bases, symbols)
    cls._Debug = False
    cls._InstanceCount = 0
    cls._Interactive = False
    # User-provided code follows.
    # TODO(wmh): How can we set environment variables when using bazel?
    # The --action_env flag from
    #    https://bazel.build/designs/2016/06/21/environment.html
    # does not appear to be working the way I understand it,
    # neither with entries in ~/.bazelrc or explicitly specified on
    # the command line:
    #   bazel test --action_env=BLAH=blork --test_output=all //wmh:regexp_test
    import os
    cls.WriteGoldensIs(os.getenv('WRITE_GOLDENS', '') == 'true')
    debug = os.getenv('META_DEBUG', '')
    if ' tests ' in debug:
      cls.DebugIs(True)
    cls.CanonicalStdoutIs(sys.stdout)
    cls.CanonicalStderrIs(sys.stderr)

    cls.cStringIOClass = cStringIO.StringIO().__class__
