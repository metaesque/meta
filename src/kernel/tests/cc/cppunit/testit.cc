#include "ComplexTest.h"
#include "StrTest.h"

int main(int argc, char* argv[]) {
  // if command line contains "--selftest" then this is the post build check
  // => the output must be in the compiler error format.
  bool selftest = (argc > 1)  && (std::string("--selftest") == argv[1]);

  CppUnit::TextTestRunner runner;
  runner.addTest(testit::StrTest::suite());
  runner.addTest(testit::ComplexTest::suite());

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
