goog.module('metax.root.Object');
goog.module.declareLegacyNamespace();

const {MetaObject} = goog.require('metax.root.ObjectMeta');

class Object_ extends Object {

  constructor() {
    super();
    var self = this;
    // User-provided code follows.
  };

  meta() {
    return MetaObject;
  };
}

exports = Object_;

