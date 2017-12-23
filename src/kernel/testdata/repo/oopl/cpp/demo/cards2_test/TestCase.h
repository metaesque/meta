#ifndef demo_cards2_test_TestCase_h
#define demo_cards2_test_TestCase_h 1

#include "metax/test/TestCase.h"

namespace demo {
namespace cards2_test {

class TestCase : public metax::test::TestCase {

  // field TestVar : int
  private: int32_t _TestVar;
  public: virtual int32_t TestVar() const { return this->_TestVar; }
  public: virtual void TestVarIs(int32_t value) { this->_TestVar = value; }
  public: virtual int32_t& TestVarRef() { return this->_TestVar; }
  public: TestCase(const std::string& meta__name = "");
};

}  // cards2_test
}  // demo


#endif // demo_cards2_test_TestCase_h
