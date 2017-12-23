import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
##########  End Imports  ##########


class PileTest(demo.cards2_test.TestCase):
  """Auto-generated test class for demo.cards2.Pile"""
  __metaclass__ = PileTestMeta

  def test_meta(self):
    """here"""
    # noop
    pass
########## Start Harness ##########


if __name__ == '__main__':
  metax.test.main()
