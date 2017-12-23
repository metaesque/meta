/**
 * @fileoverview
 */
goog.module('metax.root.ObjectMetaRoot');
goog.module.declareLegacyNamespace();

/**
 * metax.root.ObjectMetaRoot
 *   The root of the metaclass hierarchy in Meta. 
 *   
 *   There are two ways we can handle the interaction between metaclasses
 *   in Meta and those in the baselang:
 *     1) The meta-level metaclass is-a baselang-provided metaclass
 *     2) The meta-level metaclass has-a baselang-provided metaclass
 *   See ../../README.md for details. Currently implementing variant #1.
 * @public
 */
class ObjectMetaRoot extends Object {

  // field metaname : @str
  //   The name of the class being represented by this metaclass.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields. But we do want to define metaname() to return
  //   the name as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.

  /**
   * metax.root.ObjectMetaRoot.metaname/get
   * @return {!string}
   * @public
   */
  metaname() {
    return this._metaname;
  };

  /**
   * metax.root.ObjectMetaRoot.metanameIs
   * @param {!string} value
   * @public
   */
  metanameIs(value) {
    this._metaname = value;
  };

  /**
   * metax.root.ObjectMetaRoot.metanameRef
   * @return {!string}
   * @public
   */
  metanameRef() {
    return this._metaname;
  };

  // field metabases : @vec<class>
  //   The parent classes of the class.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields.  But we do want to define metabases() to return
  //   the bases as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.

  /**
   * metax.root.ObjectMetaRoot.metabases/get
   * @return {!Array.<?Object>}
   * @public
   */
  metabases() {
    return this._metabases;
  };

  /**
   * metax.root.ObjectMetaRoot.metabasesIs
   * @param {!Array.<?Object>} value
   * @public
   */
  metabasesIs(value) {
    this._metabases = value;
  };

  /**
   * metax.root.ObjectMetaRoot.metabasesRef
   * @return {!Array.<?Object>}
   * @public
   */
  metabasesRef() {
    return this._metabases;
  };

  // field metasymbols : @map
  //   The symbols available within the class.
  //   TODO(wmh): This field is not needed in python ... need a way to
  //   have 'specific' fields.  But we do want to define metasymbols() to return
  //   the symbols as stored in the type metaclass.
  //   TODO(wmh): This should be a readonly field, so no setter or reffer.

  /**
   * metax.root.ObjectMetaRoot.metasymbols/get
   * @return {!Object.<!string,?*>}
   * @public
   */
  metasymbols() {
    return this._metasymbols;
  };

  /**
   * metax.root.ObjectMetaRoot.metasymbolsIs
   * @param {!Object.<!string,?*>} value
   * @public
   */
  metasymbolsIs(value) {
    this._metasymbols = value;
  };

  /**
   * metax.root.ObjectMetaRoot.metasymbolsRef
   * @return {!Object.<!string,?*>}
   * @public
   */
  metasymbolsRef() {
    return this._metasymbols;
  };

  /**
   * initializer
   *   Every user-defined class has an auto-generated metaclass created for it,
   *   and that metaclass inherits (eventually) from this class.  The meta
   *   compiler implicitly inserts a params: block in meta class initializers
   *   (if users define a meta-level lifecycle construct, they should not
   *   specify params:, as that will be an error).
   *   
   *   This signature is currently motivated by the signature of metaclasses in
   *   Python. As additional baselangs are added to Meta, we may need to
   *   generalize this implicit signature. Note that Javascript and C++ do not
   *   have metaclasses, so we are not constrained by these baselangs). But when
   *   we add in support for Java, we will need to establish whether
   *   java.lang.Class can be subclassed (or whether metax.root.ObjectMeta will
   *   need to act as a wrapper around a java.lang.Class instance) and how that
   *   influences this signature.
   * @param {!string} name
   *   The name of the class being created
   * @param {!Array.<?Object>} bases
   *   The parent classes of the class (instances of metaclasses)
   * @param {!Object.<!string,?*>} symbols
   *   The symbols available within the class.
   */
  constructor(name, bases, symbols) {
    super();
    /** @type {!string} */ this._metaname;
    /** @type {!Array.<?Object>} */ this._metabases;
    /** @type {!Object.<!string,?*>} */ this._metasymbols;
    // User-provided code follows.
    this.metanameIs(name);
    this.metabasesIs(bases);
    this.metasymbolsIs(symbols);
  };
}
exports = ObjectMetaRoot;
