#include "metastrap/__Meta__.h"

namespace metax {

const std::string& NullStr() {
  static std::string result("");
  return result;
}

}
