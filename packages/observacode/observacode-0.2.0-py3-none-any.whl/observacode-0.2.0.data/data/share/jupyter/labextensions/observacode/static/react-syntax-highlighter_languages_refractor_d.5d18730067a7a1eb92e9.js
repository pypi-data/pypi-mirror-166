"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_d"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/d.js":
/*!*************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/d.js ***!
  \*************************************************************************/
/***/ ((module) => {



module.exports = d
d.displayName = 'd'
d.aliases = []
function d(Prism) {
  Prism.languages.d = Prism.languages.extend('clike', {
    string: [
      // r"", x""
      /\b[rx]"(?:\\[\s\S]|[^\\"])*"[cwd]?/, // q"[]", q"()", q"<>", q"{}"
      /\bq"(?:\[[\s\S]*?\]|\([\s\S]*?\)|<[\s\S]*?>|\{[\s\S]*?\})"/, // q"IDENT
      // ...
      // IDENT"
      /\bq"([_a-zA-Z][_a-zA-Z\d]*)(?:\r?\n|\r)[\s\S]*?(?:\r?\n|\r)\1"/, // q"//", q"||", etc.
      /\bq"(.)[\s\S]*?\1"/, // Characters
      /'(?:\\'|\\?[^']+)'/,
      /(["`])(?:\\[\s\S]|(?!\1)[^\\])*\1[cwd]?/
    ],
    number: [
      // The lookbehind and the negative look-ahead try to prevent bad highlighting of the .. operator
      // Hexadecimal numbers must be handled separately to avoid problems with exponent "e"
      /\b0x\.?[a-f\d_]+(?:(?!\.\.)\.[a-f\d_]*)?(?:p[+-]?[a-f\d_]+)?[ulfi]*/i,
      {
        pattern: /((?:\.\.)?)(?:\b0b\.?|\b|\.)\d[\d_]*(?:(?!\.\.)\.[\d_]*)?(?:e[+-]?\d[\d_]*)?[ulfi]*/i,
        lookbehind: true
      }
    ],
    // In order: $, keywords and special tokens, globally defined symbols
    keyword: /\$|\b(?:abstract|alias|align|asm|assert|auto|body|bool|break|byte|case|cast|catch|cdouble|cent|cfloat|char|class|const|continue|creal|dchar|debug|default|delegate|delete|deprecated|do|double|else|enum|export|extern|false|final|finally|float|for|foreach|foreach_reverse|function|goto|idouble|if|ifloat|immutable|import|inout|int|interface|invariant|ireal|lazy|long|macro|mixin|module|new|nothrow|null|out|override|package|pragma|private|protected|public|pure|real|ref|return|scope|shared|short|static|struct|super|switch|synchronized|template|this|throw|true|try|typedef|typeid|typeof|ubyte|ucent|uint|ulong|union|unittest|ushort|version|void|volatile|wchar|while|with|__(?:(?:FILE|MODULE|LINE|FUNCTION|PRETTY_FUNCTION|DATE|EOF|TIME|TIMESTAMP|VENDOR|VERSION)__|gshared|traits|vector|parameters)|string|wstring|dstring|size_t|ptrdiff_t)\b/,
    operator: /\|[|=]?|&[&=]?|\+[+=]?|-[-=]?|\.?\.\.|=[>=]?|!(?:i[ns]\b|<>?=?|>=?|=)?|\bi[ns]\b|(?:<[<>]?|>>?>?|\^\^|[*\/%^~])=?/
  })
  Prism.languages.d.comment = [
    // Shebang
    /^\s*#!.+/, // /+ +/
    {
      // Allow one level of nesting
      pattern: /(^|[^\\])\/\+(?:\/\+[\s\S]*?\+\/|[\s\S])*?\+\//,
      lookbehind: true
    }
  ].concat(Prism.languages.d.comment)
  Prism.languages.insertBefore('d', 'comment', {
    'token-string': {
      // Allow one level of nesting
      pattern: /\bq\{(?:\{[^}]*\}|[^}])*\}/,
      alias: 'string'
    }
  })
  Prism.languages.insertBefore('d', 'keyword', {
    property: /\B@\w*/
  })
  Prism.languages.insertBefore('d', 'function', {
    register: {
      // Iasm registers
      pattern: /\b(?:[ABCD][LHX]|E[ABCD]X|E?(?:BP|SP|DI|SI)|[ECSDGF]S|CR[0234]|DR[012367]|TR[3-7]|X?MM[0-7]|R[ABCD]X|[BS]PL|R[BS]P|[DS]IL|R[DS]I|R(?:[89]|1[0-5])[BWD]?|XMM(?:[89]|1[0-5])|YMM(?:1[0-5]|\d))\b|\bST(?:\([0-7]\)|\b)/,
      alias: 'variable'
    }
  })
}


/***/ }),

/***/ "./node_modules/refractor/lang/d.js":
/*!******************************************!*\
  !*** ./node_modules/refractor/lang/d.js ***!
  \******************************************/
