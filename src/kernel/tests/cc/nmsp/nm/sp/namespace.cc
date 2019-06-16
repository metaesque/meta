#include "nm/sp/namespace.h"

namespace nm {
namespace sp {

int VARIABLE = 21;

int FUNCTION(int a) {
  std::cout << "Here in nm.sp namespace with a=" << a
            << " VARIABLE=" << VARIABLE
            << std:: endl;
  return a * VARIABLE;
}

}  // namespace sp
}  // namespace nm
