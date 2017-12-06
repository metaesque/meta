# Imports for class Exiting
import sys                                # core 

import meta.errors                        # target 
# End imports for class Exiting


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
