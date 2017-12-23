# ifndef Complex
# define Complex Complex

namespace testit {

class Complex { 
 private:
  friend bool operator==(const Complex& a, const Complex& b);
  double real, im;
 public:
  Complex(double r, double i = 0) : real(r), im(i) {}
};

}  // namespace testit

# endif // Complex
