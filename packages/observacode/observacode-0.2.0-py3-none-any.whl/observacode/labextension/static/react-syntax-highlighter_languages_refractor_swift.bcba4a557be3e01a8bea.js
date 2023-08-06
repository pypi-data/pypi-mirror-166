"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_swift"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/swift.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/swift.js ***!
  \*****************************************************************************/
/***/ ((module) => {



module.exports = swift
swift.displayName = 'swift'
swift.aliases = []
function swift(Prism) {
  // issues: nested multiline comments
  Prism.languages.swift = Prism.languages.extend('clike', {
    string: {
      pattern: /("|')(\\(?:\((?:[^()]|\([^)]+\))+\)|\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
      greedy: true,
      inside: {
        interpolation: {
          pattern: /\\\((?:[^()]|\([^)]+\))+\)/,
          inside: {
            delimiter: {
              pattern: /^\\\(|\)$/,
              alias: 'variable'
            } // See rest below
          }
        }
      }
    },
    keyword: /\b(?:as|associativity|break|case|catch|class|continue|convenience|default|defer|deinit|didSet|do|dynamic(?:Type)?|else|enum|extension|fallthrough|final|for|func|get|guard|if|import|in|infix|init|inout|internal|is|lazy|left|let|mutating|new|none|nonmutating|operator|optional|override|postfix|precedence|prefix|private|protocol|public|repeat|required|rethrows|return|right|safe|self|Self|set|static|struct|subscript|super|switch|throws?|try|Type|typealias|unowned|unsafe|var|weak|where|while|willSet|__(?:COLUMN__|FILE__|FUNCTION__|LINE__))\b/,
    number: /\b(?:[\d_]+(?:\.[\de_]+)?|0x[a-f0-9_]+(?:\.[a-f0-9p_]+)?|0b[01_]+|0o[0-7_]+)\b/i,
    constant: /\b(?:nil|[A-Z_]{2,}|k[A-Z][A-Za-z_]+)\b/,
    atrule: /@\b(?:IB(?:Outlet|Designable|Action|Inspectable)|class_protocol|exported|noreturn|NS(?:Copying|Managed)|objc|UIApplicationMain|auto_closure)\b/,
    builtin: /\b(?:[A-Z]\S+|abs|advance|alignof(?:Value)?|assert|contains|count(?:Elements)?|debugPrint(?:ln)?|distance|drop(?:First|Last)|dump|enumerate|equal|filter|find|first|getVaList|indices|isEmpty|join|last|lexicographicalCompare|map|max(?:Element)?|min(?:Element)?|numericCast|overlaps|partition|print(?:ln)?|reduce|reflect|reverse|sizeof(?:Value)?|sort(?:ed)?|split|startsWith|stride(?:of(?:Value)?)?|suffix|swap|toDebugString|toString|transcode|underestimateCount|unsafeBitCast|with(?:ExtendedLifetime|Unsafe(?:MutablePointers?|Pointers?)|VaList))\b/
  })
  Prism.languages.swift['string'].inside['interpolation'].inside.rest =
    Prism.languages.swift
}


/***/ }),

/***/ "./node_modules/refractor/lang/swift.js":
/*!**********************************************!*\
  !*** ./node_modules/refractor/lang/swift.js ***!
  \**********************************************/
