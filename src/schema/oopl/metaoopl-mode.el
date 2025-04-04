;;; This is a template for defining any Meta(Lang) major mode.
;;;   Refer to
;;;      http://two-wugs.net/emacs/mode-tutorial.html
;;;   for an excellent tutorial on major-mode creation.
;;;   This code is a simple translation of that website content
;;;   to handle Meta.
;;;
;;; There are only two things that need to be done to instantiate this
;;; template as a real major-mode file:
;;;   1) Replace
;;;        <CONSTRUCTS-HERE>     with the list of construct names (each name delimited by "")
;;;        <ATTRIBUTE-KEYS-HERE> with the list of non-primary attribute keys (each key delimited by "")
;;;        <FEATURE-VALUES-HERE> with the list of feature values (each value delimited by "")
;;;   2) Replace 'metalang' with the appropriate language-specific name
;;;      (for example, 'metaoopl' for Meta(Oopl), 'metadoc' for Meta(Doc),
;;;      metainstall for 'Meta(Install)', etc.
;;;
;;; IMPORTANT:
;;;   If the line after this paragraph does NOT contain the words
;;;   'MetaLang' and 'metalang', then you are currently looking at an
;;;   instantiation of the template, not the template itself!
 ;;
 ;;      This is the file for Meta(Oopl) with suffix .metaoopl
 ;;
;;; Due to the structure of Meta, a basic major-mode is very easy to create,
;;; having few rules:
;;;
;;;   1) Each line is indented a certain number of spaces further than the
;;;      closest previous line that ends with ':' (may also support '{' in
;;;      future).
;;;
;;;   2) Since every construct consists of key/value pairs, and we know the
;;;      strings that represent keys (and, in the case of feature attributes,
;;;      the strings that represent values), we can easily provide coloring of
;;;      the various syntactic elements.
;;;
;;;   3) Text within simple blocks becomes somewhat more difficult to deal with.
;;;      For example, METHOD SCOPE blocks should be using the statement-level
;;;      code from the appropriate base-language major-mode, while COMMENT
;;;      blocks should be colored in the comment color, etc.
;;;
;;; With respect to indentation, a simple algorithm is:
;;;   1) If we are at the beginning of the buffer, indent to column 0.
;;;   2) If we are currently at a line starting with 'end' (may support '}' in
;;;      future), then de-indent relative to the previous line.  However, if
;;;      the previous line starts a block, indent to the same level.
;;;   3) If we first see a line ending with ':' then we need to increase
;;;      our indentation relative to that line.
;;;   4) If we first see an 'end' line before our current line, then we should
;;;      indent our current line to the same indentation as the 'end' line.
;;;      NOTE: It is important to check for rule 3 before rule 4 (and the
;;;            ordered is reversed from the tutorial) because in Meta
;;;            it is possible to end one block and start another on the same
;;;            line.
;;;   5) If none of the above apply, then do not indent at all.
;;;
;;;   However, the above algorithm really is too simple. To make it more
;;;   powerful, the algorithm should be extended to recognize which block-valued
;;;   attribute the current line is contained within, and only perform the above
;;;   indentation of that attribute value is complex. If simple, each line
;;;   should be indented at least metaoopl-indent-offset more than the
;;;   start-of-block line, but if the line already has more indentation than
;;;   that, it should be left as-is.
;;;
;;; With respect to coloring, a simple set of rules is:
;;;   1) All construct names are colored with font-lock-metaoopl-construct-face
;;;   2) All attribute keys are colored with font-lock-metaoopl-attribute-key-face
;;;   3) All feature values are colored with font-lock-metaoopl-feature-value-face
;;;
;;;   However, this must be extended in a few ways:
;;;
;;;     - must handle COMMENT { ... } sequences, and the tutorial
;;;       doesn't address the issue of comment sequences longer than
;;;       2 characters.  Looking at the Emacs-Lisp major-mode will
;;;       help us with 3 characters (which might allow us to generalize).
;;;       Also, looking at the lisp documentation for Syntax Descriptors
;;;       linked from the tutorial.
;;;
;;;     - Cannot currently highlight non-alphanumeric sequences.  For
;;;       example, TITLE can be highlighted, but ':' cannot be.  Why is this?
;;;
;;;     - Would be useful to color the identifier of each construct,
;;;       and maybe even give each attribute-key an
;;;       attribute-value-type-specific color (i.e. 'id' and 'word'
;;;       types colors one thing, 'str' colored another, 'id-list' and
;;;       'word-list' colored another, simple blocks colored another
;;;       and complex blocks colored yet another.
;;;
;;; Overlays and Extents
;;;   Emacs and XEmacs provide some truly powerful mechanisms for providing
;;;   hierarchial views of programs that are very well suited to Meta syntax.
;;;
;;;   In particular, Emacs provides the concept of overlays, which allows one to
;;;   associated textual properties with a range of characters. This includes
;;;   assigning colors and fonts, making the text invisible, providing an
;;;   overriding or extending keymap, etc. etc. I suspect that this support is
;;;   provided at a very low level and is thus very efficient, and it opens the
;;;   door to some truly wonderful capabilities. XEmacs provides similar
;;;   support, but unfortunately uses a different mechanism (not overlays, but
;;;   rather extents). It sounds like extents are probably more powerful than
;;;   overlays (combining in one environment both Emacs overlays and Emacs text
;;;   properties). There are also claims that XEmacs supports the Emacs overlay
;;;   interface (and implements the interface using extents). However, this does
;;;   not appear to be true in XEmacs 21.4 (the various overlay-related
;;;   functions do not exist). I did encounter an abstraction API that
;;;   introduces the concept of a 'span' and implements a common span interface
;;;   using either overlays (for Emacs) or extents (for XEmacs). See
;;;   http://proofgeneral.inf.ed.ac.uk/components. I may reimplement the
;;;   following code to use span.el, but this would require that we provide
;;;   span.el in Meta. Hopefully there is a cleaner approach (if we can find out
;;;   how to provide the overlay interface in XEmacs). For now, this code does
;;;   not work in XEmacs.
;;;
;;;   The idea behind the overlay implementation is to create an overlay
;;;   for every meta-level block.  These overlays can be used for various
;;;   purposes:
;;;    - coloring a block to show its extent
;;;    - collapsing the block (making its text invisible)
;;;    - establishing a region on which base-language-specific fontification
;;;      can be applied
;;;
;;;   Some notes about the overlay implementation:
;;;    - When the region marked by an overlay is made invisible, by default
;;;      the text is still visible to cursor movement commands (but not searching
;;;      commands).
;;;       - searching commands ignore invisible text (by default, or did I do
;;;         something?)
;;;       - line movement commands can be told to ignore invisible text by
;;;         setting the 'line-move-ignore-invisible variable to true.
;;;       - cursor movement commands cannot be ignored like line-movement
;;;         commands, but overlays can have a keymap associated with them, so
;;;         the meta overlay code provides a keymap that redefines C-f and C-b
;;;         so that they jump to the end and start of the invisible region
;;;         respectively.
;;;    - When text is made invisible, it is possible to insert arbitrary visual
;;;      text at the start and/or end of the region
;;;       - this text is not "real", does not affect searches, movement,
;;;         column counts, etc.  - it is solely a visual cue.
;;;       - initial implementations of the invisibility code made an overlay
;;;         starting on a '{' and ending on a '}', and, when the region was
;;;         made invisible, inserted the marker text '{...}'.  However, this
;;;         is problematic because searches for '{' or '}' then ignore the
;;;         entire block (remember that marker text is not real, so the '{'
;;;         and '}' in the '{...}' marker text is not seen by searches).
;;;       - a better approach creates an overlay for the region from one
;;;         character after the '{' to one character before the '}' and provides
;;;         marker text '...'.
;;;           - the disadvantage of this strategy is that an individual can
;;;             move to a '{' containing subsequent invisible text, move
;;;             forward one character (so the cursor is now "inside" the invisible
;;;             text, but not yet using the overlay keymap...
;;;       - upon moving away from from using '{' and '}' to delimit blocks
;;;         (to instead using ':' and optional 'end '), the above had to change
;;;         somewhat.

;;; **************************************************************
;;; Meta Language Specific variables
;;;   - The values of these variables differ for each particular Meta language
;;;     (but not each Meta sub-language)

; (defconst metaoopl-default-font "-*-Courier New-normal-normal-normal-*-11-*-*-*-m-0-iso10646-1")
(defconst metaoopl-default-font "-*-PT Mono-normal-normal-normal-*-10-*-*-*-m-0-iso10646-1")

(defconst metaoopl-constructs     '("Attribute" "BaseLanguage" "Construct" "FeatureValue" "File" "MetaLanguage" "Template" "accessor" "arg" "assoc" "behavior" "block" "call" "case" "category" "class" "command" "field" "flag" "if" "lifecycle" "loop" "method" "namespace" "native" "receiver" "remark" "resource" "set" "switch" "testx" "var"))
(defconst metaoopl-attribute-keys '("#" "##" "##<*>" "#<*>" "->" "->" "-><*>" "-><*>" ":<*>" "<" "<*>" "<<" "<<*>" "<<<" "<<<*>" "<<<<*>" "=" "=<*>" "@" "@<*>" "access" "accessors" "alias" "alias<*>" "aliases" "aliases<*>" "associations" "associations<*>" "assocs" "assocs<*>" "autogen" "autokey" "autokey<*>" "binary" "binary<*>" "by" "by<*>" "children" "children<*>" "clinit" "clinit<*>" "clsetup" "clsetup<*>" "clsname" "clsname<*>" "clteardown" "clteardown<*>" "color" "color<*>" "comment" "comment<*>" "compilation" "compile" "compile<*>" "config" "config<*>" "decl" "decl<*>" "default" "default<*>" "defn" "defn<*>" "delim" "delim<*>" "dispatch" "else" "else<*>" "expand" "expand<*>" "expr" "expr<*>" "extensibility" "finalize" "finalize<*>" "flags" "flags<*>" "from" "from<*>" "icomment" "icomment<*>" "import" "import<*>" "inheritance" "init" "init<*>" "interface" "interface<*>" "is" "is<*>" "key" "kind" "lazy" "lazy<*>" "level" "location" "metafinalize" "metafinalize<*>" "metainit" "metainit<*>" "metaparent" "metaparent<*>" "multiplicity" "mutability" "name" "name<*>" "nmsp" "nmsp<*>" "on" "on<*>" "optimization" "over" "over<*>" "ownership" "pack" "pack<*>" "params" "params<*>" "parent" "parent<*>" "path" "path<*>" "pclsname" "pclsname<*>" "position" "postamble" "postamble<*>" "postrec" "postrec<*>" "posts" "posts<*>" "preamble" "preamble<*>" "preports" "preports<*>" "prerec" "prerec<*>" "pres" "pres<*>" "presence" "provides" "provides<*>" "replacer" "replacer<*>" "returns" "returns" "returns<*>" "returns<*>" "role" "role<*>" "scope" "scope<*>" "setup" "setup<*>" "span" "status" "suffixes" "suffixes<*>" "super" "super<*>" "target" "target<*>" "teardown" "teardown<*>" "test" "test<*>" "testparent" "testparent<*>" "testpreports" "testpreports<*>" "tests" "tests<*>" "testsuite" "testsuite<*>" "to" "to<*>" "toplevel" "toplevel<*>" "translate" "translate<*>" "type" "type<*>" "until" "until<*>" "value" "value<*>" "varname" "varname<*>" "visibility" "while" "while<*>"))
(defconst metaoopl-feature-values '("<^([!+#~-][rwxa@])+$>" "<concrete" "abstract" "aliaskey" "autodispatch" "child" "closure" "cls" "concrete" "const" "decl" "def" "explicit" "extendable" "feature" "final" "finalizer" "general" "immutable" "implicit" "initializer" "inline" "instance" "lib" "meta" "multi" "mutable" "named" "new" "nmsp" "nokey" "nometa" "nometanotest" "nonvirtual" "normal" "notest" "noval" "optional" "outline" "override" "owned" "package" "post" "postx" "pre" "prex" "primary" "private" "protected" "public" "raw" "required" "ro" "rw" "rwx" "scoped" "secondary" "showkey" "showval" "specific" "static" "std" "superx" "test" "tmpprivate" "tmppublic" "undef" "unowned" "user" "usertest" "userval" "virtual"))
(defconst metaoopl-keywords       '("complex" "enum" "expr" "id" "num" "simple" "str" "type" "word" "xid"))
(defconst metaoopl-basewords      '("alignas" "alignof" "and" "and_eq" "as" "asm" "assert" "auto" "bitand" "bitor" "bool" "break" "case" "catch" "char" "char16_t" "char32_t" "class" "compl" "const" "const_cast" "constexpr" "continue" "debugger" "decltype" "def" "default" "del" "delete" "do" "double" "dynamic_cast" "elif" "else" "enum" "except" "exec" "explicit" "export" "extends" "extern" "false" "finally" "float" "for" "friend" "from" "function" "global" "goto" "if" "implements" "import" "in" "inline" "instanceof" "int" "interface" "is" "lambda" "let" "long" "mutable" "namespace" "new" "noexcept" "not" "not_eq" "nullptr" "operator" "or" "or_eq" "package" "pass" "print" "private" "protected" "public" "raise" "register" "reinterpret_cast" "return" "short" "signed" "sizeof" "static" "static_assert" "static_cast" "struct" "super" "switch" "template" "this" "thread_local" "throw" "true" "try" "typedef" "typeid" "typename" "typeof" "union" "unsigned" "using" "var" "virtual" "void" "volatile" "wchar_t" "while" "with" "xor" "xor_eq" "yield"))

(defconst metaoopl-constructs-re     (regexp-opt metaoopl-constructs t))
(defconst metaoopl-attribute-keys-re (regexp-opt metaoopl-attribute-keys t))
(defconst metaoopl-feature-values-re (regexp-opt metaoopl-feature-values t))
(defconst metaoopl-keywords-re       (regexp-opt metaoopl-keywords t))
(defconst metaoopl-basewords-re      (regexp-opt metaoopl-basewords t))

(setq RE (make-hash-table))
(puthash 'metaoopl-Attribute-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("aliaskey" "feature" "key" "kind" "nokey" "noval" "primary" "secondary" "showkey" "showval" "undef" "userval" "value")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-Attribute-line (concat (gethash 'metaoopl-Attribute-kv RE) "\\(Attribute\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-BaseLanguage-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "concrete" "presence")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-BaseLanguage-line (concat (gethash 'metaoopl-BaseLanguage-kv RE) "\\(BaseLanguage\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-Construct-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "concrete" "presence")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-Construct-line (concat (gethash 'metaoopl-Construct-kv RE) "\\(Construct\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-FeatureValue-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-FeatureValue-line (concat (gethash 'metaoopl-FeatureValue-kv RE) "\\(FeatureValue\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-File-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-File-line (concat (gethash 'metaoopl-File-kv RE) "\\(File\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-MetaLanguage-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-MetaLanguage-line (concat (gethash 'metaoopl-MetaLanguage-kv RE) "\\(MetaLanguage\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-Template-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-Template-line (concat (gethash 'metaoopl-Template-kv RE) "\\(Template\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-accessor-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-accessor-line (concat (gethash 'metaoopl-accessor-kv RE) "\\(accessor\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-assoc-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("cls" "decl" "def" "kind" "lib" "location" "meta" "optional" "required" "status" "std" "test" "user" "usertest")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-assoc-line (concat (gethash 'metaoopl-assoc-kv RE) "\\(assoc\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-behavior-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "autodispatch" "autogen" "closure" "cls" "concrete" "const" "dispatch" "extendable" "extensibility" "final" "finalizer" "general" "immutable" "inheritance" "initializer" "inline" "instance" "kind" "location" "meta" "mutability" "mutable" "new" "nonvirtual" "notest" "optimization" "outline" "override" "package" "postx" "presence" "prex" "private" "protected" "public" "span" "specific" "static" "std" "superx" "test" "user" "usertest" "virtual" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-behavior-line (concat (gethash 'metaoopl-behavior-kv RE) "\\(behavior\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-block-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("kind" "named" "scoped" "virtual")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-block-line (concat (gethash 'metaoopl-block-kv RE) "\\(block\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-call-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-call-line (concat (gethash 'metaoopl-call-kv RE) "\\(call\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-case-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-case-line (concat (gethash 'metaoopl-case-kv RE) "\\(case\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-category-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-category-line (concat (gethash 'metaoopl-category-kv RE) "\\(category\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-class-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "autogen" "concrete" "general" "location" "meta" "nometa" "nometanotest" "notest" "presence" "private" "public" "span" "specific" "std" "test" "user" "usertest" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-class-line (concat (gethash 'metaoopl-class-kv RE) "\\(class\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-command-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("compilation" "explicit" "implicit" "inline" "kind" "named")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-command-line (concat (gethash 'metaoopl-command-kv RE) "\\(command\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-field-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("<^([!+#~-][rwxa@])+$>" "access" "accessors" "child" "inheritance" "instance" "kind" "location" "meta" "new" "optional" "override" "owned" "ownership" "position" "post" "pre" "raw" "required" "ro" "rw" "rwx" "static" "status" "test" "tmpprivate" "tmppublic" "unowned" "user" "usertest" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-field-line (concat (gethash 'metaoopl-field-kv RE) "\\(field\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-flag-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("optional" "required" "status")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-flag-line (concat (gethash 'metaoopl-flag-kv RE) "\\(flag\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-lifecycle-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "autodispatch" "autogen" "closure" "cls" "concrete" "const" "dispatch" "extendable" "extensibility" "final" "finalizer" "general" "immutable" "inheritance" "initializer" "instance" "kind" "location" "meta" "mutability" "mutable" "new" "nonvirtual" "notest" "override" "package" "postx" "presence" "prex" "private" "protected" "public" "span" "specific" "static" "std" "superx" "test" "user" "usertest" "virtual" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-lifecycle-line (concat (gethash 'metaoopl-lifecycle-kv RE) "\\(lifecycle\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-loop-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-loop-line (concat (gethash 'metaoopl-loop-kv RE) "\\(loop\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-method-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("abstract" "autodispatch" "autogen" "child" "closure" "cls" "concrete" "const" "dispatch" "extendable" "extensibility" "final" "finalizer" "general" "immutable" "inheritance" "initializer" "inline" "instance" "kind" "location" "meta" "mutability" "mutable" "new" "nonvirtual" "notest" "optimization" "outline" "override" "package" "position" "post" "postx" "pre" "presence" "prex" "private" "protected" "public" "span" "specific" "static" "std" "superx" "test" "user" "usertest" "virtual" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-method-line (concat (gethash 'metaoopl-method-kv RE) "\\(method\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-namespace-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-namespace-line (concat (gethash 'metaoopl-namespace-kv RE) "\\(namespace\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-native-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("child" "cls" "level" "location" "meta" "nmsp" "position" "post" "pre" "test" "user" "usertest")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-native-line (concat (gethash 'metaoopl-native-kv RE) "\\(native\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-receiver-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("<concrete" "abstract" "presence")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-receiver-line (concat (gethash 'metaoopl-receiver-kv RE) "\\(receiver\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-remark-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-remark-line (concat (gethash 'metaoopl-remark-kv RE) "\\(remark\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-resource-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("location" "meta" "test" "user" "usertest")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-resource-line (concat (gethash 'metaoopl-resource-kv RE) "\\(resource\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-set-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-set-line (concat (gethash 'metaoopl-set-kv RE) "\\(set\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-switch-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-switch-line (concat (gethash 'metaoopl-switch-kv RE) "\\(switch\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-testx-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '()) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-testx-line (concat (gethash 'metaoopl-testx-kv RE) "\\(testx\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-var-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("multi" "multiplicity" "normal")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-var-line (concat (gethash 'metaoopl-var-kv RE) "\\(var\\)[ \t]+\\([^ \t]+\\)") RE)
(puthash 'metaoopl-all-kv (concat "\n\\([ \t]*\\)\\(" (regexp-opt '("<^([!+#~-][rwxa@])+$>" "<concrete" "abstract" "access" "accessors" "aliaskey" "autodispatch" "autogen" "child" "closure" "cls" "compilation" "concrete" "const" "decl" "def" "dispatch" "explicit" "extendable" "extensibility" "feature" "final" "finalizer" "general" "immutable" "implicit" "inheritance" "initializer" "inline" "instance" "key" "kind" "level" "lib" "location" "meta" "multi" "multiplicity" "mutability" "mutable" "named" "new" "nmsp" "nokey" "nometa" "nometanotest" "nonvirtual" "normal" "notest" "noval" "optimization" "optional" "outline" "override" "owned" "ownership" "package" "position" "post" "postx" "pre" "presence" "prex" "primary" "private" "protected" "public" "raw" "required" "ro" "rw" "rwx" "scoped" "secondary" "showkey" "showval" "span" "specific" "static" "status" "std" "superx" "test" "tmpprivate" "tmppublic" "undef" "unowned" "user" "usertest" "userval" "value" "virtual" "visibility")) "\[ \t\]\\)*") RE)
(puthash 'metaoopl-construct-line (concat (gethash 'metaoopl-all-kv RE) "\\(" metaoopl-constructs-re "\\)[ \t]+\\([^ \t]+\\)") RE)

(defconst metaoopl-comment-start-re "\\(?:comment\\|#\\):\n")
(defconst metaoopl-comment-re "\\(?:comment\\|#\\):\n\\([ \t]+\\)\\(.*\n\\(\\1.*\n\\)*\\)")

; Various methods set these variables
(setq metaoopl-current-construct-kind nil)
(if (not (boundp 'metaoopl-meta-binary))
  (setq metaoopl-meta-binary "metac"))

(defun metaoopl-goto-construct-line (&optional target-dent)
  ;; Find the line defining the construct within which the current line
  ;; resides.  If not currently within a construct (e.g. between constructs),
  ;; find the nearest start-of-construct above point).
  ;;
  ;; If the optional target-dent is provided, it is an integer indicating the
  ;; indentation of the desired construct, in which case the method finds the
  ;; definition of the nearest (previous) construct (but only if target-dent
  ;; is smaller than the indentation of the current construct).
  ;;
  ;; Returns the integer point of the start of the line in question (after
  ;; any leading whitespace) and sets point to this location.
  ;;
  ;; NOTES
  ;;  - These notes apply to this function and many others in this file.
  ;;  - It is important to use meta-current-indentation rather than current-indentation
  ;;    because current-indentation returns 0 for invisible lines and our code
  ;;    assumes that invisible lines are treated exactly like visible lines.
  ;;  - It is often important to use (forward-line) instead of (next-line), as the
  ;;    former sets point to the beginning of the line moved to, while the latter
  ;;    does not.  Using next-line can lead to highly unusualy behavior.

  (interactive)
  (beginning-of-line)
  (while (eq 0 (meta-current-indentation))
    (forward-line -1))
  (let* ((p (point))
         ; we skip the initial newline of our construct re since we will be
         ; doing per-line matching.
         (cons-re (substring (gethash 'metaoopl-construct-line RE) 1))
         ; we ignore lines whose indentation is greater than the smallest
         ; indentation we've seen.
         (min-dent (if (null target-dent) (meta-current-indentation) target-dent))
         ; we put a limit on how many lines we search
         (c 0)
         ; we are finished scanning lines when done is t
         (done nil)
         ; for debugging issues
         (debug nil)
         ; the number of white-space chars at the beginning of this line.
         (dent min-dent)
        )
    ;; check if we are currently on a construct line.
    (if (looking-at cons-re) (setq done t))
    ;; We search upward, ignoring any line that has indentation greater than
    ;; indent.
    (while (not done)
      (forward-line -1)
      (setq c (+ c 1))
      (cond
       ; if this is a blank line, we continue searching.
       ((blank-line-p))
       ; otherwise we listen to indentation of the line.
       (t
          (setq dent (meta-current-indentation))
          (if (< dent min-dent) (setq min-dent dent))
          (if debug (message "%s has '%s': %s" (line-number-at-pos) dent (buffer-substring (line-beginning-position) (line-end-position))))
          (cond
           ; if we exceed our line limit, we stop
           ((> c 100) (setq done t) (if debug (message (format "exceeded line limit %d" 100))))
           ; we ignore any line whose indentation exceeds the smallest indent
           ; we've seen so far.
           ((> dent min-dent) (if debug (message "ignoring %d > %d" dent min-dent)))
           ; if we have a line matching a construct, we are done.
           ((looking-at cons-re) (setq done t) (if debug (message "found cons-re")))
         )))
    )
    (setq metaoopl-current-construct-kind (match-string 3))
    (message "Construct %s" metaoopl-current-construct-kind)
    (forward-char dent)
    (point)
  )
)

(defun metaoopl-current-block ()
  ;; Establish bounds of current block.
  ;; Returns (start . end) cons cell.
  (let* ((p (point))
         ; remember the line number of point
         (line (line-number-at-pos p))
         ; remember the indentation of point
         (orig-dent (meta-current-indentation))
         ; we find the construct line for the current line, which establishes
         ; the indentation we want.
         (cons-start (metaoopl-goto-construct-line))
         ; we record the line number of the construct line
         (cons-line (line-number-at-pos cons-start))
         ; we record the indentation of the construct line (NOT for line of p)
         (dent (meta-current-indentation))
         ; we need to match against lines representing constructs.
         (cons-re (substring (gethash 'metaoopl-construct-line RE) 1))
         ; debugging
         (debug t)
         ; an indication that there is no block at the current position
         noblock
         ; the start and end of our block
         s e)
    (if debug
        (message
         (format
          "p=%d line=%d od=%d cp=%d cline=%d cd=%d"
          p line orig-dent cons-start cons-line dent)))
    (goto-char p)
    (cond
     ((eq dent orig-dent)
      ; the original line has indentation that matches that of the
      ; construct it is associated with (and isn't the construct line
      ; itself). This usually happens when we are on a line containing
      ; a secondary attribute. If it defines a scope, we can simply
      ; move down one line to get ourselves into a block. If it doesn't
      ; define a scope, there is no block.
      (beginning-of-line)
      (cond
       ((looking-at ".*:$")
        ; we are on a line containing a block-valued secondary attribute,
        ; so we move into the block.
        (forward-line)
        (setq orig-dent (meta-current-indentation))
        (setq p (point))
        (if debug (message "Adjusted p=%d od=%d" p orig-dent)))
       (t
        ; we are on a line containing a non-block-valued attribute which
        ; means there is no current block.
        (setq noblock t))))
    )

    (if debug (message (format "Looking for dent %d" dent)))

    (if noblock
        nil
      ;; Scan upward from original position until we find the first line with
      ;; exactly dent indentation.
      (goto-char p)
      (while (not (eq dent (meta-current-indentation)))
        (forward-line -1))
      (end-of-line)
      (setq s (point))
      (if debug (message "Scanned up to point %d" s))

      ;; Scan downward from original position until we find the first line with
      ;; dent or less indentation (ignoring blank lines)
      (goto-char p)
      (while (or (blank-line-p) (> (meta-current-indentation) dent))
        (forward-line))

      ;(if debug (message "Found line: %s" (buffer-substring ())))

      ;; Analzye the found line.
      (cond
       ((looking-at cons-re)
        ; We are at another construct, which means we were in the last
        ; block of a construct without an explicit termination. We
        ; back up past empty lines.
        (forward-line -1)
        (while (blank-line-p) (forward-line -1))
        (end-of-line)
        (message "here with new cons"))
       ((eq (meta-current-indentation) dent)
        ; The terminating line is at expected indentation, and isn't another
        ; construct. It can be one of two things:
        ;  1) an explicit terminator or another secondary attribute key for the
        ;     construct we are currently searching
        ;  2) a feature attribute of a subsequent construct on a line before the
        ;     primary attribute of that new construct.
        ; If we are in the same construct, we want to keep trailing whitespace
        ; in the region. But if we are now in a new construct, we do NOT want to
        ; put trailing space in the new region.  Unfortunately, it is not so easy
        ; to distinguish between these two (could heuristically search for feature
        ; attributes but this could go wrong).
        ;
        ; For now, we always remove trailing whitespace ... better to have too much
        ; whitespace (which coders can remove by not having trailing whitespace
        ; at the end of a block if another attribute is occuring) than too little
        ; (the display removes spaces between constructs, which isn't readable).
        (forward-line -1)
        (while (blank-line-p) (forward-line -1))
        (end-of-line)
        (message "here with either another attribute/terminator or a feature of new construct"))
       (t
        ; The terminating line is at an indentation level less than we excepted.
        ; This means we were in the block of a construct that was not explicitly
        ; terminated, and are now in some code of the containing construct.
        ; We do the same thing here as we did when a construct line was seend.
        (forward-line -1)
        (while (blank-line-p) (forward-line -1))
        (end-of-line)))
      (setq e (point))
      (goto-char p)
      (cons s e)
    )
  )
)

(defun metaoopl-toggle-block (region &optional force)
  ;; If specified region is hidden, reveal it, else hide it.
  ;;
  ;; Args:
  ;;   region: pair e.g.  (start . end)
  ;;   force: bool
  ;;     If t, always hide (i.e. do not toggle).
  (let* ((p (point))
        ;; The list of overlays at point ... we'll look for any overlays
        ;; that exactly match the start and end of the current block. Note
        ;; that we obtain the overlays at both point and point - 1 to handle
        ;; both the situation that we are at the beginning of the region
        ;; overlayed, and at the end of the region overlayed.  May want to
        ;; instead explore the read-advance arg of make-overlay (see
        ;;   https://www.gnu.org/software/emacs/manual/html_node/elisp/
        ;;     Managing-Overlays.html#Managing-Overlays
        ;; If at beginning or end, one of the two lists will be empty, but if
        ;; we are somewhere in the middle, both lists wlil usually return the same
        ;; elements, so we obtain a unique list.
        (overlays (remove-duplicates (append (overlays-at p) (overlays-at (- p 1)))))
        ;; will be set true if we find any overlays matching the block.
        (found nil)
        ;; the overlay
        result)
    (while overlays
      (let ((overlay (car overlays)))
        (cond
         ((and (eq (overlay-start overlay) (car region))
               (eq (overlay-end overlay) (cdr region) ))
          ; we have found an overlay that exactly matches the region.
          (if force
              nil  ; do nothing if we are forcing hide
            (message "Deleting overlay")
            (delete-overlay overlay))
          (setq found t))))
      (setq overlays (cdr overlays)))
    (cond
     ((null region)
      ; we are not currently at a point that has a block .. do nothing
      t)
     ((not found)
      ; no overlay for the block was found, so we create one.
      (message
        "Creating overlay for %d to %d (invisible)" (car region) (cdr region))
      (setq result (make-overlay (car region) (cdr region) ))
      (overlay-put result 'before-string "...")
      (overlay-put result 'invisible t)
      result))))

(defun metaoopl-hide-blocks (key-pattern &optional lang-pattern)
  ;; Hide all blocks in file whose secondary key matches pattern.
  ;;   key-pattern: re
  ;;     The secondary key to match
  ;;   lang-pattern: re
  ;;     The lang-pattern to match. If not provided, .* is assumed
  (save-excursion
    (if (null lang-pattern) (setq lang-pattern ".*"))
    (let ((re (concat "\n.*" "\\(" key-pattern "\\)" "\\(<" lang-pattern ">\\)?:$")))
      ;(message "Here with '%s'" re)
      (goto-char (point-min))
      (while (re-search-forward re nil t)
        (metaoopl-toggle-current-block)))))

(defun metaoopl-hide-blocks-old (key-pattern &optional lang-pattern)
  ;; Hide all blocks in file whose secondary key matches pattern.
  ;;   key-pattern: re
  ;;     The secondary key to match
  ;;   lang-pattern: re
  ;;     The lang-pattern to match. If not provided, .* is assumed
  (save-excursion
    (if (null lang-pattern) (setq lang-pattern ".*"))
    (let ((re (concat "\n.*" key-pattern "\\(<" lang-pattern ">\\)?"  ":$")))
      (message "Here with %s" re)
      (goto-char (point-min))
      (while (re-search-forward re nil t)
        (forward-line)
        (metaoopl-toggle-current-block)))))

(defun metaoopl-hide-blocks-except (key-pattern lang-pattern)
  ;; Hide all blocks that match key-pattern that do NOT match lang-pattern.
  (save-excursion
    (goto-char (point-min))
    (let ((re (concat "\n.*" key-pattern "\\(?:<\\(.*\\)>\\)?:\s*$")))
      (message "re is %s" re)
      (while (re-search-forward re nil t)
        (let ((lang (match-string 1)))
          (if (or (null lang) (string-match lang-pattern lang))
              ; this is a sanctioned secondary attibute, so we do not
              ; hide its block.
              nil
            ; We have a non-sanctioned secondary attribute, so we
            ; advance into the block and hide it
            (message "hidding block for %s<%s>" key-pattern lang)
            (forward-line)
            (metaoopl-toggle-current-block)))))))

(defun blank-line-p ()
  ;; t if current line consists solely of whitespace.
  (not (null (string-match
   "^[[:blank:]]*$"
   (buffer-substring (line-beginning-position) (line-end-position))))))

;; ----------------------------------------------------------------------
;; Interactive command

(defun metaoopl-toggle-current-block (&optional force)
  ;; If current block is hidden, reveal it, else hide it.
  ;; If force is t, always hide, do not toggle.
  (interactive)
  (metaoopl-toggle-block (metaoopl-current-block) force))

(defun metaoopl-show-current-block ()
  (interactive)
  ; Establish bound of current block. If invoked on a line that ends with
  ; the block start char (':') and starts with $indent whitespace, it scans
  ; down for lines with MORE than $indent whitespace.  Mark is set to the
  ; end of the region (last character of last line with more $indent), and
  ; point is set to the newline after the ':' on the original line.
  (let ((region (metaoopl-current-block)))
    (goto-char (car region))
    (push-mark (cdr region) nil t)))

(defun metaoopl-remove-overlays ()
  (interactive)
  (let ((overlays (overlays-in (point-min) (point-max))))
    (while overlays
      (let ((overlay (car overlays)))
        (delete-overlay overlay))
      (setq overlays (cdr overlays)))))

(defun metaoopl-show-overlays ()
  (interactive)
  ; Show all overlays at (point)
  ;  - note that in the current implementation (2022-12-10), overlays are only
  ;    added in metaoopl-toggle-block (and are deleted there too), so this
  ;    method currently almost never shows any overlays.
  ;  - if we decide to introduce overlays for every construct, it will become
  ;    more meaningful
  (message (format "%s" (overlays-at (point)))))

(defun metaoopl-next-construct (kind &optional backward)
  ;; Find the start/end of the next construct of give kind
  (if (null kind) (setq kind "construct"))
  (let* ((p (point))
         (re (gethash (intern (concat "metaoopl-" kind "-line")) RE))
         (s (if backward (re-search-backward re nil t) (re-search-forward re nil t)))
         se)
    (cond
     (s
      ;; We have found a construct ... extract the construct info
      (let ((indent (match-string 1))
            (kvs (match-string 2))
            (kind (match-string 3))
            (id (match-string 4))
            e)
        ;; We first establish the point after the construct id.
        (setq se (match-end 0))

        ;; Fix up the start location ... we need to move back past
        ;; feature keys and values above the line the primary key is
        ;; on (and we must handle the difference in cursor position
        ;; when backward is t vs nil).
        (if (not backward) (next-line -1))
        (beginning-of-line)
        (while (looking-at (concat indent "[^ \t]"))
          (next-line -1)
          (beginning-of-line))
        (next-line 1)
        (beginning-of-line)
        ;(forward-char (length indent))
        (setq s (point))
        (goto-char se)

        ;; Now search forward for the next construct at the same indentation
        ;; level. For now, we use <indent>.*(<construct>) in the hopes that we
        ;; don't need to change '.*' to a regexp of all feature keys and feature
        ;; values. This regexp also matches '<indent>end <construct>', which is
        ;; one we want.
        (setq e
              (re-search-forward
               (concat
                "\n"
                indent
                "\\([^ \t\n].*\\)?"
                metaoopl-constructs-re
                " ")
               nil t))
        (cond
         (e
          ; We found something looking like an end of current construct
          (beginning-of-line)
          (cond
           ((looking-at "[ \t]*end ")
            ; We've found an explicit end-of-construct line.
            (end-of-line))
           (t
            ; We did not find an explicit end, so we are now at the
            ; start of in another construct. We need to move back past
            ; any featurekey/feature-vals appearing on lines above the
            ; primary construct key itself.
            (beginning-of-line)
            (while (looking-at (concat indent "[^ \t]"))
              (next-line -1)
              (beginning-of-line))
            ; Now we move back past empty lines.
            (while (looking-at "[ \t]*$")
              (next-line -1)
              (beginning-of-line))
            (end-of-line))
          ) ; end inner cond
         ) ; end e clause of outer cond
         (t
          ; We did not find any end ... assume eof
          (goto-char (point-max)))
        ) ; end outer cond

        ; The current location is the end of the construct.
        (setq e (point))
        (push-mark e)  ; set mark to end of construct
        (goto-char s)  ; move to beginning of construct

        ; We return an alist of useful info.
        (list
          (cons 'start s)
          (cons 'end e)
          (cons 'indent indent)
          (cons 'id id)
          (cons 'kind kind))
      ))
     (t
      ;;
      )
    )
  )
)

(defun metaoopl-narrow-to-current-construct (&optional kind)
  (interactive)
  (cond
   (kind
      ; by advancing one line, we ensure that if we are the first
      ; line of a construct of kind 'kind', we will narrow this
      ; construct, not the previous one.
      (next-line 1)
      (let ((data (metaoopl-next-construct kind 'backward)))
        (widen)
        (narrow-to-region
         (assoc-default 'start data)
         (assoc-default 'end data))
        (goto-char (point-min))
     ))
   (t
    ; kind is nil, so we narrow to whatever the current construct is.
    (setq metaoopl-current-construct-kind nil)
    (metaoopl-goto-construct-line)
    (if metaoopl-current-construct-kind
        (metaoopl-narrow-to-current-construct metaoopl-current-construct-kind)))
  )
)

;; ---------------------------------------------------------------
;; These are intentionally metaoopl-specific

;*****************************************
;* Construct namespace
;*****************************************

(defun metaoopl-narrow-to-current-namespace ()
  (interactive)
  (metaoopl-narrow-to-current-construct "namespace"))
(defun metaoopl-next-namespace ()
  (interactive)
  (metaoopl-next-construct "namespace"))
(defun metaoopl-prev-namespace ()
  (interactive)
  (metaoopl-next-construct "namespace" 'backward))

(defun metaoopl-insert-namespace-template (namespace_name)
  (interactive "sNamespace Name: ")
  (insert (format "
namespace %s #:
  Some docstr.
scope:

end namespace %s;
" namespace_name namespace_name)))

;*****************************************
;* Construct class
;*****************************************

(defun metaoopl-narrow-to-current-class ()
  (interactive)
  (metaoopl-narrow-to-current-construct "class"))
(defun metaoopl-next-class ()
  (interactive)
  (metaoopl-next-construct "class"))
(defun metaoopl-prev-class ()
  (interactive)
  (metaoopl-next-construct "class" 'backward))

(defun metaoopl-insert-class-template (class_name)
  (interactive "sClass Name: ")
  (insert (format "
  class %s #:
    Some docstr.
  scope:

    field f : int #:
      Some description.

    lifecycle params:
      var f -> f;
    scope:
    clinit:
    setup:
    test:
    end;

  end class %s;
" class_name class_name)))

(setq metaoopl-var-current-class nil)
(defun metaoopl-current-class ()
  (interactive)
  (let* (
      (p (point))
      (data (metaoopl-next-construct "class" 'backward))
      (clsname (assoc-default 'id data)))
    (goto-char p)
    (setq metaoopl-var-current-class clsname)
    (message (format "%s %s" (assoc-default 'kind data) clsname))))

;*****************************************
;* Construct method
;*****************************************

(defun metaoopl-narrow-to-current-method ()
  (interactive)
  (metaoopl-narrow-to-current-construct "method"))
(defun metaoopl-next-method ()
  (interactive)
  (metaoopl-next-construct "method"))
(defun metaoopl-prev-method ()
  (interactive)
  (metaoopl-next-construct "method" 'backward))
(defun metaoopl-insert-method-template (method_name method_type)
  (interactive "sMethod Name: \nsMethod Type: ")
  (insert (format "
    method %s%s #:
      docstr
    params:
      var a : int #:
        docstr
    scope:
    test:
    end method %s;
"
   method_name
   (if (string= "" method_type) "" (concat " : " method_type))
   method_name)))

;*****************************************
;* Construct field
;*****************************************

(defun metaoopl-narrow-to-current-field ()
  (interactive)
  (metaoopl-narrow-to-current-construct "field"))
(defun metaoopl-next-field ()
  (interactive)
  (metaoopl-next-construct "field"))
(defun metaoopl-prev-field ()
  (interactive)
  (metaoopl-next-construct "field" 'backward))

(defun metaoopl-insert-field-template (field_name field_type)
  (interactive "sField Name: \nsField Type: ")
  (insert (format "
    field %s : %s #:
      docstr
    scope:
      accessor get lazy:
        res = 1
        -> res
    end field %s;
" field_name field_type field_name)))

;*****************************************
;* Construct behavior
;*****************************************

(defun metaoopl-narrow-to-current-behavior ()
  (interactive)
  (metaoopl-narrow-to-current-construct "behavior"))
(defun metaoopl-next-behavior ()
  (interactive)
  (metaoopl-next-construct "behavior"))
(defun metaoopl-prev-behavior ()
  (interactive)
  (metaoopl-next-construct "behavior" 'backward))
(defun metaoopl-insert-behavior-template (behavior_name behavior_type)
  (interactive "sBehavior Name: \nsBehavior Type: ")
  (insert (format "
  behavior %s : %s #:
    docstr
  params:
    var a : int #:
      docstr
  scope:

    receive A ::
    end receiver A;

    receive B ::
    end receiver B;

  test:
  end behavior %s;
" behavior_name behavior_name behavior_type)))

;*****************************************
;* Not construct-kind-specific
;*****************************************

(defun metaoopl-python-only ()
  (interactive)
  (metaoopl-hide-blocks-except "scope" "py\\|python"))

(defun metaoopl-cpp-only ()
  (interactive)
  (metaoopl-hide-blocks-except "scope" "cpp\\|c\\+\\+"))

;; Miscellaneous metaoopl-specific
(defun metaoopl-hide-tests ()
  (interactive)
  (metaoopl-hide-blocks "tests?"))

(defun metaoopl-hide-comments ()
  (interactive)
  (metaoopl-hide-blocks "comment\\|#"))

(defun metaoopl-hide-params ()
  (interactive)
  (metaoopl-hide-blocks "params"))

(defun metaoopl-hide-assocs ()
  (interactive)
  (metaoopl-hide-blocks "assocs\\|associations"))

;;; **************************************************************
;; Service routines
(defun metaoopl-set-face (face foreground background font)
  (interactive "sFace: \nsForeground: \nsBackground: \n Font: ")

  (let ( (res (facep face)) )
      (if (not res) (setq res (make-face face)))
      (if foreground (set-face-foreground face foreground))
      (if background (set-face-background face background))
      (if font (set-face-font face font))
      ; for whatever reason, most font-lock face names are sometimes
      ; used as variables, not symbols, so we make sure that the
      ; variable for symbol 'face' is bound to 'face'.
      (set face face)
      res
  )
)

;;; **************************************************************
;;; User customization:

;; Users can call 'metaoopl-set-face' to customize the colors
;; used for Meta programs. See http://raebear.net/comp/emacscolors.html
;; for a useful way to view background and foreground colors together.
(metaoopl-set-face 'font-lock-metaoopl-class-face          "red"             nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-behavior-face       "red"             nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-method-face         "orange"          nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-field-face          "orange"          nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-construct-face      "darkgreen"       nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-attribute-key-face  "darkolivegreen"  nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-feature-value-face  "hotpink4"        nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-keyword-face        "deep pink"       nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-baseword-face       "purple"          nil  metaoopl-default-font)
(metaoopl-set-face 'font-lock-metaoopl-end-face            "ivory4"          nil  metaoopl-default-font)

;; Users can define 'metaoopl-mode-hook' to get special functionality
;; when this mode is invoked.
(defvar metaoopl-mode-hook nil
  ""
)

;; Users can specify the indentation at each level
(defvar metaoopl-indent-offset 2
  "The amount of indentation to add to lines within a scope block.  It
is also currently used for indentation within '(' ')' lists but this
will be generalized later.")

(defvar metaoopl-wrap-collapsed-block-ends t
  "When a block attribute value is collapsed, the attribute that
appears next will by default appear on the same line, which makes for
very long single lines for fully collapsed constructs.  To address this,
it is possible to insert a newline and indentation in the collapsed-block
indication string so that the next attribute appears to reside on the
next line at the proper indentation level.  If this variable is true,
such newline-indentation is provided.")
;:TEMP
(setq metaoopl-wrap-collapsed-block-ends t)
;:ENDTEMP

(defun metaoopl-make-map ()
  (let ((metaoopl-mode-map (make-keymap))
        (space-map (make-sparse-keymap))
        )
    ;; Add key bindings here
    (define-key metaoopl-mode-map "\C-j" 'newline-and-indent)

    ;; Iniital bindings for \C-@
    ;;   some emacs versions don't bind \C-@ to Ctrl space, so we
    ;;   do both
    (define-key metaoopl-mode-map [?\C-\ ] space-map)
    (define-key metaoopl-mode-map "\C-@" space-map)
    (define-key space-map [?\C-\ ] 'set-mark-command)
    (define-key space-map "\C-@" 'set-mark-command)

    ;; Add \C-@ key bindings here
    

    ;(define-key space-map [(control \,)] 'meta-toggle-prev-overlay-color)
    ;(define-key space-map [(control \.)] 'meta-toggle-next-overlay-color)
    ;(define-key space-map [(control \<)] 'meta-toggle-prev-overlay-visibility)
    ;(define-key space-map [(control \>)] 'meta-toggle-next-overlay-visibility)
    ;(define-key space-map "ro" 'meta-remove-all-overlays)
    ;(define-key space-map "vm" (lambda () (interactive) (find-file (concat (getenv "METAROOT") "/root/lib/emacs/metaoopl-mode.el"))))
    ;(define-key space-map "lm" (lambda () (interactive) (load-file (concat (getenv "METAROOT") "/root/lib/emacs/metaoopl-mode.el"))))

    ; construct-related macros
    ;(define-key space-map "cm" 'metaoopl-complete-construct)  ; intentional metaoopl
    ;(define-key space-map "b<" 'meta-parent-block)

    ;(define-key space-map "c<" 'meta-construct-beginning)
    ;(define-key space-map "c>" 'meta-construct-end)
    ;(define-key space-map "c." 'meta-collapse-construct)
    ;(define-key metaoopl-mode-map [(control \,)] 'meta-toggle-prev-overlay-color)
    ;(define-key metaoopl-mode-map [(control \.)] 'meta-toggle-next-overlay-color)
    ;(define-key metaoopl-mode-map [(control \<)] 'meta-toggle-prev-overlay-visibility)
    ;(define-key metaoopl-mode-map [(control \>)] 'meta-toggle-next-overlay-visibility)

    ; Paragraph modifying functions
    ;(define-key space-map "pa" '(lambda (prefix) (interactive "p") (let ((s (region-beginning)) (e (region-end)) d) (goto-char s) (insert "[++===") (setq d (- (point) 3)) (goto-char (+ e 6)) (insert "--]") (goto-char d))))
    ;(define-key space-map "pd" '(lambda () (interactive) (let (p) (re-search-forward "\\[\\+\\+" nil) (forward-char -3) (delete-char 3) (re-search-forward "===" nil)  (forward-char -3) (setq p (point)) (re-search-forward "--\\]") (delete-region p (point)) )))
    ;(define-key space-map "pu" '(lambda () (interactive) (let (p) (re-search-forward "\\[\\+\\+" nil) (forward-char -3) (setq p (point)) (re-search-forward "===" nil)  (delete-region p (point)) (re-search-forward "--\\]") (delete-region (- (point) 3) (point)))))

    ; return the map!
    metaoopl-mode-map
  )
)

;; We establish the map
(setq metaoopl-mode-map
;;(defvar metaoopl-mode-map
   (metaoopl-make-map)
   ;;"Keymap for Meta major mode"
)

;; Establish a file-suffix to mode mapping
(add-to-list 'auto-mode-alist '("\\.metaoopl" . metaoopl-mode))
(add-to-list 'auto-mode-alist '("\\.metaschema" . metaoopl-mode))

;; Establish which tokens get highlighted, and with which font.
(defun metaoopl-compute-font-lock-keywords ()
  (let ((executable-constructs '("method" "initializer" "finalizer" "function" "lifecycle" "behavior" "receiver" "command"))
     )
    (list
      ;; Color multi-line comment blocks
      '("\\(?:comment\\|#\\):\n\\([ \t]+\\)\\(.*\n\\(\\1.*\n\\|\n\\)*\\)" 2 font-lock-comment-face)
      ;; Color the "end" token.
      '("end\\( [a-zA-Z0-9_. ]+\\)?;" . font-lock-metaoopl-end-face)
      ;; Color literal strings.
      (cons "'[^'\n]*'" font-lock-string-face)
      ;'("#:\n\\([ \t]*.*\\)" 1 font-lock-comment-face)
      ;; constructs, attributes and feature values

      ;; These are intentionally only for Meta(Oopl)
      (cons "\\<class\\>" font-lock-metaoopl-class-face)
      (cons "\\<behavior\\>" font-lock-metaoopl-behavior-face)
      (cons (concat "\\<" (regexp-opt executable-constructs) "\\>") font-lock-metaoopl-method-face)
      (cons "\\<field\\>" font-lock-metaoopl-field-face)
      ;; End Meta(Oopl) code.

      (cons (concat "\\<" metaoopl-constructs-re     "\\>") font-lock-metaoopl-construct-face)
      (cons (concat "\\<" metaoopl-attribute-keys-re "\\>") font-lock-metaoopl-attribute-key-face)
      (cons (concat "\\<" metaoopl-feature-values-re "\\>") font-lock-metaoopl-feature-value-face)
      ;; metaoopl-level keywords
      (cons (concat "\\<" metaoopl-keywords-re "\\>") font-lock-metaoopl-keyword-face)
      ;; baselang-level keywords
      (cons (concat "\\<" metaoopl-basewords-re "\\>") font-lock-metaoopl-baseword-face)
      ;; construct ids (for now, only certain constructs).
      '("\\(class\\|method\\|function\\|closure\\|field\\|receiver\\|var\\|behavior\\)[ \t]+\\([a-zA-Z_]+[a-zA-Z0-9_]*\\)"
        2 font-lock-function-name-face)
    )))

(defvar metaoopl-font-lock-keywords (metaoopl-compute-font-lock-keywords))
; TEMP - force changes to font info into the var
(setq metaoopl-font-lock-keywords (metaoopl-compute-font-lock-keywords))
; ENDTEMP.


;; IMPORTANT:
;;  - font-locking for Meta is subtle.
;;  - read http://www.lunaryorn.com/2014/03/12/font-locking-in-emacs.html
;;    and the linked articles for some good context on font-locking in
;;    emacs.

;; We define the syntax table for Meta
;;  - each of '-', '_' and '.' are all considered parts of words
;;  - meta uses '/#' for within-scope comments
;;  - meta has a 'comment' secondary attribute defined on most constructs
;;    that is a simple block of comments ... text indented to at least the
;;    same level as the first line in the comment should be marked as a comment.
(setq metaoopl-mode-syntax-table
  (let ((metaoopl-mode-syntax-table (make-syntax-table)))

    (modify-syntax-entry ?- "w" metaoopl-mode-syntax-table)
    (modify-syntax-entry ?_ "w" metaoopl-mode-syntax-table)
    (modify-syntax-entry ?. "w" metaoopl-mode-syntax-table)

    ;; This gives C++-style comments (/* ... */ and //)
    ;; Do not yet know how to treat COMMENT { ... } as a comment
    ;;;;;(modify-syntax-entry ?/  ". 124b" metaoopl-mode-syntax-table)
    ;;;;;(modify-syntax-entry ?*  ". 23" metaoopl-mode-syntax-table)
    ;;;;;(modify-syntax-entry ?\n "> b" metaoopl-mode-syntax-table)
    ;; This gives perl-style comments ('#').
    ;;;;;(modify-syntax-entry ?#  "< b" metaoopl-mode-syntax-table)
    ;; We need to extend this to provide meta-style comments ('/#')
    ;; but I do not yet know how to do this while still providing
    ;; perl-style comments.

    ;; This gives Meta-style comments --> /#
    (cond
     (( string-match "XEmacs\||Lucid" emacs-version)

      )
     (t
      (modify-syntax-entry ?/  ". 14" metaoopl-mode-syntax-table)
      (modify-syntax-entry ?#  ". 2b" metaoopl-mode-syntax-table)
      ;(modify-syntax-entry ?\n "> a" metaoopl-mode-syntax-table)
      (modify-syntax-entry ?\n "> b" metaoopl-mode-syntax-table)

      ;; Both single quote and double quote are string delimiters, but
      ;; we cannot use the syntax table to fontify them due to how comments
      ;; are defined.
      ;;;;(modify-syntax-entry ?\' "\"" metaoopl-mode-syntax-table)
      ;;;;(modify-syntax-entry ?\" "\"" metaoopl-mode-syntax-table)

      ;; This adds in C-style multiline comments --> /* ... */
      ;; (modify-syntax-entry ?*  ". 23" metaoopl-mode-syntax-table)
      )
     )
    metaoopl-mode-syntax-table
  )
  ;;"Syntax table for metaoopl-mode"
)

;; This method indents the current line as Meta code
(defun metaoopl-indent-line ()
   "Indent current line as Meta code"
   (interactive)
   (beginning-of-line)

   ;;;   1) If we are at the beginning of the buffer, indent to column 0.
   ;;;   2) If we are currently at a line starting with '}', then
   ;;;      de-indent relative to the previous non-blank line.  However, if the
   ;;;      previous line starts a block, indent to the same level.
   ;;;   2b) Same applies for ')' as for '}'
   ;;;   2c) If line starts with 'end', de-indent relative to previous non-blank
   ;;;       line.  NOTEs:
   ;;;        - we could instead search up for the nearest line ending with ':'
   ;;;          and use the same indentation as that line.
   ;;;        - if the line is of the form 'end <construct> [<name>]', we
   ;;;          should search upwards for the nearest line with <construct>
   ;;;          (or "<construct> <name>") in it and use that line's indentation.
   ;;;          search.
   ;;;   3) If we first see a line ending with '{' then we need to increase
   ;;;      our indentation relative to that line.
   ;;;   3b) Same applies for '(' as for '{'
   ;;;   3b) Same applies for ':' as for '{'  (to support python)
   ;;;   4) If we first see an '}' line before our current line, then we should
   ;;;      indent our current line to the same indentation as the '}' line.
   ;;;      NOTE: It is important to check for rule 3 before rule 4 (and the
   ;;;            ordered is reversed from the tutorial) because in Meta
   ;;;            it is possible to end one block and start another on the same
   ;;;            line.
   ;;;   4b) Same applies for ')' as for '}'
   ;;;   5) If line has a '(' but no matching ')', indent one space past '('
   ;;;   5b) If line ends in ')', find line that has matching start paren
   ;;;       and indent to the same level as that line.
   ;;;   6) If none of the above apply, then indent at same level as closes
   ;;;      non-empty line above point.

   (message "Here in indent-line")
   ; Check for rule 1
   (if (bobp)
      (let ()
        (indent-line-to 0)
        (message "Rule 1")
      )
   ; else
      (let ((not-indented t) cur-indent)
        (cond
         ( (looking-at "^[ \t]*}") ; Check for rule 2
           (save-excursion
             (message "Rule 2")
             (forward-line -1)
             (while (looking-at "^[ \t]*$") (forward-line -1))
             (if (looking-at ".*{[ \t]*$")
               (setq cur-indent (meta-current-indentation))
               (setq cur-indent (- (meta-current-indentation) metaoopl-indent-offset))
             )
             (if (< cur-indent 0) (setq cur-indent 0)))
           )

         ( (looking-at "^[ \t]*)") ; Check for rule 2b
           (save-excursion
             (message "Rule 2b")
             (forward-line -1)
             (while (looking-at "^[ \t]*$") (forward-line -1))
             (if (looking-at ".*([ \t]*$")
               (setq cur-indent (meta-current-indentation))
               (setq cur-indent (- (meta-current-indentation) metaoopl-indent-offset))
             )
             (if (< cur-indent 0) (setq cur-indent 0)))
           )

         ( (looking-at "^[ \t]*end[; \t]") ; Check for rule 2c
           (save-excursion
             (message "Rule 2c")
             (forward-line -1)
             (while (looking-at "^[ \t]*$") (forward-line -1))
             (if (looking-at ".*([ \t]*$")
               (setq cur-indent (meta-current-indentation))
               (setq cur-indent (- (meta-current-indentation) metaoopl-indent-offset))
             )
             (if (< cur-indent 0) (setq cur-indent 0)))
           )

         (t
         ;;; else
         ;;;   We search upwards from the current line until we find some
         ;;;   indication of how to indent the current line.
          (save-excursion
            (while not-indented
              (forward-line -1)
              (while (looking-at "^[ \t]*$")
                (forward-line -1))
              (cond
                ;; If looking at a comment line, indent to same level as comment
                ((looking-at "^\\([ \t]*\\)/#")
                 (message "Comment Rule")
                 (setq cur-indent (- (match-end 1) (match-beginning 1)))
                 (setq not-indented nil))

                ;; Check for rule 3
                ((looking-at ".*{[ \t]*$")
                 (message "Rule 3")
                 (setq cur-indent (+ (meta-current-indentation) metaoopl-indent-offset))
                 (setq not-indented nil))

                ;; Check for rule 3b
                ((looking-at ".*([ \t]*$")
                 (message "Rule 3b")
                 (setq cur-indent (+ (meta-current-indentation) metaoopl-indent-offset))
                 (setq not-indented nil))

                ;; Check for rule 3c
                ((and (looking-at ".*:[ \t]*$") (not (looking-at "^[ \t]*\/\#")))
                 (message "Rule 3c")
                 (setq cur-indent (+ (meta-current-indentation) metaoopl-indent-offset))
                 (setq not-indented nil))

                ;; Check for rule 4
                ((looking-at "^[ \t]*}")
                 (message "Rule 4")
                 (setq cur-indent (meta-current-indentation))
                 (setq not-indented nil))

                ;; Check for rule 4
                ((looking-at "^[ \t]*)")
                 (message "Rule 4b")
                 (setq cur-indent (meta-current-indentation))
                 (setq not-indented nil))

                ;; Check for rule 5 - non-matching open-paren
                ((looking-at "\\(.*(\\)[^)]*$")
                 (message "Rule 5")
                 (setq cur-indent (- (match-end 1) (match-beginning 1)))
                 (setq not-indented nil))

                ;; Check for rule 5b - line ends in ')'
                ((looking-at ".*)[ \t]*$")
                   (message "Rule 5b")
                   ; TODO(wmh): cannot believe that blink-matching-open isn't
                   ; decomposed into a self-contained function that finds the
                   ; position of the matching paren.  Must make this code mor
                   ; general, as it is not guaranteed to find the matching
                   ; open paren.
                   (while not-indented
                     (cond
                       ((looking-at "^\\([ \t]*\\).*(")
                        (setq cur-indent (- (match-end 1) (match-beginning 1)))
                        (setq not-indented nil)
                        )
                       (t
                        (forward-line -1)
                       ))))

                ;; Check for rule 7
                ((looking-at "end[; ]")
                 (message "Rule 6")

                 )

                ;; Check for rule 7
                (t
                 (setq cur-indent (meta-current-indentation))
                 (setq not-indented nil))

                )))
          ))

          (if cur-indent
             (indent-line-to cur-indent)
          ;; else
          ;;   we didn't see an indentation hint, so allow no indentation
             (indent-line-to 0)
          )
      )
   )
)

(defun insert-lines-indented (list)
   "Insert the list of lines given into the current buffer, indenting
    each line as it is inserted.  There should NOT be newline characters
    within any of the strings in the list. "
    (if (null list)
       (let ())
       (insert (car list))
       (metaoopl-indent-line)
       (end-of-line)
       (insert "\n")
       (insert-lines-indented (cdr list))
    )
)

(setq metaoopl-var-current-construct "")
(defun metaoopl-insert-construct ()
   (interactive)  ;; inputs: kind and uid (see below).

   (let (
     final
     (kind
      (read-from-minibuffer
       (format "kind [%s]: " metaoopl-var-current-construct)))
     (uid (read-from-minibuffer "uid: ")))

     ;; If kind is empty, use metaoopl-var-current-construct
     (cond
      ((eq (length kind) 0)
       (setq kind metaoopl-var-current-construct)))

     ;; Insert construct start at correct indentation
     (metaoopl-indent-line)
     (insert (format "%s %s ::\n" kind uid))

     ;; Insert (empty) one line within the SCOPE
     ;;  - note that metaoopl-indent-line will indent 2 spaces relative to prev
     (metaoopl-indent-line)
     (insert "\n")
     (setq final (- (point) 1))

     ;; Insert the end-of-construct line
     ;;  - note that metaoopl-indent-line will indent 2 spaces relative to prev
     (metaoopl-indent-line)
     (backward-char 2)
     (insert (format "end %s %s;\n" kind uid))
     (goto-char final)

     ;; remember current construct
     (setq metaoopl-var-current-construct kind)
  )
)

;; The mode method
;;  - PROBLEMS TO FIX:
;;     - when in a comment block, pressing tab should indent to first character
;;       in block
;;        - however, when there is an unmatch parenthesis, indentation instead
;;          goes to that paren.
;;        - possible solutions:
;;           https://www.gnu.org/software/emacs/manual/html_node/elisp/Mode_002dSpecific-Indent.html
(defun metaoopl-mode ()
  "Major mode for editing Meta(Oopl) language files"
  (interactive)
  (kill-all-local-variables)
  (set-syntax-table metaoopl-mode-syntax-table)

  ;; We explicitly set the map here so that each time the mode
  ;; entry function is called we recompute - this is temporary
  ;; until the meta modes are stable (after which the setq
  ;; line can be removed for efficiency)
  (setq metaoopl-mode-map (metaoopl-make-map))
  (use-local-map metaoopl-mode-map)

  (set (make-local-variable 'font-lock-defaults) '(metaoopl-font-lock-keywords))
  (set (make-local-variable 'indent-line-function) 'metaoopl-indent-line)
  (set (make-local-variable 'parse-sexp-ignore-comments) t)

  ;; This ensures that multi-line fontification (e.g. comment blocks) are
  ;; properly fontified. Note that in the interests of efficiency, a limit is
  ;; put on how far back we look to find a 'comment' token, and how far forward
  ;; we look when finding the end of the comment.
  ;; TODO(wmh): explore modifying the code so that every 1000 invocations we use
  ;; a longer min/max value.
  (make-local-variable 'font-lock-extend-region-functions)
  (add-hook 'font-lock-extend-region-functions 'metaoopl-font-lock-extend-region)

  ;; This sets up comment info
  (set (make-local-variable 'comment-start) "/#")
  (set (make-local-variable 'comment-style) 'multi-line)

  (setq major-mode 'metaoopl-mode)
  (setq mode-name "Meta(Oopl)")
  (run-hooks 'metaoopl-mode-hook)
)

(defun meta-current-indentation ()
  "Establish the number of initial whitespace characters on current line.

NOTE: The 'current-indentation function does not handle indentation of invisible
text the way we need to (the indentation of such lines is reported as 0, when
we need its actual indentation to be reported)."
  (save-excursion
    (beginning-of-line)
    (let ((bol (point)))
      (forward-to-indentation 0)
      (- (point) bol))))

(defun metaoopl-closest-preceeding-block-attribute (limit)
  (let
    ((p (point)))
    (cond
      ( ;; if
        (re-search-backward
          (concat "\n\\( \\{0,6\\}\\)[^\n]*" metaoopl-attribute-keys-re ":\n")
          ;; minimum point to search back to
          (- p limit)
          ;; do not raise error on failure
          t
        )
        ;; then
        (let
          ((ws (match-string 1))
           (attr (match-string 2)))
          (message (format "ws='%s' attr=%s" ws attr))
          ;; return the start of the matched regexp, since we are using this
          ;; to determine what font-lock-beg should be.
          (match-beginning 0)
        )
      )
    )
    (goto-char p)
  )
)

;; This method helps support multi-line comment syntax highlight.
;; See
;;   https://www.gnu.org/software/emacs/manual/html_node/elisp/Multiline-Font-Lock.html
;; and
;;   https://www.emacswiki.org/emacs/MultilineFontLock
(defun metaoopl-font-lock-extend-region ()
  ; (message "Here in metaoopl-font-lock-extend-region")
  (save-excursion
    ;; NOTE: The variables 'font-lock-beg' and 'font-lock-end' are
    ;; dynamically bound by the emacs infrastructure that invokes
    ;; this function (via the font-lock-extend-region-functions
    ;; variable, whose docstr discusses this).

    ;; NOTE(wmh): The back/forward limits were changed from 2000 to
    ;; 5000 on 2022-12-10. If this causes slowdown, change them back.
    ;;
    ;; In shell
    ;;  % metac emacs oopl
    ;; In emacs, while in a buffer containing a .meta file
    ;;  Ctrl-Space m r o   # to reload the generated metaoopl-mode.el
    ;;  Ctrl-Space m e o   # to edit that file

    ;; POSSIBLE IMPROVEMENTS
    ;;  - since this function is invoked *many* times, it is best for it to be
    ;;    as fast as possible
    ;;  - for our purposes, we only need to extend font-lock-beg and/or
    ;;    font-lock-end if font-lock-beg is currently inside a comment
    ;;    (that is, the nearest preceeding occurrence of ':\n' is
    ;;    preceeded by comment or #).
    ;;  - if we start creating overlays for every construct (or if we decided
    ;;    to just make overlays for every comment block), we could ask for
    ;;      (overlays-at font-lock-beg)
    ;;    to obtain them (and return immediately with nill if no such overlays
    ;;    are found).
    ;;  - the current implementation extends the region too far sometimes
    ;;    (it searches backword for 'comment:\n' or '#:\n' instead of just
    ;;    ':\n'), and doesn't extend it enough sometimes (it limits its search
    ;;    to 5000 chars in both directions)
    (let
      (
        (current (point))
      )
      (goto-char font-lock-beg)
      (let*
        (
          (back-limit (- font-lock-beg 5000))
          (future-limit (+ font-lock-beg 5000))
          ;; TODO(wmh): This is not remotely the correct thing to search for.
          ;;  - We are really looking for the closest preceeding line that starts
          ;;    with exactly two spaces less indentation than the current line
          ;;    that ends with 'comment:\n' or '#:\n'.
          ;;  - remember that we only need to do this extension if we are in a
          ;;    comment block, and the current implementation extends in way more
          ;;    situations than it needs to.
          ;;  - REPLACE THIS CODE with something like
          ;;    (metaoopl-closest-preceeding-block-attribute)
          (found-point (re-search-backward metaoopl-comment-start-re back-limit t))
        )
        (if found-point
          (let
            (
             ;; TODO(wmh): This is searching for the wrong thing. We should be
             ;; looking for the next line whose indentation is less than that of
             ;; the current line, not another comment block!
             (last-point (re-search-forward metaoopl-comment-re future-limit t))
            )
            ;(message (format "metaoopl-font-lock-extend-region: orig=%d beg=%d end=%d found=%d last=%d" current font-lock-beg font-lock-end found-point last-point))
            (if (and last-point (> last-point font-lock-end))
                (progn
                  (message (format "metaoopl-font-lock-extend-region: extending font-lock-end from %d to %d" font-lock-end last-point))
                  (setq font-lock-end last-point)))
            ;(message (format "metaoopl-font-lock-extend-region: extending font-lock-beg from %d to %d" font-lock-beg found-point))
            (setq font-lock-beg found-point)))))))

(provide 'metaoopl-mode)

;; The following is based on
;;    https://emacs.stackexchange.com/questions/519/key-bindings-specific-to-a-buffer
;; as a means of providing an "index" for meta files.

(defvar metaoopl-minor-mode-map (make-sparse-keymap)
  "Keymap while metaoopl-minor-mode is active.")

(define-minor-mode metaoopl-minor-mode
  "A temporary minor mode to be activated."
  nil
  :lighter " MetaMinor"
  metaoopl-minor-mode-map)

(defun metaoopl-index-to-line ()
  "Provides an index to file mapping features.

  This is to be used in a buffer that displays a mapping from meta construct
  to line number, as produced by 'meta2 hier' or 'meta2 hier --org'. One can
  navigate to a desired line and press return to invoke this method, which
  does the following:
   - finds the line number specified on the current line
   - obtains the buffer the current index file is associated with (top line)
   - switches point to the window containing the named buffer and moves to
     the desired line number.
  "
  (interactive)
  (let ((p (point))
        (line (thing-at-point 'line t))
        lnum tmp buffer window)
    (message line)
    (cond
      ((string-match "^ *\\([0-9]+\\)\\|\\[\\([0-9]+\\)\\]\n" line)
         (setq lnum
          (string-to-number (or (match-string 1 line) (match-string 2 line))))
         (message (format "found lnum %d" lnum))
         (goto-char (point-min))
         (setq tmp (thing-at-point 'line t))
         (goto-char p)
         (message (format "here with first line '%s'" tmp))
         (cond
            ((string-match "^buffer: \\(.*\\)" tmp)
               (setq tmp (match-string 1 tmp))
               (message (format "here with %s:%d" tmp lnum))
               (setq buffer (get-buffer tmp))
               (setq window (get-buffer-window buffer))
               (select-window window)
               (goto-line lnum)
            )
            (t (message "ERROR: Failed to find path in first line")))
      )
      (t (message "failed")))
  )
)
(define-key metaoopl-minor-mode-map (kbd "RET") 'metaoopl-index-to-line)

(defun metaoopl-create-index (&optional prefix)
  (interactive "P")
  (metaoopl-create-index-private nil prefix)
)

(defun metaoopl-create-filtered-index (&optional prefix filter)
  (interactive "PsRegexp: ")
  (metaoopl-create-index-private filter prefix)
)

(defun metaoopl-create-index-private (filter usenum)
  "Create an index.

   Args:
     filter: str
       A regexp to filter summary lines by
     usenum: bool
       If true, use --kind=num
  "
  (let ((command
         (concat
          metaoopl-meta-binary
          " index "
          (if usenum
              "--kind=num --min=1 --adj=-1 "
              "--kind=org1 --min=1 ")
          (if filter
            (format " --filter '%s' " filter)
            "")
          (buffer-file-name)))
        (bufname (buffer-name (current-buffer))))
    (switch-to-buffer-other-window "*Meta Index*")
    (erase-buffer)
    (insert (format "buffer: %s\n" bufname))
    (message (format "COMMAND: %s" command))
    (insert (shell-command-to-string command))
    (metaoopl-mode)
    ;(orgstruct-mode)
    (metaoopl-minor-mode 1)
    (goto-char (point-min))
    (next-line 1)
  )
)

(provide 'metaoopl-minor-mode)
