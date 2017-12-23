#include "demo/cards2/PileMeta.h"

namespace demo {
namespace cards2 {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
PileMeta* MetaPile = new PileMeta("demo.cards2.PileMeta", _bases, _symbols);

}  // cards2
}  // demo
