#ifndef demo_cards2_FrenchDeckMeta_h
#define demo_cards2_FrenchDeckMeta_h 1

#include "demo/cards2/DeckMeta.h"

namespace demo {
namespace cards2 {

// Auto-generated meta class for demo.cards2.FrenchDeck.
class FrenchDeckMeta : public demo::cards2::DeckMeta {

  // field Suits : @vec<@str>
  //   Indices are suit integers, values are suit names.
  private: std::vector<std::string> _Suits;
  public: virtual const std::vector<std::string>& Suits() const { return this->_Suits; }
  public: virtual void SuitsIs(std::vector<std::string> value) { this->_Suits = value; }
  public: virtual std::vector<std::string>& SuitsRef() { return this->_Suits; }

  // field Ranks : @vec<@str>
  //   Indices are suit integers, values are suit names.
  private: std::vector<std::string> _Ranks;
  public: virtual const std::vector<std::string>& Ranks() const { return this->_Ranks; }
  public: virtual void RanksIs(std::vector<std::string> value) { this->_Ranks = value; }
  public: virtual std::vector<std::string>& RanksRef() { return this->_Ranks; }
  public: FrenchDeckMeta(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols);
};
extern FrenchDeckMeta* MetaFrenchDeck;

}  // cards2
}  // demo


#endif // demo_cards2_FrenchDeckMeta_h
