"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_flow"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/flow.js":
/*!****************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/flow.js ***!
  \****************************************************************************/
/***/ ((module) => {



module.exports = flow
flow.displayName = 'flow'
flow.aliases = []
function flow(Prism) {
  ;(function(Prism) {
    Prism.languages.flow = Prism.languages.extend('javascript', {})
    Prism.languages.insertBefore('flow', 'keyword', {
      type: [
        {
          pattern: /\b(?:[Nn]umber|[Ss]tring|[Bb]oolean|Function|any|mixed|null|void)\b/,
          alias: 'tag'
        }
      ]
    })
    Prism.languages.flow[
      'function-variable'
    ].pattern = /[_$a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*(?=\s*=\s*(?:function\b|(?:\([^()]*\)(?:\s*:\s*\w+)?|[_$a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*)\s*=>))/i
    delete Prism.languages.flow['parameter']
    Prism.languages.insertBefore('flow', 'operator', {
      'flow-punctuation': {
        pattern: /\{\||\|\}/,
        alias: 'punctuation'
      }
    })
    if (!Array.isArray(Prism.languages.flow.keyword)) {
      Prism.languages.flow.keyword = [Prism.languages.flow.keyword]
    }
    Prism.languages.flow.keyword.unshift(
      {
        pattern: /(^|[^$]\b)(?:type|opaque|declare|Class)\b(?!\$)/,
        lookbehind: true
      },
      {
        pattern: /(^|[^$]\B)\$(?:await|Diff|Exact|Keys|ObjMap|PropertyType|Shape|Record|Supertype|Subtype|Enum)\b(?!\$)/,
        lookbehind: true
      }
    )
  })(Prism)
}


/***/ }),

/***/ "./node_modules/refractor/lang/flow.js":
/*!*********************************************!*\
  !*** ./node_modules/refractor/lang/flow.js ***!
  \*********************************************/
/***/ ((module) => {



module.exports = flow
flow.displayName = 'flow'
flow.aliases = []
function flow(Prism) {
  ;(function (Prism) {
    Prism.languages.flow = Prism.languages.extend('javascript', {})
    Prism.languages.insertBefore('flow', 'keyword', {
      type: [
        {
          pattern:
            /\b(?:[Bb]oolean|Function|[Nn]umber|[Ss]tring|any|mixed|null|void)\b/,
          alias: 'tag'
        }
      ]
    })
    Prism.languages.flow['function-variable'].pattern =
      /(?!\s)[_$a-z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*=\s*(?:function\b|(?:\([^()]*\)(?:\s*:\s*\w+)?|(?!\s)[_$a-z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)\s*=>))/i
    delete Prism.languages.flow['parameter']
    Prism.languages.insertBefore('flow', 'operator', {
      'flow-punctuation': {
        pattern: /\{\||\|\}/,
        alias: 'punctuation'
      }
    })
    if (!Array.isArray(Prism.languages.flow.keyword)) {
      Prism.languages.flow.keyword = [Prism.languages.flow.keyword]
    }
    Prism.languages.flow.keyword.unshift(
      {
        pattern: /(^|[^$]\b)(?:Class|declare|opaque|type)\b(?!\$)/,
        lookbehind: true
      },
      {
        pattern:
          /(^|[^$]\B)\$(?:Diff|Enum|Exact|Keys|ObjMap|PropertyType|Record|Shape|Subtype|Supertype|await)\b(?!\$)/,
        lookbehind: true
      }
    )
  })(Prism)
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_flow.dea4cf8227efdf1bb242.js.map