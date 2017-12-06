# Imports for class LoggerTest
import cStringIO                          # core meta: 434
import sys                                # core 

import meta.core                          # target meta: 432
import meta.testing                       # target meta: 432
import meta.testing                       # target 
# End imports for class LoggerTest


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
