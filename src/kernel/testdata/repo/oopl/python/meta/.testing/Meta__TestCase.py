# Imports for class Meta__TestCase
import sys                                # core 

import meta.root                          # target 
# End imports for class Meta__TestCase


class Meta__TestCase(meta.root.Object):
  """Meta class of TestCase."""
  
  # instance field STDOUT : meta!ostream

  # instance field STDERR : meta!ostream

  # instance field Interactive : bool
  #   Set this to True to enable interactive unit tests.

  # instance field WriteGoldens : bool
  #   Set this to True to write golden files instead of comparing them.

  # instance field Debug : bool
  #   What to initialize TestCase.debug to.

  # instance field InstanceCount : int
  #   Counts the number of instances created so we can assign unique ids.
  #   Useful for debugging purposes.

  def __init__(self):
    """This is for the class-level initialization."""
    super(Meta__TestCase, self).__init__()
    self.STDOUT = sys.stdout
    self.STDERR = sys.stderr
    self.Interactive = False
    self.WriteGoldens = False
    self.Debug = False
    self.InstanceCount = 0
    # User-provided code follows.

  def __init__(self):
    """This is for the class-level initialization."""
    super(Meta__TestCase, self).__init__()
    self.STDOUT = sys.stdout
    self.STDERR = sys.stderr
    self.Interactive = False
    self.WriteGoldens = False
    self.Debug = False
    self.InstanceCount = 0
    # User-provided code follows.

  def setUpClass(self):
    """no docstr"""
    super(Meta__TestCase, self).setUpClass()
    # User-provided code follows.
    if cls.Debug:
      print 'Invoking %s SetUp' % cls.__name__

  def tearDownClass(self):
    """no docstr"""
    if cls.Debug:
      print 'Invoking %s TearDown' % cls.__name__
    super(Meta__TestCase, self).tearDownClass()

  def Initialize(self):
    """Initialize class-level variables.  This includes variables for
    controlling golden writing, interactivity, debugging, etc, based on
    the value of envars.

    TODO(wmh): This should be added to the 'meta lifecycle' above, when
    support has been provided by Meta.
    """
    # TODO(wmh): How can we set environment variables when using bazel?
    # The --action_env flag from
    #    https://bazel.build/designs/2016/06/21/environment.html
    # does not appear to be working the way I understand it,
    # neither with entries in ~/.bazelrc or explicitly specified on
    # the command line:
    #   bazel test --action_env=BLAH=blork --test_output=all //wmh:regexp_test
    cls.WriteGoldens = os.getenv('WRITE_GOLDENS', '') == 'true'
    debug = os.getenv('META_DEBUG', '')
    if ' tests ' in debug:
      cls.Debug = True

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
      fqn: str
        The fully qualified name of the class for which resources are
        desired.  If null, uses the receiver cls to determine fqn.

    Returns: str
    """
    return meta.root.Object.Resource(resource_id, fqn=fqn, test=True)

# The singleton instance of the metaclass.
MetaTestCase = Meta__TestCase()
