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
