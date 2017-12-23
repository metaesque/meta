#include "demo/cards2_test/PileTest.h"

namespace demo {
namespace cards2_test {


TEST_F(PileTest, test_meta) {
  // noop
}


}  // cards2_test
}  // demo


int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
