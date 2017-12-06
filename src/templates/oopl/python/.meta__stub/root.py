"""The top-level classes that Meta provides."""
import exceptions
import inspect
import os
import sys
import threading

import meta.errors
import meta.root


class Object(object):
  """Except in special circumstances, every class defined within Meta
  inherits from this class. Every base language provides a specialized
  implementation that provides functionality useful in implementing
  Meta-level semantics within that base language.  Some of the methods
  defined here are present in all languages, some are only present in
  a subset of languages or in just one language.
  """

  # meta field StrNull : str
  #   The representation of 'null' for use with '&str' and '*str' types.
  StrNull =  None

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
      fqn: *str
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
    parts = fqn.split('.')
    if test:
      parts[-1] += 'Test'
      parts[-2] += '_test'
    parts[-1] += '_' + resource_id
    parts[-2] = '.' + parts[-2]
    path = '/'.join(parts)
    return path


class Meta__Object(object):
  """Meta class of Object."""

  # instance field StrNull : str
  #   The representation of 'null' for use with '&str' and '*str' types.

  def Resource(self, resource_id, fqn=None, test=False):
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
    parts = fqn.split('.')
    if test:
      parts[-1] += 'Test'
      parts[-2] += '_test'
    parts[-1] += '_' + resource_id
    parts[-2] = '.' + parts[-2]
    path = '/'.join(parts)
    return path

protected = Object._meta__protected
private = Object._meta__private


class Exception(Exception):
  """# The class that all exception classes within the Meta universe should
  # inherit from.
  """
  pass


class Meta__Exception(object):
  """Meta class of Exception."""
  pass
