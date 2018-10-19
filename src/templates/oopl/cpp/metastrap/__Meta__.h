# ifndef __META___HH
# define __META___HH __META___HH

// Included into every meta-generated .h file.  Be careful about what is
// added here.
#import <string>
//#import <string_view>

namespace meta {
  using str = std::string;
  //using strview = str::string_view;
  using strview = std::string;

  extern const std::string& NullStr();
}

# endif  // __META___HH
