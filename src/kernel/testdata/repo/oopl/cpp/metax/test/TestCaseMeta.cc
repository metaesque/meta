#include "metax/test/TestCaseMeta.h"

namespace metax {
namespace test {


TestCaseMeta::TestCaseMeta(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols) : metax::root::ObjectMetaRoot(name, bases, symbols) {
  this->_Debug = false;
  this->_InstanceCount = 0;
  this->_WriteGoldens = false;
  this->_CanonicalStdout = nullptr;
  this->_CanonicalStderr = nullptr;
  this->_Interactive = false;
  // User-provided code follows.
  // Initialize the class-level vars!
}

static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
TestCaseMeta* MetaTestCase = new TestCaseMeta("metax.test.TestCaseMeta", _bases, _symbols);

}  // test
}  // metax
