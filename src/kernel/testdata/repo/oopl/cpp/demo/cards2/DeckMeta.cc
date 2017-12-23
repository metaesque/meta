#include "demo/cards2/DeckMeta.h"

namespace demo {
namespace cards2 {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
DeckMeta* MetaDeck = new DeckMeta("demo.cards2.DeckMeta", _bases, _symbols);

}  // cards2
}  // demo
