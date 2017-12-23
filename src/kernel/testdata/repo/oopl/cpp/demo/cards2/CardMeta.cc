#include "demo/cards2/CardMeta.h"

namespace demo {
namespace cards2 {


static std::vector<void**> _bases;
static std::map<std::string, void**> _symbols;
CardMeta* MetaCard = new CardMeta("demo.cards2.CardMeta", _bases, _symbols);

}  // cards2
}  // demo
