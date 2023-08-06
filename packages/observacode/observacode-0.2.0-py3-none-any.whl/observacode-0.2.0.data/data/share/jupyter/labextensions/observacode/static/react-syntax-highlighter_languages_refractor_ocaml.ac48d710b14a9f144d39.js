"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_ocaml"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/ocaml.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/ocaml.js ***!
  \*****************************************************************************/
/***/ ((module) => {



module.exports = ocaml
ocaml.displayName = 'ocaml'
ocaml.aliases = []
function ocaml(Prism) {
  Prism.languages.ocaml = {
    comment: /\(\*[\s\S]*?\*\)/,
    string: [
      {
        pattern: /"(?:\\.|[^\\\r\n"])*"/,
        greedy: true
      },
      {
        pattern: /(['`])(?:\\(?:\d+|x[\da-f]+|.)|(?!\1)[^\\\r\n])\1/i,
        greedy: true
      }
    ],
    number: /\b(?:0x[\da-f][\da-f_]+|(?:0[bo])?\d[\d_]*\.?[\d_]*(?:e[+-]?[\d_]+)?)/i,
    type: {
      pattern: /\B['`]\w*/,
      alias: 'variable'
    },
    directive: {
      pattern: /\B#\w+/,
      alias: 'function'
    },
    keyword: /\b(?:as|assert|begin|class|constraint|do|done|downto|else|end|exception|external|for|fun|function|functor|if|in|include|inherit|initializer|lazy|let|match|method|module|mutable|new|object|of|open|prefix|private|rec|then|sig|struct|to|try|type|val|value|virtual|where|while|with)\b/,
    boolean: /\b(?:false|true)\b/,
    // Custom operators are allowed
    operator: /:=|[=<>@^|&+\-*\/$%!?~][!$%&*+\-.\/:<=>?@^|~]*|\b(?:and|asr|land|lor|lxor|lsl|lsr|mod|nor|or)\b/,
    punctuation: /[(){}\[\]|_.,:;]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/ocaml.js":
/*!**********************************************!*\
  !*** ./node_modules/refractor/lang/ocaml.js ***!
  \**********************************************/
/***/ ((module) => {



module.exports = ocaml
ocaml.displayName = 'ocaml'
ocaml.aliases = []
function ocaml(Prism) {
  // https://ocaml.org/manual/lex.html
  Prism.languages.ocaml = {
    comment: {
      pattern: /\(\*[\s\S]*?\*\)/,
      greedy: true
    },
    char: {
      pattern: /'(?:[^\\\r\n']|\\(?:.|[ox]?[0-9a-f]{1,3}))'/i,
      greedy: true
    },
    string: [
      {
        pattern: /"(?:\\(?:[\s\S]|\r\n)|[^\\\r\n"])*"/,
        greedy: true
      },
      {
        pattern: /\{([a-z_]*)\|[\s\S]*?\|\1\}/,
        greedy: true
      }
    ],
    number: [
      // binary and octal
      /\b(?:0b[01][01_]*|0o[0-7][0-7_]*)\b/i, // hexadecimal
      /\b0x[a-f0-9][a-f0-9_]*(?:\.[a-f0-9_]*)?(?:p[+-]?\d[\d_]*)?(?!\w)/i, // decimal
      /\b\d[\d_]*(?:\.[\d_]*)?(?:e[+-]?\d[\d_]*)?(?!\w)/i
    ],
    directive: {
      pattern: /\B#\w+/,
      alias: 'property'
    },
    label: {
      pattern: /\B~\w+/,
      alias: 'property'
    },
    'type-variable': {
      pattern: /\B'\w+/,
      alias: 'function'
    },
    variant: {
      pattern: /`\w+/,
      alias: 'symbol'
    },
    // For the list of keywords and operators,
    // see: http://caml.inria.fr/pub/docs/manual-ocaml/lex.html#sec84
    keyword:
      /\b(?:as|assert|begin|class|constraint|do|done|downto|else|end|exception|external|for|fun|function|functor|if|in|include|inherit|initializer|lazy|let|match|method|module|mutable|new|nonrec|object|of|open|private|rec|sig|struct|then|to|try|type|val|value|virtual|when|where|while|with)\b/,
    boolean: /\b(?:false|true)\b/,
    'operator-like-punctuation': {
      pattern: /\[[<>|]|[>|]\]|\{<|>\}/,
      alias: 'punctuation'
    },
    // Custom operators are allowed
    operator:
      /\.[.~]|:[=>]|[=<>@^|&+\-*\/$%!?~][!$%&*+\-.\/:<=>?@^|~]*|\b(?:and|asr|land|lor|lsl|lsr|lxor|mod|or)\b/,
    punctuation: /;;|::|[(){}\[\].,:;#]|\b_\b/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_ocaml.ac48d710b14a9f144d39.js.map