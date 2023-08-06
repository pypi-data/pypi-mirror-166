"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_monkey"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/monkey.js":
/*!******************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/monkey.js ***!
  \******************************************************************************/
/***/ ((module) => {



module.exports = monkey
monkey.displayName = 'monkey'
monkey.aliases = []
function monkey(Prism) {
  Prism.languages.monkey = {
    string: /"[^"\r\n]*"/,
    comment: [
      {
        pattern: /^#Rem\s+[\s\S]*?^#End/im,
        greedy: true
      },
      {
        pattern: /'.+/,
        greedy: true
      }
    ],
    preprocessor: {
      pattern: /(^[ \t]*)#.+/m,
      lookbehind: true,
      alias: 'comment'
    },
    function: /\w+(?=\()/,
    'type-char': {
      pattern: /(\w)[?%#$]/,
      lookbehind: true,
      alias: 'variable'
    },
    number: {
      pattern: /((?:\.\.)?)(?:(?:\b|\B-\.?|\B\.)\d+(?:(?!\.\.)\.\d*)?|\$[\da-f]+)/i,
      lookbehind: true
    },
    keyword: /\b(?:Void|Strict|Public|Private|Property|Bool|Int|Float|String|Array|Object|Continue|Exit|Import|Extern|New|Self|Super|Try|Catch|Eachin|True|False|Extends|Abstract|Final|Select|Case|Default|Const|Local|Global|Field|Method|Function|Class|End|If|Then|Else|ElseIf|EndIf|While|Wend|Repeat|Until|Forever|For|To|Step|Next|Return|Module|Interface|Implements|Inline|Throw|Null)\b/i,
    operator: /\.\.|<[=>]?|>=?|:?=|(?:[+\-*\/&~|]|\b(?:Mod|Shl|Shr)\b)=?|\b(?:And|Not|Or)\b/i,
    punctuation: /[.,:;()\[\]]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/monkey.js":
/*!***********************************************!*\
  !*** ./node_modules/refractor/lang/monkey.js ***!
  \***********************************************/
/***/ ((module) => {



module.exports = monkey
monkey.displayName = 'monkey'
monkey.aliases = []
function monkey(Prism) {
  Prism.languages.monkey = {
    comment: {
      pattern: /^#Rem\s[\s\S]*?^#End|'.+/im,
      greedy: true
    },
    string: {
      pattern: /"[^"\r\n]*"/,
      greedy: true
    },
    preprocessor: {
      pattern: /(^[ \t]*)#.+/m,
      lookbehind: true,
      greedy: true,
      alias: 'property'
    },
    function: /\b\w+(?=\()/,
    'type-char': {
      pattern: /\b[?%#$]/,
      alias: 'class-name'
    },
    number: {
      pattern:
        /((?:\.\.)?)(?:(?:\b|\B-\.?|\B\.)\d+(?:(?!\.\.)\.\d*)?|\$[\da-f]+)/i,
      lookbehind: true
    },
    keyword:
      /\b(?:Abstract|Array|Bool|Case|Catch|Class|Const|Continue|Default|Eachin|Else|ElseIf|End|EndIf|Exit|Extends|Extern|False|Field|Final|Float|For|Forever|Function|Global|If|Implements|Import|Inline|Int|Interface|Local|Method|Module|New|Next|Null|Object|Private|Property|Public|Repeat|Return|Select|Self|Step|Strict|String|Super|Then|Throw|To|True|Try|Until|Void|Wend|While)\b/i,
    operator:
      /\.\.|<[=>]?|>=?|:?=|(?:[+\-*\/&~|]|\b(?:Mod|Shl|Shr)\b)=?|\b(?:And|Not|Or)\b/i,
    punctuation: /[.,:;()\[\]]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_monkey.61c28ded7cbfa755e7d5.js.map