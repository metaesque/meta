# Imports for class TestCaseMetaClass
import sys                                # core 
# End imports for class TestCaseMetaClass


class TestCaseMetaClass(meta.root.ObjectMetaClass):
  """Meta class of meta.testing_test.TestCase."""

  def __init__(cls, meta__name, meta__bases, meta__dct):
    """Initializer.

    Args:
      meta__name: str
      meta__bases: list
      meta__dct: dict
    """
    super(TestCaseMetaClass, cls).__init__(meta__dct, meta__bases, meta__name)
    # User-provided code follows.
