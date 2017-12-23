
// REM ######################################################################
// REM #include "StrTest.h"
#include "StrTest.h"

namespace testit {

// REM ######################################################################
// REM # __CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(StrTest, "StrTest");
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(StrTest, "StrTest");

// REM ######################################################################
// REM # Code

void StrTest::setUp() {
  s1 = new Str((char *)"test 1");
  s2 = new Str((char *)"another test");
  m_value1 = 2.0;
  m_value2 = 3.0;
}

void StrTest::tearDown() {
  // std::cout << "tearDown" << std::endl;
  delete s1;
  delete s2;
}

void StrTest::test_setbuffer() {
  CPPUNIT_ASSERT(strcmp("test 1", s1->buffer) == 0);
  CPPUNIT_ASSERT_EQUAL(6, s1->length);
  CPPUNIT_ASSERT (1 == 1);
}

void StrTest::test_op_brackets() {
  CPPUNIT_ASSERT (2 == 2);
}

void StrTest::test_size() {
  std::auto_ptr<long>	l1 (new long (12));
  std::auto_ptr<long>	l2 (new long (12));

  // REM ######################################################################
  // REM # ASSERTS
  CPPUNIT_ASSERT_DOUBLES_EQUAL (m_value1, 2.0, 0.01);
  CPPUNIT_ASSERT_DOUBLES_EQUAL (m_value2, 3.0, 0.01);
  CPPUNIT_ASSERT_EQUAL (12, 12);
  CPPUNIT_ASSERT_EQUAL (12L, 12L);
  CPPUNIT_ASSERT_EQUAL (*l1, *l2);
  
  CPPUNIT_ASSERT(12L == 12L);
  CPPUNIT_ASSERT_DOUBLES_EQUAL (12.0, 11.99, 0.5);
}

int StrTest::Main(int argc, char* argv[]) {
  // if command line contains "-selftest" then this is the post build check
  // => the output must be in the compiler error format.
  bool selftest = (argc > 1)  && (std::string("--selftest") == argv[1]);

  CppUnit::TextTestRunner runner;
  runner.addTest(StrTest::suite()); // Add the top suite to the test runner

  if ( selftest ) {
    // Change the default outputter to a compiler error format outputter
    // The test runner owns the new outputter.
    runner.setOutputter(
      CppUnit::CompilerOutputter::defaultOutputter(
        &runner.result(), std::cerr));
  }

  // Run the test.
  bool wasSucessful = runner.run("");

  // Return error code 1 if any tests failed.
  return wasSucessful ? 0 : 1;
}

}  // namespace testit

//int main(int argc, char* argv[]) { return testit::StrTest::Main(argc, argv); }

