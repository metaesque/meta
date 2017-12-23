#include "metax/root_test/ErrorTestMeta.h"

namespace metax {
namespace root_test {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
ErrorTestMeta* MetaErrorTest = new ErrorTestMeta("metax.root_test.ErrorTestMeta", _bases, _symbols);

}  // root_test
}  // metax
