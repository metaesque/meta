#include "metax/root/ObjectMeta.h"

namespace metax {
namespace root {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
ObjectMeta* MetaObject = new ObjectMeta("metax.root.ObjectMeta", _bases, _symbols);

}  // root
}  // metax
