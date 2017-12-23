#include "demo/cards2/Card.h"

namespace demo {
namespace cards2 {


Card::Card(int32_t rank, int32_t suit) {
  this->rankIs(rank);
  this->suitIs(suit);
}

metax::root::ObjectMetaRoot* Card::meta() {
  return MetaCard;
}


}  // cards2
}  // demo
