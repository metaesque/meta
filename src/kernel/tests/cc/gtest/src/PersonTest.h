#include "gtest/gtest.h"

#include "src/Person.h"

namespace src {

// https://github.com/google/googletest/blob/master/googletest/docs/AdvancedGuide.md#global-set-up-and-tear-down
class Environment : public ::testing::Environment {
 public:
  Environment();
  virtual ~Environment();
  // https://github.com/google/googletest/blob/master/googletest/docs/AdvancedGuide.md#global-set-up-and-tear-down
  virtual void SetUp();
  virtual void TearDown();
};

// https://github.com/google/googletest/blob/master/googletest/docs/AdvancedGuide.md#sharing-resources-between-tests-in-the-same-test-case
class PersonTest : public ::testing::Test {
 protected:
  PersonTest();
  virtual ~PersonTest();
  // https://github.com/google/googletest/blob/master/googletest/docs/Primer.md#test-fixtures-using-the-same-data-configuration-for-multiple-tests
  virtual void SetUp();
  virtual void TearDown();
  // https://github.com/google/googletest/blob/master/googletest/docs/AdvancedGuide.md#sharing-resources-between-tests-in-the-same-test-case
  static void SetUpTestCase();
  static void TearDownTestCase();
};

}

