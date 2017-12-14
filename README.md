# The Implementation of Meta

This document provides details about the implementation (and design)
of Meta, meant for those contributing to the implementation itself. For
individuals interested in using Meta, see the [[UserGuide]] instead.

## Overview

This implementation of Meta is written in Meta(Oopl)<Python>.

 - The compilation of the .meta source code is performed by an older 
   implementation of Meta written purely in Python.
    - The older python implementation is NOT stored in this repository
    
 - During the transition period from v1 to v2, we need to support both
   versions in a seamless way, so the following correspondences exist:
   
                    v1                           v2
        compiler:   $METAROOT/bin/metac          $METAROOT2/bin/meta2
        filterer:   $METAROOT/bin/metafilt       $METAROOT2/bin/metafilt2
        metastrap:  $METAROOT/lib/metameta.py    $METAROOT2/lib/metameta2.py
 

 - The following structure exists in this directory
    - Every directory has a README file that describes every subfile and subdir.
 
     bin/                         # Executables
       meta2                      # The meta compiler
       metafilt2                  # Service script for mapping line numbers
     lib/                         # Maintains all versions of Meta
       beta/                      # The live source code
       current/                   # The sanctioned source code
       stable/                    # The previous sanctioned source code
       versions/                  # All previous versions of Meta
         meta-0.000.tgz
         meta-0.001.tgz
         ...
     src/                         # All source code
       kernel/
         parser.meta
       schema/                    # The Meta-Language schemas
         meta/
           schema.meta
         oopl/
           schema.meta
       templates/
 
 - Meta avoids using environment variables where possible, instead preferring
   to store user-specific customizations in $HOME/.config/meta
   
 - When Meta compiles .meta source files into baselang source code, it
   by default writes the baselang source code into a repository shared by
   all Meta source code across all base languages and all meta languages.
   The structure of that repository is:
     repo/
       <metalang>
         <baselang>
           WORKSPACE
           BUILD
           BUILD.*
           bazel-*
           <namespace1>
           <namespace2>
           ...
           
   In particular:
    - Meta uses Google's Bazel build environment in all baselangs.
       - All thirdparty source code needed to implement Meta (and to
         implement user-provided code) is defined via the per-baselang
         WORKSPACE files and associated BUILD.* files
    - Every namespace defined in a .meta source file has an associated
      sub-directory path within repo/<metalang>/<baselang>. For example,
      the Meta class 'demo.cards2.Card' in the 'demo.cards2' namespace, when
      compiled into Python, would reside in
        repo/oopl/python/demo/cards2

 - All bugs/issues/feature-requests are stored in
   https://github.com/metaesque/meta/issues
   
 - Meta can auto-generate emacs major-modes for MetaLang syntax.
     % meta2 --metalang=<lang> emacs
   The major mode is written to $METAROOT2/src/schema/meta/meta<lang>-mode.el
   and defines meta<lang>-mode (metameta-mode, metaoopl-mode, etc.)

## Adding support for a new baselang

 - Update src/kernel/{root,test}.meta2 by adding baselang specific code
    - search for <py> and do the same thing in the new baselang as was done
      in python.

 - Update src/kernel/parser.meta with baselang-specific code:
    - Use the 'cards1-*' target in src/kernel/Makefile as a starting point:
       % make cards1-cc
    - Deal with whatever error arises next, until no errors arise.
       - define OoplFoo.metaMethodBody()
       - define OoplFoo.formatParams()
       - define OoplFoo.formatParentSpec()
       
    - Use the 'cards2-*' target in src/kernel/Makefile to continue the
      support for the new baselang, this time around providing an xUnit
      testing environment.
    - Deal with whatever error arises next, until the unittests all pass.
        
## Implementing interned string support

- The 'str' type is immutable and (partially?) interned
   - equality testing is faster (for those instances that are interned) than
     char-by-char comparison.
   - Python, Perl, Java, and Javascript all have interned strings and
     they are by far the most common ways to interact with strings in
     those languages. C++ does not have builtin support for interned
     strings, but if we want the languages to play nice together, we
     have to provide them in C++.

- #str is redundant
   - should it be disallowed?
   - no methods on this type provide the ability to modify state, so instances
     are inherently const.  '#' adds clutter, which we can avoid by making
     illegal.
     
- In languages without builtin support for interned strings (e.g. C++),
  a class would be defined (e.g. meta::root::IStr) to represent the interned
  string.
   - not every instance would be interned ... could use the heuristics that
     python uses (any string less than 21 chars is interned, anything that
     is a literal string, etc.)
   - Istr.interned() is bool true if interned and false if not, used in
     operator== (et.al) to establish whether we can do ptr equality or
     need to do value equality.

