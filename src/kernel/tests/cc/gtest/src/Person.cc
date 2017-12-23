# include "src/Person.h"

namespace src {

Person::Person(const std::string& name, float weight, float height) {
  this->_name = name;
  this->_weight = weight;
  this->_height = height;
}

float Person::bmi() const {
  float height = this->_height;
  return this->_weight / (height * height);
}

}
