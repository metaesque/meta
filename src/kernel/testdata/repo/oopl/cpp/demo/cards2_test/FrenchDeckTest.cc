#include "demo/cards2_test/FrenchDeckTest.h"

namespace demo {
namespace cards2_test {


TEST_F(FrenchDeckTest, test_FrenchDeck) {
}

TEST_F(FrenchDeckTest, test_asStr) {
  demo::cards2::FrenchDeck deck;
  (*this).iseqstr("AS", deck.asStr(deck.cards()[0]));
  (*this).iseqstr("5D", deck.asStr(deck.cards()[17]));
}

TEST_F(FrenchDeckTest, test_meta) {
  // noop
}


}  // cards2_test
}  // demo


int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
