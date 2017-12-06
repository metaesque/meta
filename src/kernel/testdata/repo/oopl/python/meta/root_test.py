# -*- coding: utf-8 -*-
"""Unit tests for meta.root"""
import sys

import meta.root
import meta.testing


class ObjectTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.root_test.ObjectTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ObjectTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class ObjectTest(meta.testing.TestCase):
  """Unit tests for class Object."""
  __metaclass__ = ObjectTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(ObjectTest, self).__init__(meta__name)
    # User-provided code follows.


class ExceptionTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.root_test.ExceptionTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(ExceptionTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class ExceptionTest(meta.testing.TestCase):
  """Unit tests for class Exception."""
  __metaclass__ = ExceptionTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(ExceptionTest, self).__init__(meta__name)
    # User-provided code follows.


if __name__ == '__main__':
  meta.testing.main()
