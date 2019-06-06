# ifndef __METAX___HH
# define __METAX___HH __METAX___HH

// Included into every meta-generated .h file.  Be careful about what is
// added here.
#import <string>
//#import <string_view>

namespace metax {
  // CODETANGLE(cc_str_defn): How we define 'str' and 'strview' here needs to
  // be compatible with how we define CC_STR and CC_STRVIEW in metaoopl.meta.
  using str = std::string;
  using strview = std::string;
  //using strview = absl::string_view;

  // TODO(wmh): If we use absl::string_view, we shouldn't need a special
  // NullStr(), as we can use the special case of 'sv.data() == null' as the
  // null representation of a 'str'.
  extern const std::string& NullStr();
}

# endif  // __METAX___HH
