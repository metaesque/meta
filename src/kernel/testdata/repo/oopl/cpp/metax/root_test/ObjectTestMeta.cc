#include "metax/root_test/ObjectTestMeta.h"

namespace metax {
namespace root_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
ObjectTestMeta* MetaObjectTest = new ObjectTestMeta("metax.root_test.ObjectTestMeta", _bases, _symbols);

}  // root_test
}  // metax
