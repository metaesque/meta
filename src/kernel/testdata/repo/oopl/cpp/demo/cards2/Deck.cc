#include "demo/cards2/Deck.h"

namespace demo {
namespace cards2 {


void Deck::shuffle() {
  // static std::default_random_engine generator;
  auto& cards = this->cardsRef();
  int n = cards.size();
  for (int i = 0; i < n; ++i) {
    // 0 <= j <= i
    // std::uniform_int_distribution<int> distribution(0,i);
    // int j = distribution(generator);  // generates number in the range 0..i 
    int j = int(drand48() * (i+1));
    Card* tmp = cards[j];
    cards[j] = cards[i];
    cards[i] = tmp;
  }
}

metax::root::ObjectMetaRoot* Deck::meta() {
  return MetaDeck;
}


}  // cards2
}  // demo
