# -*- coding: utf-8 -*-
"""Exception classes for the Meta compiler.

IMPORTANT: Classes in this namespace cannot inherit from any class
in meta.root or a BUILD circularity will result (since meta.root.Object
relies on meta.errors).

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
"""
import sys

import meta.errors


class ErrorMetaClass(type):
  """Meta class of meta.errors.Error."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ErrorMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class Error(Exception):
  """This is the top-level (within Meta) exception class. It may inherit from
  some non-meta class defined within the base language, but this class
  provides the interface common across all languages for raising exceptions.

  Meta:suppress: reportUnknownTypes
  """
  __metaclass__ = ErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(Error, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ErrorClass = Error


class InvalidTypeMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InvalidType."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InvalidTypeMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class InvalidType(Error):
  __metaclass__ = InvalidTypeMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidType, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidTypeClass = InvalidType


class InvalidConstructIdMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InvalidConstructId."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InvalidConstructIdMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class InvalidConstructId(Error):
  __metaclass__ = InvalidConstructIdMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidConstructId, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidConstructIdClass = InvalidConstructId


class InvalidAttributeKeyMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InvalidAttributeKey."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InvalidAttributeKeyMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class InvalidAttributeKey(Error):
  __metaclass__ = InvalidAttributeKeyMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InvalidAttributeKey, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InvalidAttributeKeyClass = InvalidAttributeKey


class RequiredAttributeValueMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.RequiredAttributeValue."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(RequiredAttributeValueMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class RequiredAttributeValue(Error):
  __metaclass__ = RequiredAttributeValueMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(RequiredAttributeValue, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
RequiredAttributeValueClass = RequiredAttributeValue


class InternalErrorMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.InternalError."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(InternalErrorMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class InternalError(Error):
  __metaclass__ = InternalErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(InternalError, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
InternalErrorClass = InternalError


class SyntaxErrorMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.SyntaxError."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(SyntaxErrorMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class SyntaxError(Error):
  __metaclass__ = SyntaxErrorMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(SyntaxError, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
SyntaxErrorClass = SyntaxError


class ExitingMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.Exiting."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ExitingMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class Exiting(Error):
  __metaclass__ = ExitingMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(Exiting, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ExitingClass = Exiting


class PrivateMethodMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.PrivateMethod."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(PrivateMethodMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class PrivateMethod(Error):
  __metaclass__ = PrivateMethodMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(PrivateMethod, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
PrivateMethodClass = PrivateMethod


class ProtectedMethodMetaClass(ErrorMetaClass):
  """Meta class of meta.errors.ProtectedMethod."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ProtectedMethodMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class ProtectedMethod(Error):
  __metaclass__ = ProtectedMethodMetaClass

  def __init__(self, *args, **kwds):
    """Initializer.

    Args:
      args: list
      kwds: dict
    """
    super(ProtectedMethod, self).__init__(*args, **kwds)
    # User-provided code follows.

# The singleton instance of the metaclass.
ProtectedMethodClass = ProtectedMethod
