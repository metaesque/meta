# HOWTO: How to do things

## Create a new Meta-language

METAROOT=$(metac config src_root)

1. Decide what the $name and $id of the metalang will be
 - name is usually capitalized and can contain arbitrary characters.
 - id is an identifier

2. Define a schema
 % cd $METAROOT/src/schema
 % mkdir $id
 % cd $id
 % cp ../oopl/schema.meta .
 % $EDITOR schema.meta
 - Update the MetaLanguage info, and define the constructs and attributes.
 - Define the BaseLanguage instances in the schema too
   - establish name, id and suffixes for each baselang.

3. Define the classes
 % cd $METAROOT/src/kernel
 % metac schema $id
 - The above generates meta$id.meta in local directory
   - contains classes for each Construct and BaseLanguage defined
     in the schema
   - you can add 'clsname' attributes to constructs if the default
     class names aren't what are desired.
   - add 'expand:', 'import:' (optional), 'translate:', and 'compile:' (optional)
     blocks to each construct in schema.meta and reinvoke 'metac schema $id'
     to see the effect.
   - the end result should be a hierarchy of classes under Construct:
      - ${Id}Construct < metax.c.Construct
        - ${construct}Construct, for each construct in the metalang
      - BaseLanguage$Id < metax.c.BaseLanguageConstruct
        - ${Id}${baselang}, for each baselang in the metalang     
        - example: for Meta(Doc) we have Id=Doc id=doc, and for baselang markdown
          we have baselang=Markdown baseid=markdown.  So we are creating subclass
          DocMarkdown of BaseLanguageDoc.
      - remember that the baselang classes are Construct subclasses, but are
        special in that there is a separate class for each baselang id
        (all other constructs have one class per construct, not per id).

4. Create an emacs major mode:
 % metac -L $id emacs
 - $EDITOR ~/.r/home/lib/emacs/wmh.el
   - in wmh-reload-meta, add a cond entry for the new metalang
   - in wmh-initialize-keymaps, define a key in mymeta-map under "r" for new metalang
   - in wmh-initialize, add
        (add-to-list 'auto-mode-alist '("\\.<some-suffix>$" . meta<id>2-mode))
   - M-x M-x (wmh-initialize-keymaps t)
   - C-@ r <key> (in a buffer containing a file written in the new metalang)

5. Create code to interact with the new schema
 % cd $WMH/lib/python/wmh
 % $EDITOR $id.meta
 - Define a 'Env' class that inherits from metax.c.MetaEnv
    - the lifecycle should pass metal and basel up to parent lifecycle
    - See $WMH/lib/python/wmh/bio.meta for an example structure.
 - Define a 'command' that provides access to functionality related to the
   metalang.

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
   
 - When Meta compiles .meta source files into baselang source code,
   by default it writes the baselang source code into a repository shared by
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

 - Update src/kernel/parser.meta with baselang-specific code:
 
    - Define OoplFoo by copying a pre-existing Oopl* class like OoplPython.
      - The class itself contains only an initializer and a test lifecycle, all
        other functionality is defined via behaviors.
      - For each behavior defined below the Oopl* classes, add a 'receiver' for 
        OoplFoo with appropriate code and unittests.
      - Use 
          % metac -r parser.meta metax.c.OoplFoo
        to iteratively add new code and test it.
 
 - Update src/kernel/{root,test}.meta2 by adding baselang specific code
    - search for <py> and do the same thing in <foo> as was done in python.
    - use 
        % meta2 -b foo root.meta2
        % meta2 -b foo --implicit_scopes test.meta2
      The --implicit_scopes flag is to stop the compiler from producing
      warnings like
        metax.test.TestCase.iseq is general but missing scope<foo>
      
 - Look at the generated baselang files to see if they look syntactically correct:
    - The repository directory can be found with:
        % repopath=$(meta2 config repository_path)
    - The directory containing code for baselang Foo class metax.root.Object is
      (usually)
        $repopath/oopl/foo/metax/root/Object.*

 - Within parser.meta, modify the test scope of BaseLanguageOopl.typeToBase(),
   extending the test method to support baselang foo.
    - it is critically import that meta-level types be properly converted
      to baselang variants.
      
 - Use the 'cards1-*' target in src/kernel/Makefile as a starting point:
    % make cards1-cc
 - Deal with whatever error arises next, until no errors arise.
    - define OoplFoo.metaMethodBody()
    - define OoplFoo.formatParams()
    - define OoplFoo.formatParentSpec()
    
 - Use the 'cards2-*' target in src/kernel/Makefile to continue the
   support for the new baselang
   - this target generates unit testing code, which will require additional
     code to be added to OoplFoo ... for example, OoplFoo.__init__ needs
     to specify values for setup[case] and teardown[case] in updateConfigs().
   - this target allows you to actually invoke the unit tests once OoplFoo
     is generating proper test code, which will allow you to formally test
     the cards2.meta source code in Foo.

 - Add support for parsing the bazel log files for Foo:
   - Test up some new data (only after unittests for cards2.meta2 are all
     passing!):
      % cd ./testdata
      ! Edit Makefile and add foo to BASELANGS
      % make refresh_repo
      # The above will tromp on testdata/repo, recreating subdirs for all
      # baselangs supported so far. This may (or may not) break unit tests.

## Defining a non-language schema and using it in Python code.

- First, create the schema file by going to $METAROOT/src/schema and creating
  a subdirectory named 'xyz' if you are defining Meta(Xyz).
  - Copy a schema.meta file from a sibling directory into 'xyz' and modify
    it to define all desired constructs.

