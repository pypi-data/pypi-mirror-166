"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_smalltalk"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/smalltalk.js":
/*!*********************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/smalltalk.js ***!
  \*********************************************************************************/
/***/ ((module) => {



module.exports = smalltalk
smalltalk.displayName = 'smalltalk'
smalltalk.aliases = []
function smalltalk(Prism) {
  Prism.languages.smalltalk = {
    comment: /"(?:""|[^"])*"/,
    string: /'(?:''|[^'])*'/,
    symbol: /#[\da-z]+|#(?:-|([+\/\\*~<>=@%|&?!])\1?)|#(?=\()/i,
    'block-arguments': {
      pattern: /(\[\s*):[^\[|]*\|/,
      lookbehind: true,
      inside: {
        variable: /:[\da-z]+/i,
        punctuation: /\|/
      }
    },
    'temporary-variables': {
      pattern: /\|[^|]+\|/,
      inside: {
        variable: /[\da-z]+/i,
        punctuation: /\|/
      }
    },
    keyword: /\b(?:nil|true|false|self|super|new)\b/,
    character: {
      pattern: /\$./,
      alias: 'string'
    },
    number: [
      /\d+r-?[\dA-Z]+(?:\.[\dA-Z]+)?(?:e-?\d+)?/,
      /\b\d+(?:\.\d+)?(?:e-?\d+)?/
    ],
    operator: /[<=]=?|:=|~[~=]|\/\/?|\\\\|>[>=]?|[!^+\-*&|,@]/,
    punctuation: /[.;:?\[\](){}]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/smalltalk.js":
/*!**************************************************!*\
  !*** ./node_modules/refractor/lang/smalltalk.js ***!
  \**************************************************/
/***/ ((module) => {



module.exports = smalltalk
smalltalk.displayName = 'smalltalk'
smalltalk.aliases = []
function smalltalk(Prism) {
  Prism.languages.smalltalk = {
    comment: {
      pattern: /"(?:""|[^"])*"/,
      greedy: true
    },
    char: {
      pattern: /\$./,
      greedy: true
    },
    string: {
      pattern: /'(?:''|[^'])*'/,
      greedy: true
    },
    symbol: /#[\da-z]+|#(?:-|([+\/\\*~<>=@%|&?!])\1?)|#(?=\()/i,
    'block-arguments': {
      pattern: /(\[\s*):[^\[|]*\|/,
      lookbehind: true,
      inside: {
        variable: /:[\da-z]+/i,
        punctuation: /\|/
      }
    },
    'temporary-variables': {
      pattern: /\|[^|]+\|/,
      inside: {
        variable: /[\da-z]+/i,
        punctuation: /\|/
      }
    },
    keyword: /\b(?:new|nil|self|super)\b/,
    boolean: /\b(?:false|true)\b/,
    number: [
      /\d+r-?[\dA-Z]+(?:\.[\dA-Z]+)?(?:e-?\d+)?/,
      /\b\d+(?:\.\d+)?(?:e-?\d+)?/
    ],
    operator: /[<=]=?|:=|~[~=]|\/\/?|\\\\|>[>=]?|[!^+\-*&|,@]/,
    punctuation: /[.;:?\[\](){}]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_smalltalk.dd4dc1a7bb36160718ad.js.map