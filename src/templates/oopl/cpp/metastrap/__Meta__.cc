#include "metastrap/__Meta__.h"

namespace meta {

const std::string& NullStr() {
  static std::string result("");
  return result;
}

}
