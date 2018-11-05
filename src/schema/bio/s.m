MetaLanguage bio name Bio parent meta toplevel <person> #:
  The constructs in Meta(Bio).
config:

  abstract
  Construct _bioroot_ name #:
    All constructs in Meta(Bio) inherit from this abstract construct,
    so the Attribute definitions here are available in subconstructs.
    However, note that the existence of an Attribute here does NOT mean it
    is automatically included in the subconstruct ... the subconstruct
    must specify the primary attribute (and any customization of other
    values).
  config:
    
    secondary
    Attribute comment: : simple = <empty> aliases <#:> #:
      An arbitrary multi-line comment used to describe the purpose of the
      construct.

    secondary
    Attribute config: : complex = <empty> children <Construct> #:
      The complex block within which Construct/Attribute instances can be
      modified.

    secondary
    Attribute scope: : complex = <empty> aliases <::> #:
      The collection of subconstructs.

  scope:

    method kind : str scope:
      raise NotImplementedError

    method expandMeta #:
      Expand the construct.
    params:
      var output : vec<Construct> = null #:
        Where to write constructs created during expansion.  Does NOT
        include transitively created constructs. If null, do not accumulate.
    scope:
    end method expandMeta;

    override
    method translateMeta #:
      Expand the construct.
    scope:
      return (None, None)
    end method translateMeta;

  end Construct _bioroot_;

  Construct person < _bioroot_ #:
    A person for whom a bio is being defined.
  config:

    primary
    Attribute person : word = <auto> #:
      The day, in format YYYY-mm-dd or YYYYmmdd

    secondary
    Attribute given : word = <empty> #:
      First name

    secondary
    Attribute surname : word = <empty> #:
      Last name

    secondary
    Attribute dob : word = <empty> #:
      YYYY-mm-dd
      YYYY-mm
      YYYY

    Attribute comment:;
    Attribute config:;
    Attribute scope: children <video>;

  scope:

    method kind : str scope:
      raise NotImplementedError

    method expandMeta #:
      Expand the construct.
    params:
      var output : vec<Construct> = null #:
        Where to write constructs created during expansion.  Does NOT
        include transitively created constructs. If null, do not accumulate.
    scope:
    end method expandMeta;

    override
    method translateMeta #:
      Expand the construct.
    scope:
      return (None, None)
    end method translateMeta;

  end Construct day;

  Construct video < _bioroot_ #:
    A video that the person participates in.
  config:

    primary
    Attribute video : id = <auto> #:
      Some identifier for the video. Not strictly needed.

    secondary
    Attribute title : str = <empty> #:
      The official title for the video.

    Attribute comment:;
    Attribute config:;
    Attribute scope: children <source>;

  scope:

    method kind : str scope:
      raise NotImplementedError

    method expandMeta #:
      Expand the construct.
    params:
      var output : vec<Construct> = null #:
        Where to write constructs created during expansion.  Does NOT
        include transitively created constructs. If null, do not accumulate.
    scope:
    end method expandMeta;

    override
    method translateMeta #:
      Expand the construct.
    scope:
      return (None, None)
    end method translateMeta;

  end Construct video;

  Construct source < _bioroot_ #:
    A video source.
  config:

    primary
    Attribute source : id = <auto> #:
      Some identifier for the source. Not strictly needed.

    secondary
    Attribute duration : word = <empty> #:
      SS
      MM:SS
      HH:MM:SS

    Attribute comment:;
    Attribute config:;
    Attribute scope: children <source>;

  scope:

    method kind : str scope:
      raise NotImplementedError

    method expandMeta #:
      Expand the construct.
    params:
      var output : vec<Construct> = null #:
        Where to write constructs created during expansion.  Does NOT
        include transitively created constructs. If null, do not accumulate.
    scope:
    end method expandMeta;

    override
    method translateMeta #:
      Expand the construct.
    scope:
      return (None, None)
    end method translateMeta;

  end Construct source;

end MetaLanguage bio;
