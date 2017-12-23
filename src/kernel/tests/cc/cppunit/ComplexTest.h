#ifndef ComplexTest_h
#define ComplexTest_h ComplexTest_h

#include "../TestCase.h"
#include "Complex.h"

namespace testit {

class ComplexTest : public meta::testing::TestCase {
 private:
  Complex *c1, *c2, *c3;

  void test_op_equals();

  CPPUNIT_TEST_SUITE(ComplexTest);
  CPPUNIT_TEST(test_op_equals);
  CPPUNIT_TEST_SUITE_END();

 public:
  void setUp();
  void tearDown();
  static int Main(int argc, char* argv[]);  
};

} // namespace testit

#endif // ComplexTest_h
