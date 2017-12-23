#ifndef metax_root_Object_h
#define metax_root_Object_h 1

#include "metax/root/ObjectMeta.h"
#include "metax/root/ObjectMetaRoot.h"

namespace metax {
namespace root {

// Except in special circumstances, every class defined within Meta inherits
// from this class. Every base language provides a specialized implementation
// that defines functionality useful in implementing Meta-level semantics
// within that base language. Some of the methods defined here are present in
// all languages, some are only present in a subset of languages or in just one
// language.
// 
// This class does NOT introduce any instance-level state, but does define
// a significant amount of instance-level and meta-level functionality
// available to every subclass intance and subclass respectively.
// 
// Note that the metaparent of this class is always ObjectMetaRoot. Any
// class that inherits from Object will have a metaclass that inherits
// from ObjectMetaRoot.  Any user-defined meta class by default inherits
// from ObjectMetaRoot (semantics implemented in
// metax.c.ClassConstruct.metaClassInfo().
// 
// Meta:suppress: JSC_UNKNOWN_EXPR_TYPE
class Object {
  public: virtual metax::root::ObjectMetaRoot* meta();
};

}  // root
}  // metax


#endif // metax_root_Object_h
