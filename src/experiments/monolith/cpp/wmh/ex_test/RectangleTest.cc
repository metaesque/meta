// See https://google.github.io/googletest/primer.html

#import <iostream>
#include <gtest/gtest.h>
#include "cpp/wmh/ex/Rectangle.hh"

namespace wmh {
namespace ex {

class RectangleTest : public ::testing::Test {
 protected:
  // You can remove any or all of the following functions if their bodies
  // would be empty.
  wmh::ex::Rectangle _rect1;
  const wmh::ex::Rectangle& rect1() const { return this->_rect1; }

  RectangleTest() : _rect1(5, 7) {
     // You can do set-up work for each test here.
  }

  ~RectangleTest() override {
     // You can do clean-up work that doesn't throw exceptions here.
  }

  // If the constructor and destructor are not enough for setting up
  // and cleaning up each test, you can define the following methods:

  void SetUp() override {
     // Code here will be called immediately after the constructor (right
     // before each test).
  }

  void TearDown() override {
     // Code here will be called immediately after each test (right
     // before the destructor).
  }

  // Class members declared here can be used by all tests in the test suite
  // for Rectangle.
};

TEST_F(RectangleTest, test_area) {
  ASSERT_EQ(35, this->rect1().area());
}

}  // namespace ex
}  // namespace wmh
