"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_scala"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/java.js":
/*!****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/java.js ***!
  \****************************************************************************/
/***/ ((module) => {



module.exports = java
java.displayName = 'java'
java.aliases = []
function java(Prism) {
  ;(function(Prism) {
    var keywords = /\b(?:abstract|continue|for|new|switch|assert|default|goto|package|synchronized|boolean|do|if|private|this|break|double|implements|protected|throw|byte|else|import|public|throws|case|enum|instanceof|return|transient|catch|extends|int|short|try|char|final|interface|static|void|class|finally|long|strictfp|volatile|const|float|native|super|while|var|null|exports|module|open|opens|provides|requires|to|transitive|uses|with)\b/ // based on the java naming conventions
    var className = /\b[A-Z](?:\w*[a-z]\w*)?\b/
    Prism.languages.java = Prism.languages.extend('clike', {
      'class-name': [
        className, // variables and parameters
        // this to support class names (or generic parameters) which do not contain a lower case letter (also works for methods)
        /\b[A-Z]\w*(?=\s+\w+\s*[;,=())])/
      ],
      keyword: keywords,
      function: [
        Prism.languages.clike.function,
        {
          pattern: /(\:\:)[a-z_]\w*/,
          lookbehind: true
        }
      ],
      number: /\b0b[01][01_]*L?\b|\b0x[\da-f_]*\.?[\da-f_p+-]+\b|(?:\b\d[\d_]*\.?[\d_]*|\B\.\d[\d_]*)(?:e[+-]?\d[\d_]*)?[dfl]?/i,
      operator: {
        pattern: /(^|[^.])(?:<<=?|>>>?=?|->|([-+&|])\2|[?:~]|[-+*/%&|^!=<>]=?)/m,
        lookbehind: true
      }
    })
    Prism.languages.insertBefore('java', 'class-name', {
      annotation: {
        alias: 'punctuation',
        pattern: /(^|[^.])@\w+/,
        lookbehind: true
      },
      namespace: {
        pattern: /(\b(?:exports|import(?:\s+static)?|module|open|opens|package|provides|requires|to|transitive|uses|with)\s+)[a-z]\w*(\.[a-z]\w*)+/,
        lookbehind: true,
        inside: {
          punctuation: /\./
        }
      },
      generics: {
        pattern: /<(?:[\w\s,.&?]|<(?:[\w\s,.&?]|<(?:[\w\s,.&?]|<[\w\s,.&?]*>)*>)*>)*>/,
        inside: {
          'class-name': className,
          keyword: keywords,
          punctuation: /[<>(),.:]/,
          operator: /[?&|]/
        }
      }
    })
  })(Prism)
}


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/scala.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/scala.js ***!
  \*****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {


var refractorJava = __webpack_require__(/*! ./java.js */ "./node_modules/react-code-blocks/node_modules/refractor/lang/java.js")
module.exports = scala
scala.displayName = 'scala'
scala.aliases = []
function scala(Prism) {
  Prism.register(refractorJava)
  Prism.languages.scala = Prism.languages.extend('java', {
    keyword: /<-|=>|\b(?:abstract|case|catch|class|def|do|else|extends|final|finally|for|forSome|if|implicit|import|lazy|match|new|null|object|override|package|private|protected|return|sealed|self|super|this|throw|trait|try|type|val|var|while|with|yield)\b/,
    string: [
      {
        pattern: /"""[\s\S]*?"""/,
        greedy: true
      },
      {
        pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,
        greedy: true
      }
    ],
    builtin: /\b(?:String|Int|Long|Short|Byte|Boolean|Double|Float|Char|Any|AnyRef|AnyVal|Unit|Nothing)\b/,
    number: /\b0x[\da-f]*\.?[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e\d+)?[dfl]?/i,
    symbol: /'[^\d\s\\]\w*/
  })
  delete Prism.languages.scala['class-name']
  delete Prism.languages.scala['function']
}


/***/ }),

/***/ "./node_modules/refractor/lang/java.js":
/*!*********************************************!*\
  !*** ./node_modules/refractor/lang/java.js ***!
  \*********************************************/
