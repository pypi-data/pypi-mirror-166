(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_dart"],{

/***/ "./node_modules/highlight.js/lib/languages/dart.js":
/*!*********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/dart.js ***!
  \*********************************************************/
/***/ ((module) => {

/*
Language: Dart
Requires: markdown.js
Author: Maxim Dikun <dikmax@gmail.com>
Description: Dart a modern, object-oriented language developed by Google. For more information see https://www.dartlang.org/
Website: https://dart.dev
Category: scripting
*/

/** @type LanguageFn */
function dart(hljs) {
  const SUBST = {
    className: 'subst',
    variants: [{
      begin: '\\$[A-Za-z0-9_]+'
    }]
  };

  const BRACED_SUBST = {
    className: 'subst',
    variants: [{
      begin: /\$\{/,
      end: /\}/
    }],
    keywords: 'true false null this is new super'
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: 'r\'\'\'',
        end: '\'\'\''
      },
      {
        begin: 'r"""',
        end: '"""'
      },
      {
        begin: 'r\'',
        end: '\'',
        illegal: '\\n'
      },
      {
        begin: 'r"',
        end: '"',
        illegal: '\\n'
      },
      {
        begin: '\'\'\'',
        end: '\'\'\'',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '"""',
        end: '"""',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '\'',
        end: '\'',
        illegal: '\\n',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '"',
        end: '"',
        illegal: '\\n',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      }
    ]
  };
  BRACED_SUBST.contains = [
    hljs.C_NUMBER_MODE,
    STRING
  ];

  const BUILT_IN_TYPES = [
    // dart:core
    'Comparable',
    'DateTime',
    'Duration',
    'Function',
    'Iterable',
    'Iterator',
    'List',
    'Map',
    'Match',
    'Object',
    'Pattern',
    'RegExp',
    'Set',
    'Stopwatch',
    'String',
    'StringBuffer',
    'StringSink',
    'Symbol',
    'Type',
    'Uri',
    'bool',
    'double',
    'int',
    'num',
    // dart:html
    'Element',
    'ElementList'
  ];
  const NULLABLE_BUILT_IN_TYPES = BUILT_IN_TYPES.map((e) => `${e}?`);

  const KEYWORDS = {
    keyword: 'abstract as assert async await break case catch class const continue covariant default deferred do ' +
      'dynamic else enum export extends extension external factory false final finally for Function get hide if ' +
      'implements import in inferface is late library mixin new null on operator part required rethrow return set ' +
      'show static super switch sync this throw true try typedef var void while with yield',
    built_in:
      BUILT_IN_TYPES
        .concat(NULLABLE_BUILT_IN_TYPES)
        .concat([
          // dart:core
          'Never',
          'Null',
          'dynamic',
          'print',
          // dart:html
          'document',
          'querySelector',
          'querySelectorAll',
          'window'
        ]),
    $pattern: /[A-Za-z][A-Za-z0-9_]*\??/
  };

  return {
    name: 'Dart',
    keywords: KEYWORDS,
    contains: [
      STRING,
      hljs.COMMENT(
        /\/\*\*(?!\/)/,
        /\*\//,
        {
          subLanguage: 'markdown',
          relevance: 0
        }
      ),
      hljs.COMMENT(
        /\/{3,} ?/,
        /$/, {
          contains: [{
            subLanguage: 'markdown',
            begin: '.',
            end: '$',
            relevance: 0
          }]
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /\{/,
        excludeEnd: true,
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '@[A-Za-z]+'
      },
      {
        begin: '=>' // No markup, just a relevance booster
      }
    ]
  };
}

module.exports = dart;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/dart.js":
/*!****************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/dart.js ***!
  \****************************************************************************************/
/***/ ((module) => {

module.exports = function (hljs) {
  var SUBST = {
    className: 'subst',
    variants: [
       {begin: '\\$[A-Za-z0-9_]+'}
    ],
  };

  var BRACED_SUBST = {
    className: 'subst',
    variants: [
       {begin: '\\${', end: '}'},
    ],
    keywords: 'true false null this is new super',
  };

  var STRING = {
    className: 'string',
    variants: [
      {
        begin: 'r\'\'\'', end: '\'\'\''
      },
      {
        begin: 'r"""', end: '"""'
      },
      {
        begin: 'r\'', end: '\'',
        illegal: '\\n'
      },
      {
        begin: 'r"', end: '"',
        illegal: '\\n'
      },
      {
        begin: '\'\'\'', end: '\'\'\'',
        contains: [hljs.BACKSLASH_ESCAPE, SUBST, BRACED_SUBST]
      },
      {
        begin: '"""', end: '"""',
        contains: [hljs.BACKSLASH_ESCAPE, SUBST, BRACED_SUBST]
      },
      {
        begin: '\'', end: '\'',
        illegal: '\\n',
        contains: [hljs.BACKSLASH_ESCAPE, SUBST, BRACED_SUBST]
      },
      {
        begin: '"', end: '"',
        illegal: '\\n',
        contains: [hljs.BACKSLASH_ESCAPE, SUBST, BRACED_SUBST]
      }
    ]
  };
  BRACED_SUBST.contains = [
    hljs.C_NUMBER_MODE, STRING
  ];

  var KEYWORDS = {
    keyword: 'assert async await break case catch class const continue default do else enum extends false final ' +
      'finally for if in is new null rethrow return super switch sync this throw true try var void while with yield ' +
      'abstract as dynamic export external factory get implements import library operator part set static typedef',
    built_in:
      // dart:core
      'print Comparable DateTime Duration Function Iterable Iterator List Map Match Null Object Pattern RegExp Set ' +
      'Stopwatch String StringBuffer StringSink Symbol Type Uri bool double int num ' +
      // dart:html
      'document window querySelector querySelectorAll Element ElementList'
  };

  return {
    keywords: KEYWORDS,
    contains: [
      STRING,
      hljs.COMMENT(
        '/\\*\\*',
        '\\*/',
        {
          subLanguage: 'markdown'
        }
      ),
      hljs.COMMENT(
        '///',
        '$',
        {
          subLanguage: 'markdown'
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'class',
        beginKeywords: 'class interface', end: '{', excludeEnd: true,
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      hljs.C_NUMBER_MODE,
      {
        className: 'meta', begin: '@[A-Za-z]+'
      },
      {
        begin: '=>' // No markup, just a relevance booster
      }
    ]
  }
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_dart.0456df0e4ba99f7f4649.js.map