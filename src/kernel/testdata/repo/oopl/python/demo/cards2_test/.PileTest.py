import demo.cards2  # target=//demo/cards2:cards2
import demo.cards2_test  # target=//demo/cards2_test:cards2_test
import meta.testing  # target=//meta/testing:testing
##########  End Imports  ##########


class PileTest(meta.testing.TestCase):
  """Auto-generated test class for demo.cards2.Pile"""
  __metaclass__ = PileTest__Meta

  def __init__(test, meta__name):
    super(PileTest, test).__init__(meta__name)
    # User-provided code follows.
########## Start Harness ##########


if __name__ == '__main__':
  meta.testing.main()