/***/ ((module) => {



module.exports = java
java.displayName = 'java'
java.aliases = []
function java(Prism) {
  ;(function (Prism) {
    var keywords =
      /\b(?:abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|exports|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|module|native|new|non-sealed|null|open|opens|package|permits|private|protected|provides|public|record|requires|return|sealed|short|static|strictfp|super|switch|synchronized|this|throw|throws|to|transient|transitive|try|uses|var|void|volatile|while|with|yield)\b/ // full package (optional) + parent classes (optional)
    var classNamePrefix = /(^|[^\w.])(?:[a-z]\w*\s*\.\s*)*(?:[A-Z]\w*\s*\.\s*)*/
      .source // based on the java naming conventions
    var className = {
      pattern: RegExp(classNamePrefix + /[A-Z](?:[\d_A-Z]*[a-z]\w*)?\b/.source),
      lookbehind: true,
      inside: {
        namespace: {
          pattern: /^[a-z]\w*(?:\s*\.\s*[a-z]\w*)*(?:\s*\.)?/,
          inside: {
            punctuation: /\./
          }
        },
        punctuation: /\./
      }
    }
    Prism.languages.java = Prism.languages.extend('clike', {
      string: {
        pattern: /(^|[^\\])"(?:\\.|[^"\\\r\n])*"/,
        lookbehind: true,
        greedy: true
      },
      'class-name': [
        className,
        {
          // variables and parameters
          // this to support class names (or generic parameters) which do not contain a lower case letter (also works for methods)
          pattern: RegExp(
            classNamePrefix + /[A-Z]\w*(?=\s+\w+\s*[;,=()])/.source
          ),
          lookbehind: true,
          inside: className.inside
        }
      ],
      keyword: keywords,
      function: [
        Prism.languages.clike.function,
        {
          pattern: /(::\s*)[a-z_]\w*/,
          lookbehind: true
        }
      ],
      number:
        /\b0b[01][01_]*L?\b|\b0x(?:\.[\da-f_p+-]+|[\da-f_]+(?:\.[\da-f_p+-]+)?)\b|(?:\b\d[\d_]*(?:\.[\d_]*)?|\B\.\d[\d_]*)(?:e[+-]?\d[\d_]*)?[dfl]?/i,
      operator: {
        pattern:
          /(^|[^.])(?:<<=?|>>>?=?|->|--|\+\+|&&|\|\||::|[?:~]|[-+*/%&|^!=<>]=?)/m,
        lookbehind: true
      }
    })
    Prism.languages.insertBefore('java', 'string', {
      'triple-quoted-string': {
        // http://openjdk.java.net/jeps/355#Description
        pattern: /"""[ \t]*[\r\n](?:(?:"|"")?(?:\\.|[^"\\]))*"""/,
        greedy: true,
        alias: 'string'
      },
      char: {
        pattern: /'(?:\\.|[^'\\\r\n]){1,6}'/,
        greedy: true
      }
    })
    Prism.languages.insertBefore('java', 'class-name', {
      annotation: {
        pattern: /(^|[^.])@\w+(?:\s*\.\s*\w+)*/,
        lookbehind: true,
        alias: 'punctuation'
      },
      generics: {
        pattern:
          /<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&))*>)*>)*>)*>/,
        inside: {
          'class-name': className,
          keyword: keywords,
          punctuation: /[<>(),.:]/,
          operator: /[?&|]/
        }
      },
      namespace: {
        pattern: RegExp(
          /(\b(?:exports|import(?:\s+static)?|module|open|opens|package|provides|requires|to|transitive|uses|with)\s+)(?!<keyword>)[a-z]\w*(?:\.[a-z]\w*)*\.?/.source.replace(
            /<keyword>/g,
            function () {
              return keywords.source
            }
          )
        ),
        lookbehind: true,
        inside: {
          punctuation: /\./
        }
      }
    })
  })(Prism)
}


/***/ }),

/***/ "./node_modules/refractor/lang/scala.js":
/*!**********************************************!*\
  !*** ./node_modules/refractor/lang/scala.js ***!
  \**********************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {


var refractorJava = __webpack_require__(/*! ./java.js */ "./node_modules/refractor/lang/java.js")
module.exports = scala
scala.displayName = 'scala'
scala.aliases = []
function scala(Prism) {
  Prism.register(refractorJava)
  Prism.languages.scala = Prism.languages.extend('java', {
    'triple-quoted-string': {
      pattern: /"""[\s\S]*?"""/,
      greedy: true,
      alias: 'string'
    },
    string: {
      pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,
      greedy: true
    },
    keyword:
      /<-|=>|\b(?:abstract|case|catch|class|def|do|else|extends|final|finally|for|forSome|if|implicit|import|lazy|match|new|null|object|override|package|private|protected|return|sealed|self|super|this|throw|trait|try|type|val|var|while|with|yield)\b/,
    number:
      /\b0x(?:[\da-f]*\.)?[\da-f]+|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e\d+)?[dfl]?/i,
    builtin:
      /\b(?:Any|AnyRef|AnyVal|Boolean|Byte|Char|Double|Float|Int|Long|Nothing|Short|String|Unit)\b/,
    symbol: /'[^\d\s\\]\w*/
  })
  Prism.languages.insertBefore('scala', 'triple-quoted-string', {
    'string-interpolation': {
      pattern:
        /\b[a-z]\w*(?:"""(?:[^$]|\$(?:[^{]|\{(?:[^{}]|\{[^{}]*\})*\}))*?"""|"(?:[^$"\r\n]|\$(?:[^{]|\{(?:[^{}]|\{[^{}]*\})*\}))*")/i,
      greedy: true,
      inside: {
        id: {
          pattern: /^\w+/,
          greedy: true,
          alias: 'function'
        },
        escape: {
          pattern: /\\\$"|\$[$"]/,
          greedy: true,
          alias: 'symbol'
        },
        interpolation: {
          pattern: /\$(?:\w+|\{(?:[^{}]|\{[^{}]*\})*\})/,
          greedy: true,
          inside: {
            punctuation: /^\$\{?|\}$/,
            expression: {
              pattern: /[\s\S]+/,
              inside: Prism.languages.scala
            }
          }
        },
        string: /[\s\S]+/
      }
    }
  })
  delete Prism.languages.scala['class-name']
  delete Prism.languages.scala['function']
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_scala.8662f1b920e446f689b1.js.map