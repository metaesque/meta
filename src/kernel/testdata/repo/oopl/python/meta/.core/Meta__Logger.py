# Imports for class Meta__Logger
import sys                                # core 

import meta.root                          # target 
# End imports for class Meta__Logger


class Meta__Logger(meta.root.Meta__Object):
  """Meta class of meta.core.Logger."""
  pass

# The singleton instance of the metaclass.
MetaLogger = Meta__Logger()
