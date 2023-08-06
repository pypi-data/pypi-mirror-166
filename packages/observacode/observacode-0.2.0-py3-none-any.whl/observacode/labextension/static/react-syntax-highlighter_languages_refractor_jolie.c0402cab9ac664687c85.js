"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_jolie"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/jolie.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/jolie.js ***!
  \*****************************************************************************/
/***/ ((module) => {



module.exports = jolie
jolie.displayName = 'jolie'
jolie.aliases = []
function jolie(Prism) {
  Prism.languages.jolie = Prism.languages.extend('clike', {
    keyword: /\b(?:include|define|is_defined|undef|main|init|outputPort|inputPort|Location|Protocol|Interfaces|RequestResponse|OneWay|type|interface|extender|throws|cset|csets|forward|Aggregates|Redirects|embedded|courier|execution|sequential|concurrent|single|scope|install|throw|comp|cH|default|global|linkIn|linkOut|synchronized|this|new|for|if|else|while|in|Jolie|Java|Javascript|nullProcess|spawn|constants|with|provide|until|exit|foreach|instanceof|over|service)\b/,
    builtin: /\b(?:undefined|string|int|void|long|Byte|bool|double|float|char|any)\b/,
    number: /(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?l?/i,
    operator: /-[-=>]?|\+[+=]?|<[<=]?|[>=*!]=?|&&|\|\||[:?\/%^]/,
    symbol: /[|;@]/,
    punctuation: /[,.]/,
    string: {
      pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    }
  })
  delete Prism.languages.jolie['class-name']
  Prism.languages.insertBefore('jolie', 'keyword', {
    function: {
      pattern: /((?:\b(?:outputPort|inputPort|in|service|courier)\b|@)\s*)\w+/,
      lookbehind: true
    },
    aggregates: {
      pattern: /(\bAggregates\s*:\s*)(?:\w+(?:\s+with\s+\w+)?\s*,\s*)*\w+(?:\s+with\s+\w+)?/,
      lookbehind: true,
      inside: {
        withExtension: {
          pattern: /\bwith\s+\w+/,
          inside: {
            keyword: /\bwith\b/
          }
        },
        function: {
          pattern: /\w+/
        },
        punctuation: {
          pattern: /,/
        }
      }
    },
    redirects: {
      pattern: /(\bRedirects\s*:\s*)(?:\w+\s*=>\s*\w+\s*,\s*)*(?:\w+\s*=>\s*\w+)/,
      lookbehind: true,
      inside: {
        punctuation: {
          pattern: /,/
        },
        function: {
          pattern: /\w+/
        },
        symbol: {
          pattern: /=>/
        }
      }
    }
  })
}


/***/ }),

/***/ "./node_modules/refractor/lang/jolie.js":
/*!**********************************************!*\
  !*** ./node_modules/refractor/lang/jolie.js ***!
  \**********************************************/
/***/ ((module) => {



module.exports = jolie
jolie.displayName = 'jolie'
jolie.aliases = []
function jolie(Prism) {
  Prism.languages.jolie = Prism.languages.extend('clike', {
    string: {
      pattern: /(^|[^\\])"(?:\\[\s\S]|[^"\\])*"/,
      lookbehind: true,
      greedy: true
    },
    'class-name': {
      pattern:
        /((?:\b(?:as|courier|embed|in|inputPort|outputPort|service)\b|@)[ \t]*)\w+/,
      lookbehind: true
    },
    keyword:
      /\b(?:as|cH|comp|concurrent|constants|courier|cset|csets|default|define|else|embed|embedded|execution|exit|extender|for|foreach|forward|from|global|if|import|in|include|init|inputPort|install|instanceof|interface|is_defined|linkIn|linkOut|main|new|nullProcess|outputPort|over|private|provide|public|scope|sequential|service|single|spawn|synchronized|this|throw|throws|type|undef|until|while|with)\b/,
    function: /\b[a-z_]\w*(?=[ \t]*[@(])/i,
    number: /(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?l?/i,
    operator: /-[-=>]?|\+[+=]?|<[<=]?|[>=*!]=?|&&|\|\||[?\/%^@|]/,
    punctuation: /[()[\]{},;.:]/,
    builtin:
      /\b(?:Byte|any|bool|char|double|enum|float|int|length|long|ranges|regex|string|undefined|void)\b/
  })
  Prism.languages.insertBefore('jolie', 'keyword', {
    aggregates: {
      pattern:
        /(\bAggregates\s*:\s*)(?:\w+(?:\s+with\s+\w+)?\s*,\s*)*\w+(?:\s+with\s+\w+)?/,
      lookbehind: true,
      inside: {
        keyword: /\bwith\b/,
        'class-name': /\w+/,
        punctuation: /,/
      }
    },
    redirects: {
      pattern:
        /(\bRedirects\s*:\s*)(?:\w+\s*=>\s*\w+\s*,\s*)*(?:\w+\s*=>\s*\w+)/,
      lookbehind: true,
      inside: {
        punctuation: /,/,
        'class-name': /\w+/,
        operator: /=>/
      }
    },
    property: {
      pattern:
        /\b(?:Aggregates|[Ii]nterfaces|Java|Javascript|Jolie|[Ll]ocation|OneWay|[Pp]rotocol|Redirects|RequestResponse)\b(?=[ \t]*:)/
    }
  })
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_jolie.c0402cab9ac664687c85.js.map