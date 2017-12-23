#ifndef metax_root_ObjectMetaRoot_h
#define metax_root_ObjectMetaRoot_h 1

#include <map>
#include <string>
#include <vector>

namespace metax {
namespace root {

// The root of the metaclass hierarchy in Meta. 
// 
// There are two ways we can handle the interaction between metaclasses
// in Meta and those in the baselang:
//   1) The meta-level metaclass is-a baselang-provided metaclass
//   2) The meta-level metaclass has-a baselang-provided metaclass
// See ../../README.md for details. Currently implementing variant #1.
class ObjectMetaRoot {

  // field metaname : @str
  //   The name of the class being represented by this metaclass.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields. But we do want to define metaname() to return
  //   the name as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.
  private: std::string _metaname;
  public: virtual const std::string& metaname() const { return this->_metaname; }
  public: virtual void metanameIs(const std::string& value) { this->_metaname = value; }
  public: virtual std::string& metanameRef() { return this->_metaname; }

  // field metabases : @vec<class>
  //   The parent classes of the class.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields.  But we do want to define metabases() to return
  //   the bases as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.
  private: std::vector<void**> _metabases;
  public: virtual const std::vector<void**>& metabases() const { return this->_metabases; }
  public: virtual void metabasesIs(std::vector<void**> value) { this->_metabases = value; }
  public: virtual std::vector<void**>& metabasesRef() { return this->_metabases; }

  // field metasymbols : @map
  //   The symbols available within the class.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields.  But we do want to define metasymbols() to return
  //   the symbols as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.
  private: std::map<std::string,void**> _metasymbols;
  public: virtual const std::map<std::string,void**>& metasymbols() const { return this->_metasymbols; }
  public: virtual void metasymbolsIs(std::map<std::string,void**> value) { this->_metasymbols = value; }
  public: virtual std::map<std::string,void**>& metasymbolsRef() { return this->_metasymbols; }
  // Every user-defined class has an auto-generated metaclass created for it,
  // and that metaclass inherits (eventually) from this class.  The meta
  // compiler implicitly inserts a params: block in meta class initializers
  // (if users define a meta-level lifecycle construct, they should not
  // specify params:, as that will be an error).
  // 
  // This signature is currently motivated by the signature of metaclasses in
  // Python. As additional baselangs are added to Meta, we may need to
  // generalize this implicit signature. Note that Javascript and C++ do not
  // have metaclasses, so we are not constrained by these baselangs). But when
  // we add in support for Java, we will need to establish whether
  // java.lang.Class can be subclassed (or whether metax.root.ObjectMeta will
  // need to act as a wrapper around a java.lang.Class instance) and how that
  // influences this signature.
  public: ObjectMetaRoot(const std::string& name, std::vector<void**>& bases, std::map<std::string,void**>& symbols);
};

}  // root
}  // metax


#endif // metax_root_ObjectMetaRoot_h
