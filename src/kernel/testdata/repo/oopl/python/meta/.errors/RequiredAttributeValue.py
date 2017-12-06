# Imports for class RequiredAttributeValue
import sys                                # core 

import meta.errors                        # target 
# End imports for class RequiredAttributeValue


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
