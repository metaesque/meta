#ifndef NM_SP_CLASS_H
#define NM_SP_CLASS_H

#include <iostream>

namespace nm {
namespace sp {

extern int Variable;
int Function(int a);

class Class {
  public:
    Class();
  private:
    int instance_;
    static int Static;
};

}  // namespace sp
}  // namespace nm

#endif  // NM_CLASS_H

