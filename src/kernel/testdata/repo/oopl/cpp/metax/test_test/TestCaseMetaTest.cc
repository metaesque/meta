#include "metax/test_test/TestCaseMetaTest.h"

namespace metax {
namespace test_test {


TEST_F(TestCaseMetaTest, test_TestCaseMeta) {
}


}  // test_test
}  // metax


int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
