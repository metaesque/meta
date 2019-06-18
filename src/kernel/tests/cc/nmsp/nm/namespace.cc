#include "nm/namespace.h"

namespace nm {

int VARIABLE = 11;

int FUNCTION(int a) {
  std::cout << "Here in nm namespace with a=" << a
            << " VARIABLE=" << VARIABLE
            << std:: endl;
  return a * VARIABLE;
}

}  // namespace nm