- In python code:
  - Define a root construct:

      class XyzRootConstruct < metax.c.Construct #:
        Abstract superclass of all Meta(Xyz) constructs.
      scope:

        meta
        lifecycle scope:
          config, config_path = metax.root.Object.Config()
          meta_root = config['src_root']
          cls.MetaData = {
            /###############
            /# Meta(Xyz) #
            /###############
            'xyz': {
              'schema': os.path.join(
                meta_root, 'src', 'schema', 'xyz', 'schema.meta'),
              'name': 'Xyz',
              'parent': 'meta',
              'toplevel': ['fixme'],
              'constructs': {
                /# FIX THESE!
                'cons1': Cons1Construct,
                'cons2': Cons2Construct,
                'consn': ConsnConstruct,
              },
              'baselangs': {},
              'basesels': [],
            }
          }
        end lifecycle;

        ...
      end;

  - Define subclasses of XyzRootConstruct for each construct defined in
    the schema/xyz/schema.meta file

      class FamilyConstruct < XyzRootConstruct #:
        The 'person' construct.
      scope:

        ... add fields as appropriate ...

        method kind : str scope:
          return 'family'

        method expandMeta scope:
          /# This should parse the construct and initialize construct-specific
          /# fields
        end;

        method translateMeta scope:
          /# For non-language schemas, what happens in expandMeta() and what
          /# happens in translateMeta() is rather fuzzily defined ... up to you.
        end;

      end;

      class PersonConstruct < XyzRootConstruct #:
        The 'person' construct.
      scope:

        method kind : str scope:
          return 'person'

        ...
      end;

  - To setup a compiler for input written in Meta(Xyz):

      import metastrap
      sys.argv = ['faux', '-L', 'xyz', '-A', '0']
      Compiler, command, metacli = metastrap.ImportMeta()
      Compiler.Initialize(metadata=XyzRootConstruct.MetaData)
      metac = Compiler(metal=metacli.metalang, basel=None)

  - To parse a .meta file in Meta(Xyz) format:
      metafile, errors, warnings = metac.processMeta(path)
      if not metafile.hasErrors(show=True):
        scope = metafile.construct().attrval('scope:')
        top = scope[0]
        top.write()

## Implementing semantics of types without a prefix

- For primitive types, it makes sense that the implicit prefix should be '@'
  - Need to establish what '@' means in Meta:
     - could mean "pass-by-value", but then clones would need to be taken
       in baselangs other than C++ in situations they aren't necessary
       (pass-by-value in C++ is often a means of ensuring the object is
       cleaned up).
     - could mean "guaranteed not to be null and will be automatically gced".
     - consider how move semantics in C++ changes things
     - ... more contemplation needed...
- For class types:
   - We define "pass-by-reference" to mean "pass-by-pointer and guaranteed
     to not be null".
   - Most languages other than C++ do not have a distinction between
     pass-by-value, pass-by-reference and pass-by-pointer.
     - they are mostly pass-by-pointer but use '.' to access
   - We can have the default be '*' or '&' or '&#'
      - pros of '*'
        - matches intuitions of most people
      - cons of '*'
        - In C++, we have to use '->'. Especially problematic if 'str' means
          '*str'.
      - pros of '&'
        - In C++, we can use '.'.  This is especially useful if 'str' means
          '&str', as string manipulation is very common and it would be nice
          to be able to use '.' instead of '->' in the default situation.
        - It is arguably more common for class types to be non-null pointers
          that it is for them to be nullable pointers
        - Distinguishes Meta<C++> more clearly from C++ ... "improvement"?
      - cons of '&'
        - Some baselangs do not have a static typechecking mechanism for
          enforcing non-null pointers (so this check would either need to
          happen at runtime or not happen).
        - Without making it const, we would be allowing modification of
          the calling scope variable in some languages.
           - in many languages, pass-by-pointer has the same issues
             (in Java, one passes by pointer and cannot make the object const).
      - pros of '&#'
        - same as for '&'
        - increased type safety
      - cons of '&#'
        - constness not statically enforceable in many baselangs
        - non-nullness not statically enforceable in many baselangs
        
- For native types:
  - if all native types are class types in baselangs, it makes sense that 
    native types would use the same default as for class types, but I'm not
    sure all native types will be baselang class types.
     - more contemplation needed.

## Implementing the 'str' type

- Features of the 'str' type:
  - values are immutable
  - efficient comparison for at least literal strings
  - space efficiency
  - ability to store null
  - ability to indicate at the type level whether the 'str' can be null or not
  - ability to efficiently concatenate values of type 'str' with other strings
    (of type 'str' or other variants)
    
  - using the Meta type system, we have the following variants:
    - *str : can be null
    - &str : cannot be null  (unless we special-case it)
    - @str : storage space
    - str: same as &#str?

