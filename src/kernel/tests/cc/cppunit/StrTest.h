#ifndef StrTest_h
#define StrTest_h StrTest_h

// REM ######################################################################
// REM # StrTest.h includes
# include "../TestCase.h"

// The class this class is testing.
# include "Str.h"

namespace testit {

class StrTest : public meta::testing::TestCase {
 private: 
  Str* s1;
  Str* s2;
  double m_value1;
  double m_value2;

  void test_setbuffer();
  void test_op_brackets();
  void test_size();

  // REM ######################################################################
  // REM # ___CPPUNIT_TEST_SUITE(StrTest)
  CPPUNIT_TEST_SUITE(StrTest);
  CPPUNIT_TEST(test_setbuffer);
  CPPUNIT_TEST(test_op_brackets);
  CPPUNIT_TEST(test_size);
  CPPUNIT_TEST_SUITE_END();
  // REM # ___CPPUNIT_TEST_SUITE_END()
  // REM ######################################################################
  // The above culminates in
  //   static CppUnit::TestSuite *suite()
  // being define.

 public:
  void setUp();
  void tearDown();
  static int Main(int argc, char* argv[]);
};

}  // namespace testit

#endif  // StrTest_h
