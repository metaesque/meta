# -*- coding: utf-8 -*-
"""Unit tests for meta.core"""
import cStringIO
import sys

import meta.core
import meta.testing


class LoggerTestMetaClass(meta.testing.TestCaseMetaClass):
  """Meta class of meta.core_test.LoggerTest."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(LoggerTestMetaClass, cls).__init__(
      meta__dct, meta__bases, meta__name)
    # User-provided code follows.


class LoggerTest(meta.testing.TestCase):
  """Unit tests for class Logger."""
  __metaclass__ = LoggerTestMetaClass

  def __init__(self, meta__name):
    """Initializer.

    Args:
      meta__name: str
    """
    super(LoggerTest, self).__init__(meta__name)
    # User-provided code follows.

  def setUp(self):
    super(LoggerTest, self).setUp()
    # User-provided code follows.
    self._fp = cStringIO.StringIO()
    # TODO(wmh): meta.compiler doesn't exist. Which Logger was I
    # planning to use?  wmh.Log?
    self._logger = None  # meta.compiler.lib.Logger(fp=self._fp)

  def test_fpIs(self):
    print 'Fix LoggerTest.test_fp'
    return
    self.assertEqual(self._fp, self._logger.fp())
    fp = cStringIO.StringIO()
    self._logger.fpIs(fp)
    self.assertEqual(fp, self._logger.fp())

  def test_info(self):
    print 'Fix LoggerTest.test_info'
    return
    self.assertEqual(self._fp, self._logger.fp())
    fp = cStringIO.StringIO()
    self._logger.fpIs(fp)
    self.assertEqual(fp, self._logger.fp())

  def test_indent(self):
    print 'Fix LoggerTest.test_indent'
    return
    self.assertEqual(0, self._logger._level)
    self._logger.indent()
    self.assertEqual(1, self._logger._level)
    self._logger.undent()
    self.assertEqual(0, self._logger._level)

  def test_undent(self):
    print 'Fix LoggerTest.test_undent'
    return
    self.assertEqual(0, self._logger._level)
    self._logger.indent()
    self.assertEqual(1, self._logger._level)
    self._logger.undent()
    self.assertEqual(0, self._logger._level)


if __name__ == '__main__':
  meta.testing.main()
