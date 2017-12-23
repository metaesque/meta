# ifndef Person_h
# define Person_h

# include <string>

namespace src {

class Person {
  std::string _name;
  float _weight;
  float _height;

 public:
  Person(const std::string& name, float weight, float height);
  float bmi() const;
  float height() const { return this->_height; }
  float weight() const { return this->_weight; }
};
    
}

# endif  // Person_h
