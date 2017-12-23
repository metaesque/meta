#include "metax/root_test/ObjectTest.h"

namespace metax {
namespace root_test {


TEST_F(ObjectTest, test_Object) {
}

TEST_F(ObjectTest, test_meta) {
  // noop
}


}  // root_test
}  // metax


int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
