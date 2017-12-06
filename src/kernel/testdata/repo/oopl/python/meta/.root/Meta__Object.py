# Imports for class Meta__Object
import sys                                # core 

import meta.root                          # target 
# End imports for class Meta__Object


class Meta__Object(object):
  """Meta class of meta.root.Object."""
  
  # instance field StrNull : *str
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
      fqn: str
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

  def metaSummary(self, indent=''):
    """Auto-generated one-line summary of the object.

    Args:
      indent: str
        Indentation to insert before each line.

    Returns: str
    """
    return 'meta.root.Meta__Object %s' % id(self)

  def metaStream(self, fp=sys.stdout, indent='', depth=1):
    """Auto-generated human-readable description of the object.

    Args:
      fp: file
        Where to write the output.
      indent: str
        Indentation to insert before each line.
      depth: int
        How many levels to recurse.
    """
    subindent = indent + '  '

# The singleton instance of the metaclass.
MetaObject = Meta__Object()
