#ifndef NM_CLASS_H
#define NM_CLASS_H

#include <iostream>

namespace nm {

extern int Variable;
int Function(int a);

class Class {
  public:
    Class();
  private:
    int instance_;
    static int Static;
};

}  // namespace nm

#endif  // NM_CLASS_H

