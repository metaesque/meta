#ifndef demo_cards2_Card_h
#define demo_cards2_Card_h 1

#include "demo/cards2/CardMeta.h"
#include "metax/root/Object.h"

namespace demo {
namespace cards2 {

// A card with suit and rank.
// 
// In this implementation, Card instances do not know about the Deck they
// belong to. See cards3.meta2 for a version in which Card maintains a Deck
// (this introduces a circularity, as Deck needs Card and Card needs Deck).
class Card : public metax::root::Object {

  // field rank : int
  //   Rank as simple integer. Deck assigns display semantics to rank values.
  private: int32_t _rank;
  public: virtual int32_t rank() const { return this->_rank; }
  public: virtual void rankIs(int32_t value) { this->_rank = value; }
  public: virtual int32_t& rankRef() { return this->_rank; }

  // field suit : int
  //   Suit as simple integer. Deck assigns display semantics to suit values.
  private: int32_t _suit;
  public: virtual int32_t suit() const { return this->_suit; }
  public: virtual void suitIs(int32_t value) { this->_suit = value; }
  public: virtual int32_t& suitRef() { return this->_suit; }
  // It should not be necessary to create Card instances directly.
  // Instead, one should create instances of Deck, and use the cards
  // it contains.
  public: Card(int32_t rank, int32_t suit);
  public: virtual metax::root::ObjectMetaRoot* meta();
};

}  // cards2
}  // demo


#endif // demo_cards2_Card_h