- *str  (variant #1)
  - Variant 1: a pointer to the interned string
     - details:
     - pros:
        - matches expectations
        - can be null
     - cons:
        - in C++, 'var name : *str' would become 'const IStr* name' and one
          would need to access methods with name->len() and (*name)[0].
           - solution #1:
              - details:
                 - define an operator '.' on const IStr* that returns const IStr&?
                 - define operator[] on const IStr* as well.
              - pros:
                 - provides convenient access to strings while allowing us to
                   distinguish between 'interned string that can be null' and
                   'interned string that cannot be null'.
              - cons:
                 - can we define the needed operators?
           - solution #2:
              - details:
                - *str is implemented as const IStr&
                - the IStr class would overload operator '->' to be the same as '.'
                  so that C++ users looking at the '*str' and assuming they need
                  to use '->' won't be confused.
                - the 'null' meta pseudovalue can be semantically overloaded. In most
                  situations it is the null ptr of the baselang (nullptr, None, null,
                  etc), but for 'str' types it can be IStr::Null, a special instance
                  of IStr).
              - pros:
                 - this allows us to support 'var name : str = null' as
                   'const IStr& name = IStr::Null'
              - cons:
                 - it does NOT allow us to distinguish between the types
                   'interned string that can be null' and
                   'interned string that cannot be null' in the same way that
                   it would if '*str' means IStr*

