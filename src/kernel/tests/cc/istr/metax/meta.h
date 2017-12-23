#ifndef metax_meta_h
#define metax_meta_h

// Core funcitonality that every meta-defined class includes.
#include <string>
#include <map>

// Goals:
//  - same interface as 'const std::string&' or 'std::string_view'
//    (e.g. can be implicitly converted to those types and used
//    wherever they can be used).
//  - instance creation given a 'const char*' or 'const string&'
//  - conditional internment of inputs, storing canonical versions
//    to make comparison faster.

class IStr {

 public:
  operator std::string() const { return *this->str; }
  IStr(const std::string& str, int level=2) {
    // There are two independent things we need to establish
    //  - is 'str' already in the set of interned strings?
    //  - 

    // If level == 0, we do not intern
    // If level == 1, we intern if the string matches certain criteria.
    // If level == 2, we unconditionally intern
    if (intern > 0) {
    }
  }

 protected:
  IStr(const std::string* str, bool interned) : {
    this->_str = str;
    this->_interned = interned;
  }

 private:
  // str: string
  //   The underlying string instance.
  const std::string* _str;
  // interned: bool
  //   True if _str represents an interned string instance, false if it does
  //   not.
  //   TODO(wmh): store _interned in low bit of pointer?
  bool _interned;

  static std::map<
};


#endif // metax_meta_h
