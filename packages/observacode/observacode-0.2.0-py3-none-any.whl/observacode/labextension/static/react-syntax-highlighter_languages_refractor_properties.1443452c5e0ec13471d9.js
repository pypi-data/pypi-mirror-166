"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_properties"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/properties.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/properties.js ***!
  \**********************************************************************************/
/***/ ((module) => {



module.exports = properties
properties.displayName = 'properties'
properties.aliases = []
function properties(Prism) {
  Prism.languages.properties = {
    comment: /^[ \t]*[#!].*$/m,
    'attr-value': {
      pattern: /(^[ \t]*(?:\\(?:\r\n|[\s\S])|[^\\\s:=])+?(?: *[=:] *| ))(?:\\(?:\r\n|[\s\S])|[^\\\r\n])+/m,
      lookbehind: true
    },
    'attr-name': /^[ \t]*(?:\\(?:\r\n|[\s\S])|[^\\\s:=])+?(?= *[=:] *| )/m,
    punctuation: /[=:]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/properties.js":
/*!***************************************************!*\
  !*** ./node_modules/refractor/lang/properties.js ***!
  \***************************************************/
/***/ ((module) => {



module.exports = properties
properties.displayName = 'properties'
properties.aliases = []
function properties(Prism) {
  Prism.languages.properties = {
    comment: /^[ \t]*[#!].*$/m,
    'attr-value': {
      pattern:
        /(^[ \t]*(?:\\(?:\r\n|[\s\S])|[^\\\s:=])+(?: *[=:] *(?! )| ))(?:\\(?:\r\n|[\s\S])|[^\\\r\n])+/m,
      lookbehind: true
    },
    'attr-name': /^[ \t]*(?:\\(?:\r\n|[\s\S])|[^\\\s:=])+(?= *[=:]| )/m,
    punctuation: /[=:]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_properties.1443452c5e0ec13471d9.js.map