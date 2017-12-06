# Imports for class Object
import inspect                            # core meta: 20
import os                                 # core meta: 21
import sys                                # core meta: 22
import sys                                # core 
import threading                          # core meta: 23

import meta.errors                        # target meta: 24
# End imports for class Object


class Object(object):
  """Except in special circumstances, every class defined within Meta
  inherits from this class. Every base language provides a specialized
  implementation that provides functionality useful in implementing
  Meta-level semantics within that base language.  Some of the methods
  defined here are present in all languages, some are only present in
  a subset of languages or in just one language.
  """
  __metaclass__ = ObjectMetaClass
  
  # field StrNull : *str
  #   The representation of 'null' for use with '&str' and '*str' types.
  StrNull = None

  @classmethod
  def Resource(cls, resource_id, fqn=None, test=False):
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
      test: bool
        If true, the resource is for a test class.

    Returns: str
    """
    # TODO(wmh): Each metaclass should maintain the list of legal
    # resources associated with class instances, so that this method
    # is just a lookup in a map.  There are, however, some complexities
    # involved in auto-generating this map that need to be worked out
    # (code for auto-generation of field constructs needs to be written,
    # similar to the code for auto-generating methods).  We also need
    # to decide whether resources get inherited from parent classes, etc.

    if fqn is None:
      cname = cls.__name__
      nmsp = cls.__module__
      fqn = nmsp + '.' + cname

    # Convert the fqn to a relative path.
    metarep = os.getenv('METAREP')
    if metarep is None:
      # TODO(wmh): Handle non-test bazel invocation (e.g. bazel run vs bazel test)
      if os.getenv('TEST_SRCDIR', None) or os.getenv('IN_UNITTEST'):
        # We are in bazel running a test.  All such tests are invoked from
        # the directory containing WORKSPACE.
        parts = [os.getcwd()] + fqn.split('.')
      else:
        raise meta.errors.Error('Missing environment variable METAREP')
    else:
      # We are
      parts = [metarep, 'oopl', 'python']
      parts.extend(fqn.split('.'))
    if test:
      parts[-1] += 'Test'
      parts[-2] += '_test'
    parts[-1] += '_' + resource_id
    parts[-2] = '.' + parts[-2]
    # print parts
    path = '/'.join(parts)
    # TODO(wmh): Verify that the path exists? Or do we avoid using the
    # filesystem here and let callers deal with it themselves?
    return path

  @classmethod
  def ShowHierarchy(cls, fp=sys.stdout):
    """Print out the inheritance hierarchy of this class.

    Args:
      fp: file
        Where to write the hierarchy.
    """
    classes = [self.__class__]
    i = 0
    while i < len(classes):
      cls = classes[i]
      classes.extend(cls.__bases__)
      fp.write(str(cls) + '\n')
      i += 1

  def __init__(self):
    """The default initializer for the top of the hierarchy."""
    super(Object, self).__init__()
    # User-provided code follows.

  @staticmethod
  def _meta__protected(method):
    """A runtime decorator for ensuring that a method marked as protected
    abides by that privacy constraint.

    Raises:
      ProtectedMethod: if invoked from a method not within the inheritance
      hierarchy of the class in which the method was defined.

    Args:
      method: any
        An instance or class method (but not a static method).
    """
    def wrapper(self, *args, **kwds):
      frame = inspect.currentframe()
      calling_frame = frame.f_back
      calling_class = calling_frame.f_locals['self'].__class__
      if not issubclass(calling_class, self.__class__):
        receiver_class = frame.f_locals['self'].__class__
        filename, lineno, function, code_context, index = inspect.getframeinfo(
          calling_frame)
        raise meta.errors.ProtectedMethod(
          '%s.%s is a protected method (invoked in %s.%s but %s !< %s)' %
          (receiver_class.__name__, method.__name__,
           calling_class.__name__, function,
           calling_class.__name__, receiver_class.__name__))
      method(self, *args, **kwds)
    return wrapper

  @staticmethod
  def _meta__private(method):
    """A runtime decorator for ensuring that a method marked as private
    abides by that privacy constraint.

    Raises:
      PrivateMethod: if invoked from a method not within the class defining
      the method.

    Args:
      method: any
        An instance or class method (but not a static method).
    """
    def wrapper(self, *args, **kwds):
      frame = inspect.currentframe()
      calling_frame = frame.f_back
      calling_class = calling_frame.f_locals['self'].__class__
      if not calling_class is self.__class__:
        receiver_class = frame.f_locals['self'].__class__
        filename, lineno, function, code_context, index = inspect.getframeinfo(
          calling_frame)
        raise meta.errors.PrivateMethod(
          '%s.%s is a protected method (invoked in %s.%s but %s !< %s)' %
          (receiver_class.__name__, method.__name__,
           calling_class.__name__, function,
           calling_class.__name__, receiver_class.__name__))
      method(self, *args, **kwds)
    return wrapper

  # field _IdCounter : int
  #   Used by the 'id' method to assign unique integer to object in javascript.
  _IdCounter = 0

  def metaSummary(self):
    """Return a one-line summary of this object.

    Meta auto-generates metaSummary methods for any class that does not
    explicitly provide a definition.  We provide an initial implementation
    here so that all subclass definitions can use 'inheritance override'.

    Returns: str
    """
    return '[meta.root.Object ' + self.id() + ']'

  def metaStream(self, fp=sys.stdout, indent='', depth=1):
    """Write a human-readable description of all fields to a stream.

    Meta auto-generates a metaStream method for any class that does not
    explicitly provide a definition. This definition is the root of the call
    change (each metaStream implementation is a post-extend of its parent's
    definition).

    IMPORTANT: This method does NOT write out an initial title for the
    object (using metaSummary() or anything else), because doing so would
    mean that each invocation of parent definition would add spurious
    titles, and its recursive use within metaStream implementations would
    also be problematic. We will either provide a wrapper method for
    printing a title, or add a 'showtitle' param to this method for enabling
    it (but if we add 'showtitle', the indent parameter is a bit more
    complicated to deal with).

    Args:
      fp: file
        Where to write the output.
      indent: str
        What to insert before each line of output.
      depth: int
        How deeply to recurse when invoking metaStream on fields. A value of 0
        means do not recurse into any fields. A value of 1 means recurse into
        fields present in this class, but not into the fields present within
        each field. etc.  Be forewarned that the code does NOT currently
        check for cycles, so specifying a large value for depth can produce
        redundant (and excessive) output.
    """
    # This root definition is a noop.

  def metaPrint(self, fp=sys.stdout, indent='', depth=1):
    """Print out a human-readable description of this object.

    This method invokes metaSummary() followed by metaStream().

    Notes:
     - subclasses rarely need to override this method, as one can customize
       metaSummary and metaStream instead.
     - subclasses rarely need to define metaSummary explicitly ... instead,
       add code to the 'summary' attribute of 'class' to provide code for
       this method
     - subclasses rarely need to define metaStream explicitly, as this
       method is just a printing of each field, and the code to print for
       a field can be explicitly provided via the 'stream' accessor within
       the 'scope' block of 'field'.

    Args:
      fp: file
        Where to write the output.
      indent: str
        What to insert before each line of output.
      depth: int
        How deeply to recurse when invoking metaStream on fields. A value of 0
        means do not recurse into any fields. A value of 1 means recurse into
        fields present in this class, but not into the fields present within
        each field. etc.  Be forewarned that the code does NOT currently
        check for cycles, so specifying a large value for depth can produce
        redundant (and excessive) output.
    """
    fp.write(indent + self.metaSummary());
    self.metaStream(fp=fp, indent=indent + '  ', depth=depth)

# The singleton instance of the metaclass.
ObjectClass = Object
