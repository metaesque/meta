#include "metax/test_test/TestCaseTestMeta.h"

namespace metax {
namespace test_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
TestCaseTestMeta* MetaTestCaseTest = new TestCaseTestMeta("metax.test_test.TestCaseTestMeta", _bases, _symbols);

}  // test_test
}  // metax