- &str  (variant #1)
   - Variant 1: interned string that cannot be null
      - pros
         - not null is consistent with '&' semantics of other types
      - cons
         - none?

   - Variant 2: interned string that can be null
      - pros
         - if 'str' means '&str' it would be useful for &str to be nullable
           (although 'null' may not mean nullptr ... could mean special
           instance of interned str class).
      - cons
         - violates the fundamental meaning of what '&' means in Meta.
           DEAL BREAKER.
           
   - Notes:
      - it is absolutely crucial to provide some mechanism for distinguishing
        between
          interned string type that can be null
        and
          interned string type that cannot be null
        because this distinction is important in Javascript when using the
        Google closure optimization javascript compiler.

- @str  (variant ??)
   - Variant #1: is illegal
      - pros
         - is intuitive ... @ implies copy semantics, and an immutable
           interned object cannot be copied. Even if we have @ mean
           'copy or move semantics', it is still problematic because
           we don't want to move these interned instances either.
      - cons
        - user has to remember that @str is illegal, unlike every other
          type (not a big issue).
        
   - Variant #2: value cannot be null
      - pros
         - synonym for &str?
      - cons
         - special-case semantics (does NOT mean copy-by-value, although
           @ does mean copy-by-value everywhere else).
        
   - Variant #3: value can be null
      - pros
         - ??
      - cons
         - special-case semantics (does NOT mean copy-by-value, although
           @ does mean copy-by-value everywhere else).
               
- str  (variant #1)
   - Variant 1: 'str' means '*str'
      - pros:
         - consistent with how all other non-primitive types are handled
           (e.g. vec is *vec, map is *map, Person is *Person, etc.)
         - Python, Perl and Javascript all use interned strings everywhere, and
           all string-typed variables can be null, so by having 'str' map to
           '*str', most variables can be typed as 'str' (note that Javascript
           with closure requires us to be able to distinguish betweeen 'str can
           be null' and 'str cannot be null'
      - cons:
         - In C++ syntax is cumbersome (but see '*str' discussion above for
           possible workaround).
           
   - Variant 2: 'str' means '&str'
      - pros:
         - Python, Perl and Javascript all use interned strings everywhere, and
           all string-typed variables can be null. If 'str' means '&str' and
           '&str' can be null, then the most common usecase can be represented
           by 'str' (a weak pro given the conditional).
      - cons:
         - violates the semantics of '&' within Meta, which very clearly
           indicates that '&' means "cannot be null".  DEAL BREAKER.
         - it is more common for str-valued variables to be of the form
           'interned string that can be null' than 'interned string that
           cannot be null'. By having 'str' mean '&str', we will be forced
           to explicitly type variables as '*str' most often. DEAL BREAKER?
         - Python, Perl and Javascript all use interned strings
           everywhere, and all string-typed variables can be null.  If
           str maps to &str, and &str cannot be null, almost every
           variable in these languages would need to be explicitly
           marked as \*str.  DEAL BREAKER ... this variant is nonviable.
           
   - Variant 3: 'str' means '@str'
      - pros:
         - none?
      - cons:
         - '@' means pass-by-value, which for read-only types like 'str' is
           somewhat counter-intuitive (more intuitive would be to disallow
           @str is legal).  But we could define '@' differently for read-only
           types, so this isn't a deal breaker.
         - Unless '@str' implies that the var cannot be null (not something
           I necessarily want it to imply, since there is a case for allowing
           null values for @str), 'str' meaning '@str' would mean there is no
           type to clearly state 'interned string that cannot be null'
           (we would need to introduce another type like !str to handle this).
           
   - Variant 4: 'str' means '&str' or '*str' depending on value assigned to var
      - details:
           .
         - When defining a parameter
             var name1 : str;
             var name2 : str = null;
             var name3 : str = '';
           we have:
             name1 is &str
             name2 is *str
             name3 is could be &str or *str ... let's say &str for now, and user
                can explicitly specify *str to allow null
           .
         - When defining a field:
             field name1 : str;
             field name2 : str = null;
             field name3 : str = '';
           we do not have as much info here as we do for parameters, as fields
           are often not given explicit defaults since there are type-specific
           defaults user can rely on. So it isn't so clear cut that name1
           should be &str vs *str, but we can assume &str and allow user to
           specify *str if needed.  name2 is clearly *str, and name3 can be
           assumed to be &str (user can specify *str if needed).
           .
         - When defining a local var:
             var name1 : str;
             var name2 : str = null;
             var name3 : str = '';
           similar reasoning as for fields (not for params!).
                      
      - pros:
         - the user rarely needs to explicitly specify *str or &str, using
           'str' everywhere, then adding *str or &str only when forced by
           type checking.
      - cons:
         - it is not as obvious what the actual type of 'str' is in this
           variant as it is in the other variants, which may lead to
           programmer confusion.

## Implementation of Classes in Meta<javascript>

 - The user-level class nm.sp.Foo is written to 
     $METAREP/oopl/javascript/nm/sp/Foo.js
   and Foo.js is implemented using goog.module('nm.sp.Foo'), and exports a
   single value (the defined class Foo), which allows any other namespace
   requiring nm.sp.Foo to obtain it with:
      const Foo = goog.require('nm.sp.Foo');
      
 - The metaclass for nm.sp.Foo is written to 
     $METAREP/oopl/javascript/nm/sp/FooMeta.js
   and FooMeta.js is implemented using goog.module('nm.sp.FooMeta'), but
   unlike Foo.js it exports two values (the defined metaclass FooMeta and
   the singleton instance of that metaclass, MetaFoo). This means that
   namespaces needing access to the metaclass must specify which symbol(s)
   they want, with:
     const {MetaFoo} = goog.require('nm.sp.FooMeta')
   or 
     const {FooMeta} = goog.require('nm.sp.FooMeta')
   or 
     const {MetaFoo,FooMeta} = goog.require('nm.sp.FooMeta')

 - The above inconsistency in how the modules are imported is unfortunate,
   but stems from the following facts:
    - nm.sp.Foo only has one thing to return (the class itself)
       - this may not be true if there is native code pre/post the class
         that should export symbols ... do we want to support that?
    - nm.sp.FooMeta defines the meta class, but one never actual needs
      the metaclass itself ... it is the singleton instance of the metaclass
      that is needed (we can obtain the metaclass itself from
      metainst.constructor).
       - Instead of having the metaclass module return both metainst and
         metaclass, we could just return the metainst ... that would be a
         bit more consistent, although the user would still need to remember
         that goog.require('nm.sp.Foo' returns a class, while
         goog.require('nm.sp.FooMeta') returns an instance of a metaclass.
    - it is possible that no module other than nm.sp.Foo will ever need
      to import nm.sp.FooMeta, since nm.sp.Foo.meta() provides access to
      the metainst (and thus the metaclass). Should we disallow the
      explicit importing of nm.sp.FooMeta ... that would hide the above
      inconsistency quite nicely.
      
 - Another subtle issue here. We do NOT want to return multiple symbols
   from goog.require('nm.sp.Foo'), because if multiple symbols are provided,
   the user must explicitly specify which symbols are desired.
    - This is a problem in situations where we want to define, for example,
      metax.root.Object, which inherits from javascript Object. We cannot
      use:
        class Object extends Object { ... }
        exports = Object;
      because the compiler doesn't know what we mean by the two different
      uses of Object.  So we need to instead do something like:
        class Object_ extends Object { ... }
        exports = Object_;
        
      This works fine if clients use the following:
        const Object = goog.require('metax.root.Object');
      but if the module for metax.root.Object returned multiple objects
      (for example: 'exports {Object\_, Symbol2, Symbol3};'), then
      the client would need to use:
        const {Object_} = goog.require('metax.root.Object');
      but only in the rare situation where the basename of the class matches
      a builtin javascript class from which the class inherits.  To hide
      away this rare but important special-casing, it is best if user-level
      class modules return the class and only the class.

## Class Hierarchy

Every user-defined user-level class in Meta has two auto-generated classes
associated with it, a meta class and a test class.
 - A user-defined user-level class A in namespace 'nm.sp' (nm.sp.A):
    - has meta class nm.sp.AMeta
       - has metaclass instance nm.sp.MetaA
    - has test class nm.sp_test.ATest

It is useful to understand how the user-defined class hierarchy generates
a metaclass hierarchy and a testclass hierarchy.

 - User Class Hierarchy

  baselang root object (or no parent if the baselang has no root object)
    metax.root.Object
      nm.sp1.A
        nm.sp2.BsubA
           nm.sp2.DsubB
        nm.sp3.CsubA
        
 - Meta Class Hierarchy

    baselang metaclass class (if exists and compatible with Meta metaclasses)
      metax.root.ObjectMeta
        nm.sp1.AMeta
          nm.sp2.BSubAMeta
            nm.sp2.DsubBMeta
          nm.sp3.CsubAMeta
          
   In particular, the metaclass hierarchy exactly mirrors the userclass
   hierarchy, differing only above the root (Object) level.

 - Test Class Hierarchy
 
    baselang testclass class (if appropriate, although we may forego these in favor of a pure-meta implementation)
      metax.test.TestCase
        metax.root_test.ObjectTest
          nm.sp1_test.ATest
            nm.sp2_test.BSubATest
              nm.sp2_test.DsubBTest
            nm.sp3_test.CsubATest
            
    The testclass hierarchy also mirrors the userclass hierarchy, but test
    classes are placed in a different namespace than the classes they test
    (classes in namespace 'nm.sp' have test classes in namespace 'nm.sp_test').

IMPORTANT QUESTIONS RELATED TO CLASS HIERARCHY:
 - should the meta-defined metaclass hierarchy inherit from baselang-specific
   metaclasses where present, or should the meta-defined metaclass
   hierarchy instead inherit from metax.root.Object and contain the
   baselang-specific metaclass when it is present?
    - inheriting from baselang metaclasses
    - not inheriting from baselang metaclasses
       - means that meta-defined metaclasses can inherit from metax.root.Object
         and thus benefit from a consistent interface
       - implies delegation of most functionality in situations where the
         baselang has an underlying metaclass
       - incurs additional (nominal) memory, since there will be a
         (presumably very small) metaclass instance associated with each
         user-defined class. Even if it isn't small, there are a small
         number of classes defined.
       - simplifies the code base, since we do not need to insert implicit
         parameters.

 - should test classes have meta classes?
    - pros
       - consistency ... why should test classes be punked?
       - needed if we want to allow 'meta' level methods and fields in test
         classes (and we are attempting, with Meta, to promote location=meta
         over the less powerful kind=static)
    - cons
       - additional complexity for something that is rarely used ... how
         many test classes need to define meta-level methods/fields?


 - should meta classes have test classes?
    - pros
       - uniformity.
    - cons
       - unnecessary complexity ... we can test any and all methods defined
         on the metaclass from within the user-level class wolog.

 - should it be possible for users to turn off the auto-generated
   metaclass and/or testclass associated with a user-level class?
    - For test classes
       - pros:
          - meta classes often don't need test classes (if all they do is
            initialize some state), or the methods can be defined on the
            user-level instance.
          - exception classes almost never need test classes
       - cons:
          - none?
    - For meta classes:
       - pros:
          - exception classes usually don't need a meta class.
          - test clases usually don't need a meta class.
          - if a user doesn't want the overhead of the metaclass, and
            has no need of any meta-level functionality, they should be
            able to disable it.
          - meta classes often don't need test classes
       - cons:
          - introduces an inconsistency in the interface available on
            classes
    - CONCLUSION: Allow disabling!
      - Add an 'autogen' feature attribute to the 'class' construct that
        allows one to disable test and/or meta class generation.

## Finding class/method/field definitions in meta files

 - By providing the ability to define many namespaces/classes/methods in
   a single file, we introduce a problem not present in other languages ...
   how to find the right definition of a class/method/field by id.
    
 - Variant #1:
    - search for 'class <id>' or 'method <id>' or 'field <id>'
       - pros:
       - cons:
          - takes a long time to type, and 'class <id>' is not very
            unique.
              - Searching for '^J class <id>' but is cumbersome to type.
              - Searching for 'd <id>' can be used to find field or method
                with given name.
          - because a method 'foo' might be defined via 'field' or 'behavior',
            it is not so easy to find.
            
 - Variant #2:
    - rely on IDE support
       - emacs and vim support for:
          - class:
             - identifying current class
             - going to start or end of current class
             - going to previous/next class
          - method:
             - identifying current method
             - going to start or end of current method
             - going to previous/next method
          - overview:
             - display all classes, lifecycles, methods, fields, behaviors
               (and allow narrowing based on typed id) and allow jump-to
               capabilities.