- In languages like Perl and Python, which have good support for text
  manipulation, strings are immutable and conditionally interned.
  
   - in python (http://guilload.com/python-string-interning)
      - '' and all length 1 strings are interned
      - from the above url, all literal strings matching regexp 
          ^[a-zA-Z0-9_]{1,20}$
        are interned, but my experiments show that
          'foo!' is 'foo!'
        returns True, and it appears that ALL literal strings
        are interned (even a string of 1025 'o's is interned)
        
   - the conditional internment allows for O(1) equality testing between strings
     if both are interned (falling back to the O(N) algorithm if either isn't
     interned). Because strings are often keys within dicts, efficient equality
     testing is beneficial.
     
   - a variable of type 'str' (Python), 'String' (Javascript), or scalar (Perl)
     can be null, and in some languages (Javascript) one can indicate a
     distinction between "string that can be null" and "string that cannot be
     null"

- In C++
   - there are a variety of types that can be used to represent a string:
     - char*
     - std::string
     - str::string_view  (points to pre-existing char* or string)
   - when needed to convert between types:
      - char* to string requires a copy: O(N)
      - char* to string_view does not require a copy: O(1)
      - string to char* uses s.c_str(): O(1)
      - string to string_view does not copy: O(1)
      - string_view to char* uses sv.data() but is NOT guaranteed to be NUL-terminated: (O(1))
      - string_view to NUL-terminated char*: O(N)
      - string_view to string: O(N)
      - creating string_view from char* needs strlen(): O(N) unless explicit length passed
      - creating string_vew from string shares state: O(1)
      
   - implementing 'str' using 'const char*'
      - no length, no convenient methods for various things.
      - not viable

   - implementing 'str' using 'const std::string' and std::string_view
      - when used in a field or local var:
         - @str --> std::string
         - &str --> const std::string&
         - *str --> const std::string*
      - when used as an arg or return of a method
         - @str --> std::string_view
         - &str --> std::string_view or const std::string_view&
         - *str --> const std::string_view*
      - notes:
         - string cannot separate "empty" from "null/invalid"
         - string_view can separate "empty" from "null/invalid"
           (.length()==0 vs .data()==nullptr vs )
           
   - implementing 'str' using 'const std::string'
      - variants:
        - *str --> const std::string* 
        - &str --> const std::string&
        - @str --> std::string
      - notes:
        - the most common type is '*str' ('str' means '*str'), which means one
          needs to use s->meth() instead of s.meth().  Having to remember whether
          to use -> or . depending on whether the type is '*str' or '&str' is
          cumbersome
        - no internment, so using 'str' as the key in a map incurs relatively
          expensive string comparisons.
       
   - implementing 'str' using a special IStr class
     - variants:
       - *str --> IStr*
       - &str --> IStr
       - @str --> std::string
     - notes:
       - The most common type is '*str' which means one uses s->meth() instead
         of s.meth(), and *s instead of s when wanting a 'const std::string&'.
          - Can we support the syntax 's.meth()'?  C++ does not allow '.' to
            be overridden (https://stackoverflow.com/questions/8777845/overloading-member-access-operators-c)
            but does allow dereference ('*') to be overridden ... will that help
            us?  I don't think so.
          - see proposal http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4173.pdf
            is this in c++17?
       
   - implementing 'str' using a special IStr class that stores nullable as state
     - variants:
       - *str --> IStr (with state indicating null allowed)
       - &str --> IStr (with state indicating null not allowed)
       - @str --> std::string
     - notes:
       - by having state in IStr store whether nullable, we lose static
         type-checking on that aspect!
         
    - implement 'str' using two classes, 'IStrPtr' (nullable) and 'IStrRef' (non-nullable)

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

   - Variant 3: &str is not legal
     - pros
       - implementation-wise, vec<&str> is not possible because a growable
         array must allocate more space than elements, with those elements
         somehow marked as "null", which isn't allowed for an actual reference
         (although &str does not necessarily need to be implemented by a
         reference).
     - cons
       - people are very use to 'const std::string&' (aka &#str = &str since str
         is implicitly const)
           
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
         - alternative for &str if &str is made illegal.     
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
         - In C++, we often pass strings by reference because they are rarely
           allowed to be null, and having to dreference string pointers is
           very cumbersome (but see '*str' discussion above for
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

## Accessors

Meta defines the 'field' construct, which serves many purposes:
 - defines state
 - defines various accessors on the state
 - defines dump, read, write
 - supports packing
 - supports UML generation

The standard accessors for a field:
  field foo : int;
are
   foo() : int
   fooIs(value:int)
   fooRef() : &int

The reasoning behind using 'Is' and 'Ref' suffixes for setter and mutable
setter
 - it is useful to be able to search for '.foo' and find all accesses
   to the field, which is not as easily accomplished if the accessors are
   named 'setFoo' and 'mutableFoo'.
 - case-consistency ... foo() and setFoo() are asymettric, foo() and fooIs()
   are symmetric
    - yes, using getFoo() and setFoo() would be symettric too, but getFoo()
      is too cumbersome.

Questions:
 - Should the setter return &Class instead of void?
    - pros:
      - Returning &Class allows one to cascade messages:
          obj.ageIs(32).weightIs(85).heightIs(187)
    - cons:
      - more code clutter
      - more inefficient ... the return value will often be unused, wasting
        an assignment
      - we can support message cascades using '..', which is a more
        general solution anyways:
          obj.ageIs(32)..weightIs(85)..heightIs(187)
    - conclusion:
       - Setters return 'void'

Notes:
 - getters are const and return consts
 - setters are not const and return nothing
 - reffers are not const and return non-const
    - in languages without the ability to return lvalues
      from methods, a different means of providing reffer
      semantics is needed
       - for languages with properties, the reffer is
         a property instead of a method (not optimal,
         but better than nothing).
 
 - the type of a field determines the type of args/return of
   accessors:
    - if field F has type @T
      - getter()
        - returns @T if T is primitive
        - returns &#T if T is class
      - setter(value)
        - value has type &#T and a copy is assigned to @T
      - reffer()
        - returns &T (so that T can be modified)

    - if field F has type @#T
      - getter()
        - returns @T if T is primitive
        - returns &#T if T is class
      - setter() not generated
      - reffer() not generated

    - if field F has type &T (non-null ptr)
       - getter() returns &#T
       - setter(value) has value of type &#T

       - notes
         - in C++, vec<&T> is not possible if it is implemented
           literally as a vec of references. We could still
           support this conceptually, with vec<*T> and implicit
           dereferencing.

 - the base type associated with a metatype varies depending on the
   context it is used in:
    - as a field
       - @T     T
       - @#T    const T
       - &T     T&           <-- requires initialization via init list of constructor (cannot reside in contanier)
       - &#T    const T&     <-- requires initialization via init list of constructor (cannot reside in contanier)
       - *T     T*
       - *#T    const T*
       - **T    T**
       - #*#T   const T*const         <-- cannot reside in contanier
       - *#*#T  const T*const*
       - #*#*#T const T*const*const   <-- cannot reside in contanier
    - as a positial parameter

    - as a keyword parameter
    - as a local variable without default
    - as a local variable with default


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
   
    - The metaclass hierarchy defined by Meta inherits from the metaclass(es)
      defined by baselangs.
       - pros:
          - we aren't maintaining two separate hierarchies in languages
            that provide 
          - the features added by Meta integrate seamlessly into the
            features provided by the baselang, instead of the two sets
            of features being forced to be independent
       - cons:
          - Metaclasses are a required feature, introducing additional
            classes and complexity without any ability to remove them if
            they are unused.
       - notes about ObjectMetaRoot:
          - This class is for the metaclass hierarchy what Object is for the
            class hierarchy. All metaclasses in Meta inherit (directly or indirectly)
            from this class unless the user specifies a metaparent outside the
            meta metaclass inheritance hierarchy (which limits what Meta can do).
          - This class acts as a bridge between the Meta world and the non-Meta
            world, inheriting from whatever baselang-specific class is used
            for metaclasses. If such a class does not exist, this class
            inherits from the root class in the baselang. If such a class
            does not exist, this class inherits from nothing. We 
            intentionally do NOT have this class inherit from
            metax.root.Object in such cases because that would mean that
            metax.root.Object functionality would be available in some
            baselang metaclasses but not in others.

    - Meta introduces a metaclass hierarchy that is independent of the
      metaclass hierarchy of the baselang, and instances of the Meta-defined
      metaclass hierarchy contain instances of the baselang metaclass
      instances (for baselangs that have a metaclass concept).
       - pros:
          - all metaclasses across all baselangs can inherit from
            metax.root.Object and benefit from a consistent interface,
            instead of different functionality existing in different
            baselangs.
          - the metaclasses introduced by Meta can be completely decoupled
            from the user-classes ... they can be used if needed, but
            do not have any impact on the code if not used. Note however
            that they are implicitly being used (and thus required) if
            the user defines any 'meta'-level classic constructs.
       - cons:
          - results in an extra hierarchy
          - implies delegation of most functionality in situations where the
            baselang has an underlying metaclass
          - *** In Python, we would not be able to set __metaclass__ to
            the Meta-defined metaclass, and would have to implement all
            meta-level functionality using @classmethod, etc.
             - this would be definining an 'Initialize' method and ensuring
               it always gets invoked when classes are loaded, etc. ...
               not nearly as clean a solution as having the metaclass
               initializer perform such initialization.

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

## Exception classes.

  There is an important issue that needs to be resolved related to exceptions.
  We want to be able to offer two mutually exclusive features:
   1. In order for baselang code to use meta-generated classes and catch
      exceptions without using Meta exception classes, each of these classes
      should inherit from baselang coorelates where possible.
   2. In order to catch ranges of exceptions, it is useful to define an
      inheritance hierarchy of exceptions (if exception classes B and C inherit
      from A, then either exception can be caught be looking for exception A).

  Python: https://airbrake.io/blog/python-exception-handling/class-hierarchy
  - BaseException
    - Exception
      - ArithmeticError
        - FloatingPointError
      - AssertionError
      - ImportError
        - ModuleNotFoundError
      - LookupError
        - IndexError
        - KeyError
      ...

  C++: http://stdcxx.apache.org/doc/stdlibug/18-2.html modiifed in http://en.cppreference.com/w/cpp/error/exception
  - exception
    - logic_error
      - domain_error
      - invalid_argument
      - length_error
      - out_of_range
    - runtime_error
      - range_error
      - overflow_error 
      - underflow_error     - 
    ...

  Suppose Meta also wants to define a hierarchy of exceptions
  - metax.root.Error
    - metax.error.Error
      - metax.error.LogicError
        ...
      - metax.error.RuntimeError
        ...

  The classes in the Meta exception hierarchy need to inherit from other classes
  from the Meta exception hierarchy ... but they should also inherit from
  baselang equivalent classes.
   a. In baselangs with support for full multiple inheritance, this is viable
   b. In baselangs with support for single class inheritance and multiple
     interface inheritance, this is viable as long as the Meta exception class
     hierarchy is instead a Meta interface hierarchy.
   c. In baselangs without support for any form of multiple inheritance, this
     is only supportable in Meta by having all exception classes be native
     types.

  Given that Meta does not, as of 2017/12/31, have full support for multiple
  inheritance or interfaces, the easiest (and most general) solution is (c), so
  that is what we'll go with for now.
   - must maintain a mapping from conceptual exception class to
     baselang equivalent
   - must provide some special baselang syntax to allow baselang scope: blocks
     to refer to the conceptual meta-level exception class name and have it
     replaced with the appropiate baselang exception class.
      - there is a more general need for such an escape mechanism within baselang
        scope: blocks
      - possible syntaxes:
         - $#{...}  --> I don't think this is legal in perl, is it?
         - #${...}  --> this may conflict with perl syntax
         - $!{...}
         - !${...}  --> conflicts with Perl
         - $!{...}  <-- this one is promising (slight problem related to ! field access, but acceptable)
         
         
## Variable interpolation within literal strings

Suppose we want to form a string providing a person's name, dob, height and weight.

  python:
    print 'Person %s born %s height %1.2fm weight %1.2fkg' % (
      p.name(), p.dob(), p.height(), p.weight())
      
  javascript:
    console.log(
        'Person ' + p.name() + ' born ' + p.dob() +
        ' height ' + p.height().toFixed(2) + 'm' +
        ' weight ' + p.weight().toFixed(2) + 'kg');
       
  C++
    cout << "Person " << p.name()
         << " born " << p.dob()
         << " height " << ios:setprecision(2) << p.height() << "m"
         << " weight " << ios:setprecision(2) << p.weight() << "h"
         << endl;


Meta provides a mechanism for identifying literal strings in baselang source code
that contain special variable interpolation requests, and generating the appropriate
baselang source code.
 - the code generated will not be valid RHS in all baselangs, so this is
   limited to situations where an arbitrary block of code can be inserted.
    - NOTE: not strictly true, in that Meta could define a method, but passing in all
      necessary local vars becomes complicated ... maybe later.
      
 - rather than introducing escape syntax within baselang code to indicate
   creation of a string object based on this special syntax, we can do the more
   general thing ... use meta-level statements. Added bonus: provide a mechanism
   to embed meta-level statements inside a baselang simple block!
   
    method show
    scope<*>:
      var msg : str = 
        "Person ${.name} born ${.dob} "
        "height ${.height:1.2f}m weight ${.weight:1.2f}kg\n";
      block
      :py:
        print msg
      :js:
        console.log(msg)
      :cc:
        cout << msg << endl;
    end method;
    
Meta can provide lots of convenience syntax within these variables:
 - ${.name} means @self.name
 - ${!name} means @self!name
 - ${rec.name} means @rec.name
 - ${rec!name} means @rec!name
 - ${name} means local variable 'name'
 - ${@name} means "name " + local variable 'name'
 - ${@.name} means "name " + @self.name


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

## The Importance Of Antlr

Although Meta can do a great deal without having baselang parsers,
being able to produce an AST of a baselang program (across all
baselangs) would provide the following benefits:
 - can introduce { ... } block syntax in addition to indent-based blocks
 - can automate baselang-to-meta conversations
 - can properly identify whether fields are initialized in initializers
 - can establish whether a method returns before end

Note that for javascript, we don't need Antlr because we have
https://github.com/google/closure-compiler/wiki/Writing-Compiler-Pass

## C++ and Bazel

C++17 offers many features that will be very useful in Meta<C++>, so we need
Meta to be C++17-enabled from the get-go. However:
 - on macos as of 2017/12/16, the default c++ compile is clang
      % c++ --version
      |c++ --version
      |Apple LLVM version 9.0.0 (clang-900.0.38)
      |Target: x86_64-apple-darwin16.7.0
      |Thread model: posix
      |InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
      
 - apple clang 9.0.0 is mapped to LLVM 4.? 
     - LLVM releases at http://releases.llvm.org/ 
     - C++ status for LLVM at https://clang.llvm.org/cxx_status.html
     - apple version numbers to LLVM version numbers: https://en.wikipedia.org/wiki/Xcode#cite_note-LLVM_versions-80
        - nothing specified for most recent apple clang, but presumably LLVM 4*
     - one can supposedly use -std=c++1z (according to https://clang.llvm.org/cxx_status.html
       in the 'C++17 implementation status' section), but that doesn't work:
         % cd meta2/src/kernel/tests/cc/c++17
         % make 
         % /usr/bin/clang++ -std=c++1z main.cc
         |main.cc:2:10: fatal error: 'any' file not found
         |#include <any>
         |         ^~~~~
         |1 error generated.
         % which clang++
         |clang++ is /usr/bin/clang++
         % cd /usr/include
         % find . -name '*any*'
         |./apr-1/apr_anylock.h
         
 - g++ does handle C++17 properly:
     % cd meta2/src/kernel/tests/cc/c++17
     % /usr/local/wmh/gcc-7.2/bin/g++ -std=c++17 main.cc
     % ./main
     |Hello World
     |val1 = 1
     
 - bazel's default CROSSTOOL uses clang:
     % cd meta2/src/kernel/tests/cc/c++17
     % make bazel-clobber
     % blaze build --cxxopt=-std=c++1z --verbose_failures :main
     |...
     |main.cc:2:10: fatal error: 'any' file not found
     |#include <any>
     |         ^~~~~
     
     % grep cxx $(find $(bazel info execution_root) -name CROSSTOOL)
     |...
     |cxx_builtin_include_directory: "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/9.0.0/include"
     |...

 - it is possible to have bazel use a different compiler
   - a discussion of cc_configure
      - https://blog.bazel.build/2016/03/31/autoconfiguration.html
   - indicates that one can set envvar CC and rerun:
       % cd meta2/src/kernel/tests/cc/c++17
       % bazel clean --expunge
       % make bazel-clobber
       % export CC=/usr/local/wmh/gcc-7.2/bin/g++
       % blaze build --cxxopt=-std=c++17 --verbose_failures :main
       |...
       |g++: error: unrecognized command line option '-Wthread-safety'; did you mean '-fthread-jumps'?
       |g++: error: unrecognized command line option '-Wself-assign'; did you mean '-Wcast-align'?
       |...

    - Looks like the crosstool generation code defined in cc_configure is accidentally
      inserting some compiler_flag options that aren't legal for gcc.
        - comment out 
             compiler_flag: "-Wthread-safety"
             compiler_flag: "-Wself-assign"
          in
            % emacsclient $(find $(bazel info execution_root) -name CROSSTOOL)
 
    - Retrying the build:
        % blaze build --cxxopt=-std=c++17 --verbose_failures :main
        |...
        |collect2: fatal error: cannot find 'ld'
        |...
 
  https://stackoverflow.com/questions/41356173/how-to-use-clang-instead-g-in-bazel


## Supporting native methods

Many languages provide a mechanism for interacting with code written in other
languages
 - perlxs (https://perldoc.perl.org/perlxs.html) links to C code
 - python (https://docs.python.org/2.0/ext/intro.html) links to C code
 - java JNI (https://en.wikipedia.org/wiki/Java_Native_Interface) links to C, C++, assembler

As well, there are means of perform whole-program conversion to other languages:
 - emscripten (https://en.wikipedia.org/wiki/Emscripten) compiles C++ and
   outputs asm.js, a subset of Javascript !!!
 - mono/.NET
 
Meta can make these cross-language capabilities much easier:

  Suppose we have a program written in python. A specific method could instead
  be written in C++ (with Meta automatically providing all of the glue needed
  to interface between the languages).

    class Matrix scope:
    
      method times : Matrix #:
        Implemented in C++ for efficiency.
      params:
        var matrix : Matrix;
      scope<py>:
        native lang c++ scope:
          ... add C++ code here ...
        end;
      end method times;
        
  Note that my original idea that an entire method could be marked
  'native' does not work because we need to specify both the target baselang
  and the native baselang, which would only be possible if we put the 
  target baselang on the 'scope:' of 'class' (that is too limiting).
   - Will need to expand this idea further.

## Supporting I/O (etc.) in Javascript

We need to provide I/O capabilities in Javascript.  Since phantomjs already
has such support (and would also be the sensible choice to provide the
javascript version of 'meta2 repl') we can use phantomjs.

TODO(wmh): Establish how to properly specify the needed dependencies if a
certain javascript class uses phantomjs libraries like 'require(webpage)', etc.

Note that 
  https://github.com/bazelbuild/rules_closure/blob/master/closure/testing/phantomjs_harness.js
(and the other files in its directory) may be helpful here.  For example,
note how one types phantomjs objects:
  var webpage = /** @type {!phantomjs.WebPage} */ (require('webpage'));
  var fs = /** @type {!phantomjs.FileSystem} */ (require('fs'));
  var webserver = /** @type {!phantomjs.WebServer} */ (require('webserver'));
  var system = /** @type {!phantomjs.System} */ (require('system'));

And from
  https://github.com/bazelbuild/rules_closure/blob/master/closure/testing/BUILD
the BUILD target:
  closure_js_library(
      name = "phantomjs_harness",
      srcs = ["phantomjs_harness.js"],
      no_closure_library = True,
      deps = ["//closure/testing/externs:phantomjs"],
  )
I suspect the dep will need to be modified to use @ syntax, but it should be
a helpful starting point ... we may be able to use


## Languages to Support

Java
Perl
Go
Eiffel
Ada
C#
ObjC
Ruby
Emacs (EIEIO): https://www.gnu.org/software/emacs/manual/html_mono/eieio.html

## History
 - Pxx and Cxx
 - X3
 - Meta (uwo, in perl)
 - Meta (uwo, in Meta<perl>)
 - Meta (sf, in python)
 - Meta2 (in Meta<python>)
 
## Units of Measurement

 - Research
   - https://dl.acm.org/citation.cfm?id=1035292.1029008

 - For C++
   - https://github.com/nholthaus/units (https://sourceforge.net/projects/tuoml/)

 - For python
   - https://pypi.python.org/pypi/units/
   - https://pypi.python.org/pypi/measurement/1.8.0
   - https://pypi.python.org/pypi/quantities/
   - http://home.scarlet.be/be052320/Unum.html
   - http://dirac.cnrs-orleans.fr/ScientificPython/ScientificPythonManual/Scientific.Physics.PhysicalQuantities-module.html
   - https://pint.readthedocs.io/en/latest/

 - For .NET?
   - https://www.codeproject.com/Articles/216191/Quantities-Units-and-Values-an-Object-Oriented-Imp

## Languages To Add To Meta

- Python            py
- Javascript        js
- C++               cc
- Java              java
- Ruby              rb
- C#                cs
- Objective-C       mm
- Delphi            pas
- Swift             swift
- Perl              pm
- Go                go
- Dart              dart
- Ada               ada
- R?                r
- Eiffel
- EIEIO
- Smalltalk/Squeak  st
- Tcl               tcl

## Pain Points

- finding specific code in a large file is problematic
  - having code defined in various possible places makes searching for it difficult
    - is it a field or a method?
    - is it defined in the class or in a behavior?


## Important To Remember

- Metaclass initializers get invoked N+1 times if there are N descendent
  classes of the underclass. In hindsight, this is obvious, but I had been
  assuming that code written into metaclass __init__ blocks was executed
  exactly once. Important to keep this in mind.
   - puts more importance on providing 'static' fields separate from 'meta'
     fields, for situations where we want to ensure code occurs exactly
     once.

## Bugs

- The 'default' attribute of 'var' is of type 'word' instead of 'expr'.
  This means we cannot use:
    var  delim : str = '  ';
  and is totally limiting in many other ways. Fix!!

- Cannot define a 'native' construct before the first 'class' in a namespace
  scope: because the code is looking for a class to attach the native code
  to.  Need to support this usecase ... it will be common to add a native
  block before any classes.
  
- NamespaceConstruct._mergeClassesPython() has to deal with the fact that
  we sometimes want to refer to class nm.sp.Class2 from within nm.sp.Class1
  as nm.sp.Class2, when python prefers we use Class2 when they share a
  namespace (because python does not add 'sp' to 'nm' until 'nm.sp' is fully
  parsed).  The code currently inserts some magic at the top of each
  module to define nm.sp within nm.sp, but it is entirely possible that this
  code will break something in python's control flow.
  
- The Emacs major-mode has various weaknesses:
  - Within Meta comment blocks, inserting the character \" immediately kills
    all syntax highligting
    
  - When in a comment block, if the current line has a '(' without matching
    ')' and newline-tab is entered, the cursor is moved below the unmatch
    ')' rather than being moved to the start of block position.

  - When searching up for start of construct, it can be mislead by matching
    regexps in comments.
    - could be improved by having Meta know how many spaces appear before
      each construct (usually 0 for namespace, 2 for class, 4 for method),
      but this will obviously break for nested classes, etc.

- The fundamentally important Construct.attrpair() method has a problem:
     locattr, location = self.attrpair('location', default=LOOKUP)
  Suppose that the construct in question does not explicitly specify a
  'location'. That means it does not have a location in the metafile, which
  means locattr.line() will not be meaningful ... but often the whole point
  of keeping locattr around is to get the meta linenum!
  
   - In such situations, attrpair() should return (None, <value>) instead of
     returning the misleading special Attribute instance.
  
   - To identify places where this is causing problems, we could initialize
     the 'line' field of the special Attribute instances cached in attrinfo
     to some sentinal like -123, and whenever Attribute.line() is invoked, if
     the value is -123, we raise an error.

- Suppose we have a class with user and meta methods and a user-defined
  TestCase class in 'test' location.  The meta method test blocks cannot
  benefit from the initialization done in the TestCase, because they
  are defined separately.
   - consider merging tests into a single class, or otherwise fixing this
     (copying TestCase code to TestCaseMeta?)

## Critical Missing Features

- Meta needs someone to write code for vim that does syntax highlighting, etc.

- Should Meta support python-like continuations in all baselangs?
   - https://www.ps.uni-saarland.de/~duchier/python/continuations.html

- Support for multiple inheritance (state and/or interface).
  - Meta can do a lot here, but there is almost zero support for
    multiple inheritance as of 2018-01-01, even at the level of
    individual baselangs (never mind making it work for Meta<X1|X2>).

- Support for interfaces

## TODO

- In type specifications, support named params:

    For example:
      tuple<dirname:str,basename:str>
    vs
      tuple<str,str>

    And
      map<{name:str,height:float,cards:int,present:bool}>
    vs
      map<str,any>
      
- For every native type, introduce a class in the Meta library that
  provides a baselang-independent implementation and describes the
  public interface available.  Introduce some secondary simplex attribute
  on 'executable' to allow specification of native code:
  
    class Vector<T> < Container<T> #:
      A collection of contiguous element indexed by integer
       - get(index) = O(1)
       - set(index) = O(1)
       - sort() = O(N)
    nativetype<py> list
    nativetype<cc> std::vector<$T>
    nativetype<js> Array
    scope:
    
      field allocated : int #:
        How many elements are allocated.
      field size : int #:
        How many elements are assigned.
       
      lifecycle params:
        var size : int = 0 #:
          Initialize size of list.
      scope:
      end;
      
      method size : int aliases "len,length" #:
        Number of elements in vector.
      scope<*>:
        return @self.size;
      native<py> 'len($rec)'
      native<cc> '$rec->size()'
      native<js> 'this.length'
      end method;
    end class;
    
    NOTES:
     - there should be both 'native' and 'native:' defined on methods
        - native accepts a string, and represents baselang code that can be
          used to implement the method as a statement
        - native: defines a block of baselang code and implies that the
          method cannot be implemented in the given baselang as a statement
          (requires multiple lines).  The result can still be used as a RHS,
          as long as it is possible to insert lines of code into the
          baselang code stream before the line requiring the RHS.

- Support aliases for method and field names
  - will at the very least be useful for 


- The 'default' attribute of 'var', 'field' and 'flag' should have type 'expr'
  not 'word'
   - will allow us to support
        var item : nm.sp.Class = @nm.sp.Class2.Func;
     or
        var item : map = {'a': 1, 'b': 2};
        
- In describing Meta, emphasize the utility in being able to add good ideas
  from arbitrary languages into all baselangs
   - 'new' vs 'override' semantics on methods is crucial ... not all baselangs
     support it.  Meta can ensure this semantics exists everywhere.
   - python-like repl
   - java-like per-class entry points
   - ability to distinguish "nullable ptr" vs "non-nullable ref" vs "value"
   - easy-to-use multi-match regexp
   - variable interpolation in strings
   - units of measurement
   - unified test environment
   - formalized resources and associations
   - automated uml generation
   - source code configuration and canonicalization
     - index generation
   - trivial aspect-oriented capabilities
   - cross-language native embedding
   - cross-language typechecking
   - 'auto' type

- NamespaceConstruct.expandMeta() needs updating so that each namespace has an
  'id' with no dots in it. The code in
     NamespaceConstruct.createImplicitParents()
  was designed for use in the namespace initializer, but similar code can be
  crafter for expandMeta. 
   - start with the test namespace, which is being created within expandMeta
     (instead of creating a namespace with multi-dots, create individual
     namespaces). 
   - once the test namespace is working properly, move on to updating the
     user namespace, which is a bit more subtle because it already exists.
        
- Statement level support!!
  - recursive loading of dependency classes
  - proper initialization of symbol tables
     
- Decide how to handle exceptions
  - See discussion above entitled 'Exception classes'.
  - Looks like providing a mapping from conceptual exception naems to
    baselang equivalents is the way to go for now.
    - This could be a real problem moving forward...

Define metax.error, a namespace consisting solely of exception classes.
   - each exception class should inherit from appropriate baselang 
     classes where possible.
   - each should be clearly documented with when it should be raised
   - all code in the Meta implementation should use these classes.

- Support aliases on primary attributes (e.g. 'arg' for 'flag')

- In addition to the >| syntax, which does:
     namespace nm.sp scope:
       class A scope:
          method f scope:
            text = """
             >|some text
             >|more text"""
  we should also support
     namespace nm.sp scope:
       class A scope:
          method f scope:
            text = """
     !meta_inline:
     some text
     more text"""
     !end meta_inline:
  which inserts the text to the same level as the line before !meta_inline:
  This is not optimal, and will require special support from the simple-block
  parsing code, but having to indent text via >| is sometimes cumbersome.
  Is there a better solution?  emacs and vim support for >|?

- Implement C++ to the point where 'make cards2-cc' works.
  - need to get C++ unit testing working
  - may need to improve the type system.

- uml generation
   - this should use the HTML syntax so that we can draw association lines
     from field to field rather than just class to class.

- implement behavior stubs?
  - Problem: if one looks for a method in a class but it is defined
    in a behavior instead, it can be confusing.
  - Solution: support "behavior stubs" ... method declarations
    in classes with a featval 'stub' to indicate they are replaced
    by a behavior.

      class Foo scope:
        stub method methname;
      end class;

- Provide a 'Meta' symbol in every namespace, to give access to:
  - all reflection capabilities
  - a parsed dict of the ~/.config/metameta file
  - ... there are more benefits here ... list them...

## Ideas

- Add a 'preamble:' block to 'behavior' constructs that is inserted at the
  start of each receiver scope block before user code after auto-gened
  preamble code.  Useful for initializing params with same logic.
   - less useful if per-baselang blocks are needed .. more useful if
     logic can be written in Meta*

- The 'lazy' block on accessors in fields should be moved up to being
  a block on 'field' itself, not on accessors
   - it doesn't make sense for 'set'
   - the same code applies to both 'get' and 'ref' (confirm this before moving)

- Add a 'super' feature attribute to the 'var' construct for use in params:
  blocks ... implicitly added to the super() attribute:
    method f params:
      super var a : int;
    scope:
    end;
  is equivalent to
    method f params:
      var a : int;
    super (a)
    scope:
    end;
    
  For bonus points, can skip type and comment because meta can look it up
  from the parent method:
    method f params:
      super var a;
    scope:
    end;
  is equivalent to
    method f params:
      var a : int;
    super (a)
    scope:
    end;
  because Meta can find the parent definition to determine that param
  'a' has type int (and can insert parent comment block, etc.) 

  NOTE: may need to make 'super' a secondary attribute, not feature attribute,
  in order to specify position within super() call.

- Provide a syntax on 'var' within 'params:' to indicate that the
  default value should be "whatever the default of the parent invocation is"
  for use in super calls.
   - in python, this can be implemented by not passing the keyword parameter
     at all in the super call.
   - example:
        method f params:
          super var a : int;
          super var b : int = 3;
          super var c : int = super;
     this would be equivalent to
        super (a, b=3)
     (the c arg is marked as 'use default from super' so we don't
      pass it to the super call).

- Support literal syntax for bases other than 10.
     723@8
     010001100010100@2
     ab8373a@16
     1234@10
   or (not as flexible, cannot handle @7, @23, etc.)
     0o723
     0b010001100010100
     0xab8373a
     123
   
   Note: Meta does NOT support 0235 as being base 8! (too ambiguous)
   
   Note: How will this interact with literal units? 
     83kg in base 8?
     
   Note that suffixes like Ki, Mi, Gi, Ti, and Pi implicitly
   encode a base-2 interpretation, but somewhat special in nature.
    - Ki = 2^10
    - Mi = 2^20
    - Gi = 2^30
    - Ti = 2^40
    - Pi = 2^50

## Stack

 - ability to see ConsInfo data for specific construct
   --> meta shell
     --> native type for 'date', 'time', etc
       - units of measurement
     --> getting 'run' command working
       --> creating a 'hierarchy' summary of a meta file using org-mode
         --> supporting 'aliases' attribute on 'command' construct
           --> getting 'str' attribute type working
             --> auto-filtering exceptions raised when meta2 invoked 
               - blocked because exception was occuring during creation of Compiler
                 and since filterMetaOutput is an instance method I have a catch-22
             - solution to 'str' issue was 
                 Attribute path : str = <empty> #:
               vs
                 Attribute path : str = empty #:
           --> timing how long it takes to parse/expand/translate/compile each metafile
             --> adding file/line counts to writeSummary
           --> tracking down the bug in metax.root.flags.Command.instantiate()
                - was a use of 'current_arg_index' instead of 'index' when forming
                  argv to consume with multi-valued catch flags!
           - finally got aliases working!
         --> provide a total in writeSummary when more than two files were parsed.
