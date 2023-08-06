"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_rip"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/rip.js":
/*!***************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/rip.js ***!
  \***************************************************************************/
/***/ ((module) => {



module.exports = rip
rip.displayName = 'rip'
rip.aliases = []
function rip(Prism) {
  Prism.languages.rip = {
    comment: /#.*/,
    keyword: /(?:=>|->)|\b(?:class|if|else|switch|case|return|exit|try|catch|finally|raise)\b/,
    builtin: /@|\bSystem\b/,
    boolean: /\b(?:true|false)\b/,
    date: /\b\d{4}-\d{2}-\d{2}\b/,
    time: /\b\d{2}:\d{2}:\d{2}\b/,
    datetime: /\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b/,
    character: /\B`[^\s`'",.:;#\/\\()<>\[\]{}]\b/,
    regex: {
      pattern: /(^|[^/])\/(?!\/)(\[.+?]|\\.|[^/\\\r\n])+\/(?=\s*($|[\r\n,.;})]))/,
      lookbehind: true,
      greedy: true
    },
    symbol: /:[^\d\s`'",.:;#\/\\()<>\[\]{}][^\s`'",.:;#\/\\()<>\[\]{}]*/,
    string: {
      pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    },
    number: /[+-]?(?:(?:\d+\.\d+)|(?:\d+))/,
    punctuation: /(?:\.{2,3})|[`,.:;=\/\\()<>\[\]{}]/,
    reference: /[^\d\s`'",.:;#\/\\()<>\[\]{}][^\s`'",.:;#\/\\()<>\[\]{}]*/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/rip.js":
/*!********************************************!*\
  !*** ./node_modules/refractor/lang/rip.js ***!
  \********************************************/
/***/ ((module) => {



module.exports = rip
rip.displayName = 'rip'
rip.aliases = []
function rip(Prism) {
  Prism.languages.rip = {
    comment: {
      pattern: /#.*/,
      greedy: true
    },
    char: {
      pattern: /\B`[^\s`'",.:;#\/\\()<>\[\]{}]\b/,
      greedy: true
    },
    string: {
      pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    },
    regex: {
      pattern:
        /(^|[^/])\/(?!\/)(?:\[[^\n\r\]]*\]|\\.|[^/\\\r\n\[])+\/(?=\s*(?:$|[\r\n,.;})]))/,
      lookbehind: true,
      greedy: true
    },
    keyword:
      /(?:=>|->)|\b(?:case|catch|class|else|exit|finally|if|raise|return|switch|try)\b/,
    builtin: /@|\bSystem\b/,
    boolean: /\b(?:false|true)\b/,
    date: /\b\d{4}-\d{2}-\d{2}\b/,
    time: /\b\d{2}:\d{2}:\d{2}\b/,
    datetime: /\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b/,
    symbol: /:[^\d\s`'",.:;#\/\\()<>\[\]{}][^\s`'",.:;#\/\\()<>\[\]{}]*/,
    number: /[+-]?\b(?:\d+\.\d+|\d+)\b/,
    punctuation: /(?:\.{2,3})|[`,.:;=\/\\()<>\[\]{}]/,
    reference: /[^\d\s`'",.:;#\/\\()<>\[\]{}][^\s`'",.:;#\/\\()<>\[\]{}]*/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_rip.e10d8f4edc1804aaf8d5.js.map