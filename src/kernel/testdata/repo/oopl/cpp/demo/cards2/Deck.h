#ifndef demo_cards2_Deck_h
#define demo_cards2_Deck_h 1

#include "demo/cards2/DeckMeta.h"
#include "demo/cards2/Pile.h"
#include <stdlib.h>

namespace demo {
namespace cards2 {

// A pre-determined collection of Card instances.
class Deck : public demo::cards2::Pile {
  using demo::cards2::Pile::Pile;
  // http://wikipedia.org/wiki/Fisher-Yates_shuffle
  public: virtual void shuffle();
  public: virtual metax::root::ObjectMetaRoot* meta();
};

}  // cards2
}  // demo


#endif // demo_cards2_Deck_h