/***/ ((module) => {



module.exports = swift
swift.displayName = 'swift'
swift.aliases = []
function swift(Prism) {
  Prism.languages.swift = {
    comment: {
      // Nested comments are supported up to 2 levels
      pattern:
        /(^|[^\\:])(?:\/\/.*|\/\*(?:[^/*]|\/(?!\*)|\*(?!\/)|\/\*(?:[^*]|\*(?!\/))*\*\/)*\*\/)/,
      lookbehind: true,
      greedy: true
    },
    'string-literal': [
      // https://docs.swift.org/swift-book/LanguageGuide/StringsAndCharacters.html
      {
        pattern: RegExp(
          /(^|[^"#])/.source +
            '(?:' + // single-line string
            /"(?:\\(?:\((?:[^()]|\([^()]*\))*\)|\r\n|[^(])|[^\\\r\n"])*"/
              .source +
            '|' + // multi-line string
            /"""(?:\\(?:\((?:[^()]|\([^()]*\))*\)|[^(])|[^\\"]|"(?!""))*"""/
              .source +
            ')' +
            /(?!["#])/.source
        ),
        lookbehind: true,
        greedy: true,
        inside: {
          interpolation: {
            pattern: /(\\\()(?:[^()]|\([^()]*\))*(?=\))/,
            lookbehind: true,
            inside: null // see below
          },
          'interpolation-punctuation': {
            pattern: /^\)|\\\($/,
            alias: 'punctuation'
          },
          punctuation: /\\(?=[\r\n])/,
          string: /[\s\S]+/
        }
      },
      {
        pattern: RegExp(
          /(^|[^"#])(#+)/.source +
            '(?:' + // single-line string
            /"(?:\\(?:#+\((?:[^()]|\([^()]*\))*\)|\r\n|[^#])|[^\\\r\n])*?"/
              .source +
            '|' + // multi-line string
            /"""(?:\\(?:#+\((?:[^()]|\([^()]*\))*\)|[^#])|[^\\])*?"""/.source +
            ')' +
            '\\2'
        ),
        lookbehind: true,
        greedy: true,
        inside: {
          interpolation: {
            pattern: /(\\#+\()(?:[^()]|\([^()]*\))*(?=\))/,
            lookbehind: true,
            inside: null // see below
          },
          'interpolation-punctuation': {
            pattern: /^\)|\\#+\($/,
            alias: 'punctuation'
          },
          string: /[\s\S]+/
        }
      }
    ],
    directive: {
      // directives with conditions
      pattern: RegExp(
        /#/.source +
          '(?:' +
          (/(?:elseif|if)\b/.source +
            '(?:[ \t]*' + // This regex is a little complex. It's equivalent to this:
            //   (?:![ \t]*)?(?:\b\w+\b(?:[ \t]*<round>)?|<round>)(?:[ \t]*(?:&&|\|\|))?
            // where <round> is a general parentheses expression.
            /(?:![ \t]*)?(?:\b\w+\b(?:[ \t]*\((?:[^()]|\([^()]*\))*\))?|\((?:[^()]|\([^()]*\))*\))(?:[ \t]*(?:&&|\|\|))?/
              .source +
            ')+') +
          '|' +
          /(?:else|endif)\b/.source +
          ')'
      ),
      alias: 'property',
      inside: {
        'directive-name': /^#\w+/,
        boolean: /\b(?:false|true)\b/,
        number: /\b\d+(?:\.\d+)*\b/,
        operator: /!|&&|\|\||[<>]=?/,
        punctuation: /[(),]/
      }
    },
    literal: {
      pattern:
        /#(?:colorLiteral|column|dsohandle|file(?:ID|Literal|Path)?|function|imageLiteral|line)\b/,
      alias: 'constant'
    },
    'other-directive': {
      pattern: /#\w+\b/,
      alias: 'property'
    },
    attribute: {
      pattern: /@\w+/,
      alias: 'atrule'
    },
    'function-definition': {
      pattern: /(\bfunc\s+)\w+/,
      lookbehind: true,
      alias: 'function'
    },
    label: {
      // https://docs.swift.org/swift-book/LanguageGuide/ControlFlow.html#ID141
      pattern:
        /\b(break|continue)\s+\w+|\b[a-zA-Z_]\w*(?=\s*:\s*(?:for|repeat|while)\b)/,
      lookbehind: true,
      alias: 'important'
    },
    keyword:
      /\b(?:Any|Protocol|Self|Type|actor|as|assignment|associatedtype|associativity|async|await|break|case|catch|class|continue|convenience|default|defer|deinit|didSet|do|dynamic|else|enum|extension|fallthrough|fileprivate|final|for|func|get|guard|higherThan|if|import|in|indirect|infix|init|inout|internal|is|isolated|lazy|left|let|lowerThan|mutating|none|nonisolated|nonmutating|open|operator|optional|override|postfix|precedencegroup|prefix|private|protocol|public|repeat|required|rethrows|return|right|safe|self|set|some|static|struct|subscript|super|switch|throw|throws|try|typealias|unowned|unsafe|var|weak|where|while|willSet)\b/,
    boolean: /\b(?:false|true)\b/,
    nil: {
      pattern: /\bnil\b/,
      alias: 'constant'
    },
    'short-argument': /\$\d+\b/,
    omit: {
      pattern: /\b_\b/,
      alias: 'keyword'
    },
    number:
      /\b(?:[\d_]+(?:\.[\de_]+)?|0x[a-f0-9_]+(?:\.[a-f0-9p_]+)?|0b[01_]+|0o[0-7_]+)\b/i,
    // A class name must start with an upper-case letter and be either 1 letter long or contain a lower-case letter.
    'class-name': /\b[A-Z](?:[A-Z_\d]*[a-z]\w*)?\b/,
    function: /\b[a-z_]\w*(?=\s*\()/i,
    constant: /\b(?:[A-Z_]{2,}|k[A-Z][A-Za-z_]+)\b/,
    // Operators are generic in Swift. Developers can even create new operators (e.g. +++).
    // https://docs.swift.org/swift-book/ReferenceManual/zzSummaryOfTheGrammar.html#ID481
    // This regex only supports ASCII operators.
    operator: /[-+*/%=!<>&|^~?]+|\.[.\-+*/%=!<>&|^~?]+/,
    punctuation: /[{}[\]();,.:\\]/
  }
  Prism.languages.swift['string-literal'].forEach(function (rule) {
    rule.inside['interpolation'].inside = Prism.languages.swift
  })
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_swift.bcba4a557be3e01a8bea.js.map