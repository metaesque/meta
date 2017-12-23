# include <iostream>

# include "src/PersonTest.h"

using namespace std;

namespace src {

Environment::Environment() {
  cout << "In Environment::Environment" << endl;
}

Environment::~Environment() {
  cout << "In Environment::~Environment" << endl;
}

void Environment::SetUp() {
  cout << "In Environment::SetUp" << endl;
}

void Environment::TearDown() {
  cout << "In Environment::TearDown" << endl;
}

PersonTest::PersonTest() {
  cout << "In PersonTest::PersonTest" << endl;
}

PersonTest::~PersonTest() {
  cout << "In PersonTest::~PersonTest" << endl;
}

void PersonTest::SetUp() {
  cout << "In PersonTest::SetUp" << endl;
}

void PersonTest::TearDown() {
  cout << "In PersonTest::TearDown" << endl;
}

void PersonTest::SetUpTestCase() {
  cout << "In PersonTest::SetUpTestCase" << endl;
}

void PersonTest::TearDownTestCase() {
  cout << "In PersonTest::TearDownTestCase" << endl;
}

TEST_F(PersonTest, basics) {
  src::Person person("Bob", 97, 1.82);
  EXPECT_EQ(97.0, person.weight());
}

TEST_F(PersonTest, bmi) {
  src::Person person("Bob", 97, 1.82);
  EXPECT_EQ(97.0, person.weight());
  ASSERT_NEAR(29.2839, person.bmi(), 0.00001);
}

}  // end namespace 'src'

// https://github.com/google/googletest/blob/master/googletest/docs/Primer.md#writing-the-main-function

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  ::testing::AddGlobalTestEnvironment(new ::src::Environment);
  return RUN_ALL_TESTS();
}


