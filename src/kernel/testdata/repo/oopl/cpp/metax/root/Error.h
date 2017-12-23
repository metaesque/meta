#ifndef metax_root_Error_h
#define metax_root_Error_h 1

#include "metax/root/ObjectMetaRoot.h"
#include <exception>

namespace metax {
namespace root {

// The exception hierarchy is documented in the following places:
//   python: https://docs.python.org/2/library/exceptions.html
//   javascript: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
class Error : public std::runtime_error {
  using std::runtime_error::runtime_error;
};

}  // root
}  // metax


#endif // metax_root_Error_h
