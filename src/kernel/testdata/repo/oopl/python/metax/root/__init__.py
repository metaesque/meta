"""The top-level classes that Meta provides."""
import metax.root


class ObjectMetaRoot(type):
  """The root of the metaclass hierarchy in Meta. 

  There are two ways we can handle the interaction between metaclasses
  in Meta and those in the baselang:
    1) The meta-level metaclass is-a baselang-provided metaclass
    2) The meta-level metaclass has-a baselang-provided metaclass
  See ../../README.md for details. Currently implementing variant #1.
  """

  # field metaname : @str
  #   The name of the class being represented by this metaclass.
  #   TODO(wmh): This field is not needed in python ... need a way to
  #   have 'specific' fields. But we do want to define metaname() to return
  #   the name as stored in the type metaclass.
  #   TODO(wmh): This should be a readonly field, so no setter or reffer.

  def metaname(cls):
    """here"""
    return cls._metaname

  def metanameIs(cls, value):
    """here

    Args:
      value: @str
    """
    cls._metaname = value

  def metanameRef(cls):
    """here"""
    return cls._metaname

  # field metabases : @vec<class>
  #   The parent classes of the class.
  #   TODO(wmh): This field is not needed in python ... need a way to
  #   have 'specific' fields.  But we do want to define metabases() to return
  #   the bases as stored in the type metaclass.
  #   TODO(wmh): This should be a readonly field, so no setter or reffer.

  def metabases(cls):
    """here"""
    return cls._metabases

  def metabasesIs(cls, value):
    """here

    Args:
      value: @vec<class>
    """
    cls._metabases = value

  def metabasesRef(cls):
    """here"""
    return cls._metabases

  # field metasymbols : @map
  #   The symbols available within the class.
  #   TODO(wmh): This field is not needed in python ... need a way to
  #   have 'specific' fields.  But we do want to define metasymbols() to return
  #   the symbols as stored in the type metaclass.
  #   TODO(wmh): This should be a readonly field, so no setter or reffer.

  def metasymbols(cls):
    """here"""
    return cls._metasymbols

  def metasymbolsIs(cls, value):
    """here

    Args:
      value: @map
    """
    cls._metasymbols = value

  def metasymbolsRef(cls):
    """here"""
    return cls._metasymbols

  def __init__(cls, name, bases, symbols):
    """here
    Every user-defined class has an auto-generated metaclass created for it,
    and that metaclass inherits (eventually) from this class.  The meta
    compiler implicitly inserts a params: block in meta class initializers
    (if users define a meta-level lifecycle construct, they should not
    specify params:, as that will be an error).

    This signature is currently motivated by the signature of metaclasses in
    Python. As additional baselangs are added to Meta, we may need to
    generalize this implicit signature. Note that Javascript and C++ do not
    have metaclasses, so we are not constrained by these baselangs). But when
    we add in support for Java, we will need to establish whether
    java.lang.Class can be subclassed (or whether ObjectMeta will
    need to act as a wrapper around a java.lang.Class instance) and how that
    influences this signature.

    Args:
      name: &str
        The name of the class being created
      bases: &vec<class>
        The parent classes of the class (instances of metaclasses)
      symbols: &map
        The symbols available within the class.
    """
    super(ObjectMetaRoot, cls).__init__(name, bases, symbols)
    cls._metaname = ''
    cls._metabases = []
    cls._metasymbols = {}
    # User-provided code follows.


class ObjectMeta(ObjectMetaRoot):
  """Auto-generated meta class for Object."""


class Object(object):
  """Except in special circumstances, every class defined within Meta inherits
  from this class. Every base language provides a specialized implementation
  that defines functionality useful in implementing Meta-level semantics
  within that base language. Some of the methods defined here are present in
  all languages, some are only present in a subset of languages or in just one
  language.

  This class does NOT introduce any instance-level state, but does define
  a significant amount of instance-level and meta-level functionality
  available to every subclass intance and subclass respectively.

  Note that the metaparent of this class is always ObjectMetaRoot. Any
  class that inherits from Object will have a metaclass that inherits
  from ObjectMetaRoot.  Any user-defined meta class by default inherits
  from ObjectMetaRoot (semantics implemented in
  metax.c.ClassConstruct.metaClassInfo().

  Meta:suppress: JSC_UNKNOWN_EXPR_TYPE
  """
  __metaclass__ = ObjectMeta

  def meta(self):
    """here"""
    result = self.__class__
    assert result is Object
    assert result is MetaObject
    return result

MetaObject = Object


class Error(Exception):
  """The exception hierarchy is documented in the following places:
    python: https://docs.python.org/2/library/exceptions.html
    javascript: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
  """
