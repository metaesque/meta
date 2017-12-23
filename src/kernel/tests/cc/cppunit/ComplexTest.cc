# include "ComplexTest.h"

namespace testit {

void ComplexTest::setUp() {
  c1 = new Complex(1, 2);
  c2 = new Complex(3, 4);
  c3 = new Complex(-2, 7);  
}

void ComplexTest::tearDown() {
  delete c1;
  delete c2;
  delete c3;
}

void ComplexTest::test_op_equals() {
  CPPUNIT_ASSERT(!(*c1 == *c2));
}

int ComplexTest::Main(int argc, char* argv[]) {
  CppUnit::TextTestRunner runner;
  runner.addTest(ComplexTest::suite());
  bool wasSucessful = runner.run("");
  return wasSucessful ? 0 : 1;
}

}  // namespace testit

//int main(int argc, char* argv[]) { return testit::ComplexTest::Main(argc, argv); }
