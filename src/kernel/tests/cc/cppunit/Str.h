#ifndef Str_h
#define Str_h Str_h

#include <string.h>

namespace testit {

class StrTest;  // to support friendship

class Str {
 private:
  char* buffer; 
  int length;
  friend StrTest;  // Test classes have access to internals of real classes.
 public: 
  Str(char* s) { this->setbuffer(s); }
  void setbuffer(char* s) { buffer = s; length = strlen(s); } 
  char& operator[] (const int index) { return buffer[index]; }
  int size() { return length; }
}; 

}  // namespace testit

#endif  // Str_h
