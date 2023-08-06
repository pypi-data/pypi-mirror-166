"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_typescript"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/typescript.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/typescript.js ***!
  \**********************************************************************************/
/***/ ((module) => {



module.exports = typescript
typescript.displayName = 'typescript'
typescript.aliases = ['ts']
function typescript(Prism) {
  Prism.languages.typescript = Prism.languages.extend('javascript', {
    // From JavaScript Prism keyword list and TypeScript language spec: https://github.com/Microsoft/TypeScript/blob/master/doc/spec.md#221-reserved-words
    keyword: /\b(?:abstract|as|async|await|break|case|catch|class|const|constructor|continue|debugger|declare|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|is|keyof|let|module|namespace|new|null|of|package|private|protected|public|readonly|return|require|set|static|super|switch|this|throw|try|type|typeof|var|void|while|with|yield)\b/,
    builtin: /\b(?:string|Function|any|number|boolean|Array|symbol|console|Promise|unknown|never)\b/
  })
  Prism.languages.ts = Prism.languages.typescript
}


/***/ }),

/***/ "./node_modules/refractor/lang/typescript.js":
/*!***************************************************!*\
  !*** ./node_modules/refractor/lang/typescript.js ***!
  \***************************************************/
/***/ ((module) => {



module.exports = typescript
typescript.displayName = 'typescript'
typescript.aliases = ['ts']
function typescript(Prism) {
  ;(function (Prism) {
    Prism.languages.typescript = Prism.languages.extend('javascript', {
      'class-name': {
        pattern:
          /(\b(?:class|extends|implements|instanceof|interface|new|type)\s+)(?!keyof\b)(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?:\s*<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>)?/,
        lookbehind: true,
        greedy: true,
        inside: null // see below
      },
      builtin:
        /\b(?:Array|Function|Promise|any|boolean|console|never|number|string|symbol|unknown)\b/
    }) // The keywords TypeScript adds to JavaScript
    Prism.languages.typescript.keyword.push(
      /\b(?:abstract|declare|is|keyof|readonly|require)\b/, // keywords that have to be followed by an identifier
      /\b(?:asserts|infer|interface|module|namespace|type)\b(?=\s*(?:[{_$a-zA-Z\xA0-\uFFFF]|$))/, // This is for `import type *, {}`
      /\btype\b(?=\s*(?:[\{*]|$))/
    ) // doesn't work with TS because TS is too complex
    delete Prism.languages.typescript['parameter']
    delete Prism.languages.typescript['literal-property'] // a version of typescript specifically for highlighting types
    var typeInside = Prism.languages.extend('typescript', {})
    delete typeInside['class-name']
    Prism.languages.typescript['class-name'].inside = typeInside
    Prism.languages.insertBefore('typescript', 'function', {
      decorator: {
        pattern: /@[$\w\xA0-\uFFFF]+/,
        inside: {
          at: {
            pattern: /^@/,
            alias: 'operator'
          },
          function: /^[\s\S]+/
        }
      },
      'generic-function': {
        // e.g. foo<T extends "bar" | "baz">( ...
        pattern:
          /#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>(?=\s*\()/,
        greedy: true,
        inside: {
          function: /^#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*/,
          generic: {
            pattern: /<[\s\S]+/,
            // everything after the first <
            alias: 'class-name',
            inside: typeInside
          }
        }
      }
    })
    Prism.languages.ts = Prism.languages.typescript
  })(Prism)
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_typescript.ac925cf8df121eb22815.js.map