# include <iostream>
# include <vector>
# include <any>
using namespace std;

// Used as a scratch-pad for emulating rvalues for methods not normally
// rvalued in C++.
//   - example: Meta defines vec.shift() and vec.extract(index) to remove
//     an element (from 0 and index respectively) **and return the removed
//     element).  C++ has vector::erase(), but that method does not return
//     the deleted element, it returns an iterator to a position within
//     the vector.  To have an rvalue that deletes and returns, we need
//     to use G_scratch as shown below.
thread_local std::any G_scratch;

int main() {
  vector<int> v = {1, 2, 3, 4};

  // Index 1 before removal
  cout << "before v[1] = " << v[1] << endl;

  // Remove index 1, assigning deleted element into 'n'.
  int n = (G_scratch = v[1], v.erase(v.begin()+1), std::any_cast<int>(G_scratch));
  cout << "after  v[1] = " << v[1] << endl;
  cout << "n = " << n << endl;
}
