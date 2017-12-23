#include "demo/cards2_test/DeckTest.h"

namespace demo {
namespace cards2_test {


TEST_F(DeckTest, test_shuffle) {
}

TEST_F(DeckTest, test_meta) {
  // noop
}


}  // cards2_test
}  // demo


int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
