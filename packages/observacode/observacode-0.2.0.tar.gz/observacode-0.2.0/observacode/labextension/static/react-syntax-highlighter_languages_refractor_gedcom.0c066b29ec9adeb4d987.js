"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_gedcom"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/gedcom.js":
/*!******************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/gedcom.js ***!
  \******************************************************************************/
/***/ ((module) => {



module.exports = gedcom
gedcom.displayName = 'gedcom'
gedcom.aliases = []
function gedcom(Prism) {
  Prism.languages.gedcom = {
    'line-value': {
      // Preceded by level, optional pointer, and tag
      pattern: /(^\s*\d+ +(?:@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@ +)?\w+ +).+/m,
      lookbehind: true,
      inside: {
        pointer: {
          pattern: /^@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@$/,
          alias: 'variable'
        }
      }
    },
    tag: {
      // Preceded by level and optional pointer
      pattern: /(^\s*\d+ +(?:@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@ +)?)\w+/m,
      lookbehind: true,
      alias: 'string'
    },
    level: {
      pattern: /(^\s*)\d+/m,
      lookbehind: true,
      alias: 'number'
    },
    pointer: {
      pattern: /@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@/,
      alias: 'variable'
    }
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/gedcom.js":
/*!***********************************************!*\
  !*** ./node_modules/refractor/lang/gedcom.js ***!
  \***********************************************/
/***/ ((module) => {



module.exports = gedcom
gedcom.displayName = 'gedcom'
gedcom.aliases = []
function gedcom(Prism) {
  Prism.languages.gedcom = {
    'line-value': {
      // Preceded by level, optional pointer, and tag
      pattern:
        /(^[\t ]*\d+ +(?:@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@ +)?\w+ ).+/m,
      lookbehind: true,
      inside: {
        pointer: {
          pattern: /^@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@$/,
          alias: 'variable'
        }
      }
    },
    tag: {
      // Preceded by level and optional pointer
      pattern:
        /(^[\t ]*\d+ +(?:@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@ +)?)\w+/m,
      lookbehind: true,
      alias: 'string'
    },
    level: {
      pattern: /(^[\t ]*)\d+/m,
      lookbehind: true,
      alias: 'number'
    },
    pointer: {
      pattern: /@\w[\w!"$%&'()*+,\-./:;<=>?[\\\]^`{|}~\x80-\xfe #]*@/,
      alias: 'variable'
    }
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_gedcom.0c066b29ec9adeb4d987.js.map