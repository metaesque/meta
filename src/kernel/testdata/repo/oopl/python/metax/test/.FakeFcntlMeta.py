import metax.root  # target=//metax/root:root
##########  End Imports  ##########


class FakeFcntlMeta(metax.root.ObjectMetaRoot):
  """Auto-generated meta class for metax.test.FakeFcntl."""

  def __init__(cls, name, bases, symbols):
    """here

    Args:
      name: &str
      bases: &vec<class>
      symbols: &map
    """
    super(FakeFcntlMeta, cls).__init__(name, bases, symbols)
    # User-provided code follows.
    cls.LOCK_UN = fcntl.LOCK_UN
    cls.LOCK_SH = fcntl.LOCK_SH
    cls.LOCK_EX = fcntl.LOCK_EX