/***/ ((module) => {



module.exports = d
d.displayName = 'd'
d.aliases = []
function d(Prism) {
  Prism.languages.d = Prism.languages.extend('clike', {
    comment: [
      {
        // Shebang
        pattern: /^\s*#!.+/,
        greedy: true
      },
      {
        pattern: RegExp(
          /(^|[^\\])/.source +
            '(?:' +
            [
              // /+ comment +/
              // Allow one level of nesting
              /\/\+(?:\/\+(?:[^+]|\+(?!\/))*\+\/|(?!\/\+)[\s\S])*?\+\//.source, // // comment
              /\/\/.*/.source, // /* comment */
              /\/\*[\s\S]*?\*\//.source
            ].join('|') +
            ')'
        ),
        lookbehind: true,
        greedy: true
      }
    ],
    string: [
      {
        pattern: RegExp(
          [
            // r"", x""
            /\b[rx]"(?:\\[\s\S]|[^\\"])*"[cwd]?/.source, // q"[]", q"()", q"<>", q"{}"
            /\bq"(?:\[[\s\S]*?\]|\([\s\S]*?\)|<[\s\S]*?>|\{[\s\S]*?\})"/.source, // q"IDENT
            // ...
            // IDENT"
            /\bq"((?!\d)\w+)$[\s\S]*?^\1"/.source, // q"//", q"||", etc.
            // eslint-disable-next-line regexp/strict
            /\bq"(.)[\s\S]*?\2"/.source, // eslint-disable-next-line regexp/strict
            /(["`])(?:\\[\s\S]|(?!\3)[^\\])*\3[cwd]?/.source
          ].join('|'),
          'm'
        ),
        greedy: true
      },
      {
        pattern: /\bq\{(?:\{[^{}]*\}|[^{}])*\}/,
        greedy: true,
        alias: 'token-string'
      }
    ],
    // In order: $, keywords and special tokens, globally defined symbols
    keyword:
      /\$|\b(?:__(?:(?:DATE|EOF|FILE|FUNCTION|LINE|MODULE|PRETTY_FUNCTION|TIMESTAMP|TIME|VENDOR|VERSION)__|gshared|parameters|traits|vector)|abstract|alias|align|asm|assert|auto|body|bool|break|byte|case|cast|catch|cdouble|cent|cfloat|char|class|const|continue|creal|dchar|debug|default|delegate|delete|deprecated|do|double|dstring|else|enum|export|extern|false|final|finally|float|for|foreach|foreach_reverse|function|goto|idouble|if|ifloat|immutable|import|inout|int|interface|invariant|ireal|lazy|long|macro|mixin|module|new|nothrow|null|out|override|package|pragma|private|protected|ptrdiff_t|public|pure|real|ref|return|scope|shared|short|size_t|static|string|struct|super|switch|synchronized|template|this|throw|true|try|typedef|typeid|typeof|ubyte|ucent|uint|ulong|union|unittest|ushort|version|void|volatile|wchar|while|with|wstring)\b/,
    number: [
      // The lookbehind and the negative look-ahead try to prevent bad highlighting of the .. operator
      // Hexadecimal numbers must be handled separately to avoid problems with exponent "e"
      /\b0x\.?[a-f\d_]+(?:(?!\.\.)\.[a-f\d_]*)?(?:p[+-]?[a-f\d_]+)?[ulfi]{0,4}/i,
      {
        pattern:
          /((?:\.\.)?)(?:\b0b\.?|\b|\.)\d[\d_]*(?:(?!\.\.)\.[\d_]*)?(?:e[+-]?\d[\d_]*)?[ulfi]{0,4}/i,
        lookbehind: true
      }
    ],
    operator:
      /\|[|=]?|&[&=]?|\+[+=]?|-[-=]?|\.?\.\.|=[>=]?|!(?:i[ns]\b|<>?=?|>=?|=)?|\bi[ns]\b|(?:<[<>]?|>>?>?|\^\^|[*\/%^~])=?/
  })
  Prism.languages.insertBefore('d', 'string', {
    // Characters
    // 'a', '\\', '\n', '\xFF', '\377', '\uFFFF', '\U0010FFFF', '\quot'
    char: /'(?:\\(?:\W|\w+)|[^\\])'/
  })
  Prism.languages.insertBefore('d', 'keyword', {
    property: /\B@\w*/
  })
  Prism.languages.insertBefore('d', 'function', {
    register: {
      // Iasm registers
      pattern:
        /\b(?:[ABCD][LHX]|E?(?:BP|DI|SI|SP)|[BS]PL|[ECSDGF]S|CR[0234]|[DS]IL|DR[012367]|E[ABCD]X|X?MM[0-7]|R(?:1[0-5]|[89])[BWD]?|R[ABCD]X|R[BS]P|R[DS]I|TR[3-7]|XMM(?:1[0-5]|[89])|YMM(?:1[0-5]|\d))\b|\bST(?:\([0-7]\)|\b)/,
      alias: 'variable'
    }
  })
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_d.5d18730067a7a1eb92e9.js.map