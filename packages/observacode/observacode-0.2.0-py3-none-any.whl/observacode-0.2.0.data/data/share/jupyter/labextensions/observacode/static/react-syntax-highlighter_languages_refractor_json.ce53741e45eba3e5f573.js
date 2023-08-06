"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_json"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/json.js":
/*!****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/json.js ***!
  \****************************************************************************/
/***/ ((module) => {



module.exports = json
json.displayName = 'json'
json.aliases = []
function json(Prism) {
  Prism.languages.json = {
    property: {
      pattern: /"(?:\\.|[^\\"\r\n])*"(?=\s*:)/,
      greedy: true
    },
    string: {
      pattern: /"(?:\\.|[^\\"\r\n])*"(?!\s*:)/,
      greedy: true
    },
    comment: /\/\/.*|\/\*[\s\S]*?(?:\*\/|$)/,
    number: /-?\d+\.?\d*(e[+-]?\d+)?/i,
    punctuation: /[{}[\],]/,
    operator: /:/,
    boolean: /\b(?:true|false)\b/,
    null: {
      pattern: /\bnull\b/,
      alias: 'keyword'
    }
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/json.js":
/*!*********************************************!*\
  !*** ./node_modules/refractor/lang/json.js ***!
  \*********************************************/
/***/ ((module) => {



module.exports = json
json.displayName = 'json'
json.aliases = ['webmanifest']
function json(Prism) {
  // https://www.json.org/json-en.html
  Prism.languages.json = {
    property: {
      pattern: /(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?=\s*:)/,
      lookbehind: true,
      greedy: true
    },
    string: {
      pattern: /(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?!\s*:)/,
      lookbehind: true,
      greedy: true
    },
    comment: {
      pattern: /\/\/.*|\/\*[\s\S]*?(?:\*\/|$)/,
      greedy: true
    },
    number: /-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,
    punctuation: /[{}[\],]/,
    operator: /:/,
    boolean: /\b(?:false|true)\b/,
    null: {
      pattern: /\bnull\b/,
      alias: 'keyword'
    }
  }
  Prism.languages.webmanifest = Prism.languages.json
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_json.ce53741e45eba3e5f573.js.map