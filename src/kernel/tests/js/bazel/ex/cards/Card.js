// https://github.com/bazelbuild/rules_closure
// http://usejsdoc.org/howto-es2015-classes.html
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
// https://github.com/google/closure-library/wiki/goog.module:-an-ES6-module-like-alternative-to-goog.provide
goog.module('ex.cards.Card');
//goog.module.declareLegacyNamespace();

/**
 * Class representing a card 
 * @class
 */
class Card {
  /**
   * Create a Card.
   * @param {*} deck
   *   The deck this card belongs to.
   * @param {number} rank
   *   The rank of the card
   * @param {number} suit
   *   The suit of the card
   * @member {*} _deck
   * @member {number} _rank
   * @member {number} _suit
   */
  constructor(deck, rank, suit) {
    // TODO(wmh): Establish how to get this working when we use
    //   this.rankIs(rank);
    //
    // Currently the compiler is raising errors of the form:
    //    ex/cards/Card.js:44: ERROR - Property _rank never defined on module$exports$ex$cards$Card
    //      rank() { return this._rank; }
    //                           ^
    //      ProTip: "JSC_INEXISTENT_PROPERTY" or "checkTypes" or "missingProperties" can be added to the `suppress` attribute of:
    //      //ex/cards:Card
    //      Alternatively /** @suppress {missingProperties} */ can be added to the source file.
    //    
    //    ex/cards/Card.js:49: ERROR - Cannot add a property to a struct instance after it is constructed. (If you already declared the property, make sure to give it a type.)
    //      rankIs(value) { this._rank = value; return this;}
    //                           ^
    //      ProTip: "JSC_ILLEGAL_PROPERTY_CREATION" or "checkTypes" can be added to the `suppress` attribute of:
    //      //ex/cards:Card
    //      Alternatively /** @suppress {checkTypes} */ can be added to the source file.
    //    
    //    ex/cards/Card.js:59: ERROR - Property _rank never defined on module$exports$ex$cards$Card
    //      debug() { return '<' + this._rank + ', ' + this._suit + '>'; }
    //                                  ^
    //      ProTip: "JSC_INEXISTENT_PROPERTY" or "checkTypes" or "missingProperties" can be added to the `suppress` attribute of:
    //      //ex/cards:Card
    //      Alternatively /** @suppress {missingProperties} */ can be added to the source file.
    //
    // The above situation is a problem because:
    //   1) we want to encourage the use of the method setters over raw
    //      field access, but any field the user specifies by setter must
    //      still be pre-initialized by property beforehand (inefficient)
    //   2) initializing a property directly does not perform any of the
    //      functionality in the setter, which defeats the purpose of having
    //      a setter ... it is supposed to be executed *every* time a field
    //      is modified.
    //
    // The only way to ensure correctness is to pre-initialize any field that
    // the user does not initialize-by-property (if they use the setter, we must
    // still pre-initialize).  Can we do something about this using
    // Object.defineProperty()?
    //   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty
    // I believe this would need to be used after the class is defined (by
    // which time the compiler will have complained about errors), or within
    // the constructor (presumably even more inefficient than just initializing
    // the field normally).

    this._rank = rank;
    this._suit = suit;
    this._deck = deck;

    /** @type {number} */ this._tmp = 1;
  }

  /** @return {*} The deck. */
  deck() { return this._deck; }
  /** 
   * @param {*} value 
   * @return {!Card} The card.
   */
  deckIs(value) { this._deck = value; return this;}

  /** @return {number} The rank. */
  rank() { return this._rank; }
  /**
   * @param {number} value - the rank
   * @return {!Card} The card.
   */
  rankIs(value) { this._rank = value; return this;}

  /** @return {number} The suit. */
  suit() { return this._suit; }
  /**
   * @param {number} value - the suit
   * @return {!Card} The card.
   */
  suitIs(value) { this._suit = value; return this;}

  debug() { return '<' + this._rank + ', ' + this._suit + '>'; }

  /** @returns {number} */
  get val() { return this._tmp; }

  /** @param {number} num */
  set val(num) { this._tmp = num; }
}

exports = Card;


