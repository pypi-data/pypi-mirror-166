"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_makefile"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/makefile.js":
/*!********************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/makefile.js ***!
  \********************************************************************************/
/***/ ((module) => {



module.exports = makefile
makefile.displayName = 'makefile'
makefile.aliases = []
function makefile(Prism) {
  Prism.languages.makefile = {
    comment: {
      pattern: /(^|[^\\])#(?:\\(?:\r\n|[\s\S])|[^\\\r\n])*/,
      lookbehind: true
    },
    string: {
      pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    },
    // Built-in target names
    builtin: /\.[A-Z][^:#=\s]+(?=\s*:(?!=))/,
    // Targets
    symbol: {
      pattern: /^[^:=\r\n]+(?=\s*:(?!=))/m,
      inside: {
        variable: /\$+(?:[^(){}:#=\s]+|(?=[({]))/
      }
    },
    variable: /\$+(?:[^(){}:#=\s]+|\([@*%<^+?][DF]\)|(?=[({]))/,
    keyword: [
      // Directives
      /-include\b|\b(?:define|else|endef|endif|export|ifn?def|ifn?eq|include|override|private|sinclude|undefine|unexport|vpath)\b/, // Functions
      {
        pattern: /(\()(?:addsuffix|abspath|and|basename|call|dir|error|eval|file|filter(?:-out)?|findstring|firstword|flavor|foreach|guile|if|info|join|lastword|load|notdir|or|origin|patsubst|realpath|shell|sort|strip|subst|suffix|value|warning|wildcard|word(?:s|list)?)(?=[ \t])/,
        lookbehind: true
      }
    ],
    operator: /(?:::|[?:+!])?=|[|@]/,
    punctuation: /[:;(){}]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/makefile.js":
/*!*************************************************!*\
  !*** ./node_modules/refractor/lang/makefile.js ***!
  \*************************************************/
/***/ ((module) => {



module.exports = makefile
makefile.displayName = 'makefile'
makefile.aliases = []
function makefile(Prism) {
  Prism.languages.makefile = {
    comment: {
      pattern: /(^|[^\\])#(?:\\(?:\r\n|[\s\S])|[^\\\r\n])*/,
      lookbehind: true
    },
    string: {
      pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    },
    'builtin-target': {
      pattern: /\.[A-Z][^:#=\s]+(?=\s*:(?!=))/,
      alias: 'builtin'
    },
    target: {
      pattern: /^(?:[^:=\s]|[ \t]+(?![\s:]))+(?=\s*:(?!=))/m,
      alias: 'symbol',
      inside: {
        variable: /\$+(?:(?!\$)[^(){}:#=\s]+|(?=[({]))/
      }
    },
    variable: /\$+(?:(?!\$)[^(){}:#=\s]+|\([@*%<^+?][DF]\)|(?=[({]))/,
    // Directives
    keyword:
      /-include\b|\b(?:define|else|endef|endif|export|ifn?def|ifn?eq|include|override|private|sinclude|undefine|unexport|vpath)\b/,
    function: {
      pattern:
        /(\()(?:abspath|addsuffix|and|basename|call|dir|error|eval|file|filter(?:-out)?|findstring|firstword|flavor|foreach|guile|if|info|join|lastword|load|notdir|or|origin|patsubst|realpath|shell|sort|strip|subst|suffix|value|warning|wildcard|word(?:list|s)?)(?=[ \t])/,
      lookbehind: true
    },
    operator: /(?:::|[?:+!])?=|[|@]/,
    punctuation: /[:;(){}]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_makefile.419d3e24ada0f4948d28.js.map