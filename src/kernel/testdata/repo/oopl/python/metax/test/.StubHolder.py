import metax.test  # target=//metax/test:test
##########  End Imports  ##########


class StubHolder(object):
  """Support class for stubbing methods out for unit testing.

  Sample Usage:

  You want os.path.exists() to always return true during testing.

     stubs = StubHolder()
     stubs.Set(os.path, 'exists', lambda x: 1)
       ...
     stubs.CleanUp()

  The above changes os.path.exists into a lambda that returns 1.  Once
  the ... part of the code finishes, the CleanUp() looks up the old
  value of os.path.exists and restores it.
  """
  __metaclass__ = StubHolderMeta

  def __init__(self):
    """here"""
    super(StubHolder, self).__init__()
    # User-provided code follows.
    self.cache = []
    self.stubs = []

  def __del__(self):
    """here
    Do not rely on the destructor to undo your stubs.

    You cannot guarantee exactly when the destructor will get called without
    relying on implementation details of a Python VM that may change.
    """
    self.CleanUp()

  def __enter__(self):
    """here"""
    return self

  def __exit__(self, unused_exc_type, unused_exc_value, unused_tb):
    """here

    Args:
      unused_exc_type: any
      unused_exc_value: any
      unused_tb: any
    """
    self.CleanUp()

  def CleanUp(self):
    """here
    Undoes all SmartSet() & Set() calls, restoring original definitions.
    """
    self.SmartUnsetAll()
    self.UnsetAll()

  def SmartSet(self, obj, attr_name, new_attr):
    """here
    Replace obj.attr_name with new_attr.

    This method is smart and works at the module, class, and instance level
    while preserving proper inheritance. It will not stub out C types however
    unless that has been explicitly allowed by the type.

    This method supports the case where attr_name is a staticmethod or a
    classmethod of obj.

    Notes:
     - If obj is an instance, then it is its class that will actually be
       stubbed. Note that the method Set() does not do that: if obj is
       an instance, it (and not its class) will be stubbed.
     - The stubbing is using the builtin getattr and setattr. So, the __get__
       and __set__ will be called when stubbing.

    Raises:
      AttributeError: If the attribute cannot be found.

    Args:
      obj: any
        The object whose attributes we want to modify.
      attr_name: str
        The name of the attribute to modify.
      new_attr: any
        The new value for the attribute.
    """
    if (inspect.ismodule(obj) or
        (not inspect.isclass(obj) and attr_name in obj.__dict__)):
      orig_obj = obj
      orig_attr = getattr(obj, attr_name)
    else:
      if not inspect.isclass(obj):
        mro = list(inspect.getmro(obj.__class__))
      else:
        mro = list(inspect.getmro(obj))

      mro.reverse()

      orig_attr = None
      found_attr = False

      for cls in mro:
        try:
          orig_obj = cls
          orig_attr = getattr(obj, attr_name)
          found_attr = True
        except AttributeError:
          continue

      if not found_attr:
        raise AttributeError('Attribute not found.')

    # Calling getattr() on a staticmethod transforms it to a 'normal' function.
    # We need to ensure that we put it back as a staticmethod.
    old_attribute = obj.__dict__.get(attr_name)
    if old_attribute is not None and isinstance(old_attribute, staticmethod):
      orig_attr = staticmethod(orig_attr)

    self.stubs.append((orig_obj, attr_name, orig_attr))
    setattr(orig_obj, attr_name, new_attr)

  def SmartUnsetAll(self):
    """here
    Reverses SmartSet() calls, restoring things to original definitions.

    This method is automatically called when the StubOutForTesting()
    object is deleted; there is no need to call it explicitly.

    It is okay to call SmartUnsetAll() repeatedly, as later calls have
    no effect if no SmartSet() calls have been made.
    """
    for args in reversed(self.stubs):
      setattr(*args)

    self.stubs = []

  def Set(self, parent, child_name, new_child):
    """here
    In parent, replace child_name's old definition with new_child.

    The parent could be a module when the child is a function at
    module scope.  Or the parent could be a class when a class' method
    is being replaced.  The named child is set to new_child, while the
    prior definition is saved away for later, when UnsetAll() is
    called.

    This method supports the case where child_name is a staticmethod or a
    classmethod of parent.

    Args:
      parent: *any
        The_context_in_which_the_attribute_child_name_is_to_be_changed.
      child_name: *any
        The_name_of_the_attribute_to_change.
      new_child: *any
        The_new_value_of_the_attribute
    """
    old_child = getattr(parent, child_name)

    old_attribute = parent.__dict__.get(child_name)
    if old_attribute is not None and isinstance(old_attribute, staticmethod):
      old_child = staticmethod(old_child)

    self.cache.append((parent, old_child, child_name))
    setattr(parent, child_name, new_child)

  def UnsetAll(self):
    """here
    Reverses Set() calls, restoring things to their original definitions.

    This method is automatically called when the StubOutForTesting()
    object is deleted; there is no need to call it explicitly.

    It is okay to call UnsetAll() repeatedly, as later calls have no
    effect if no Set() calls have been made.
    """
    # Undo calls to Set() in reverse order, in case Set() was called on the
    # same arguments repeatedly (want the original call to be last one undone)
    for (parent, old_child, child_name) in reversed(self.cache):
      setattr(parent, child_name, old_child)
    self.cache = []

  def meta(self):
    """here"""
    result = self.__class__
    assert result is StubHolder
    assert result is MetaStubHolder
    return result

MetaStubHolder = StubHolder
