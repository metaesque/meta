#include "metax/root/ObjectMetaRoot.h"

namespace metax {
namespace root {


ObjectMetaRoot::ObjectMetaRoot(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols) {
  this->metanameIs(name);
  this->metabasesIs(bases);
  this->metasymbolsIs(symbols);
}


}  // root
}  // metax
