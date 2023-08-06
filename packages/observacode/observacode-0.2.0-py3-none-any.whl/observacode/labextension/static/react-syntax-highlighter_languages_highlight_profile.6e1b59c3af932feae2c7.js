(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_profile"],{

/***/ "./node_modules/highlight.js/lib/languages/profile.js":
/*!************************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/profile.js ***!
  \************************************************************/
/***/ ((module) => {

/*
Language: Python profiler
Description: Python profiler results
Author: Brian Beck <exogen@gmail.com>
*/

function profile(hljs) {
  return {
    name: 'Python profiler',
    contains: [
      hljs.C_NUMBER_MODE,
      {
        begin: '[a-zA-Z_][\\da-zA-Z_]+\\.[\\da-zA-Z_]{1,3}',
        end: ':',
        excludeEnd: true
      },
      {
        begin: '(ncalls|tottime|cumtime)',
        end: '$',
        keywords: 'ncalls tottime|10 cumtime|10 filename',
        relevance: 10
      },
      {
        begin: 'function calls',
        end: '$',
        contains: [ hljs.C_NUMBER_MODE ],
        relevance: 10
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\\(',
        end: '\\)$',
        excludeBegin: true,
        excludeEnd: true,
        relevance: 0
      }
    ]
  };
}

module.exports = profile;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/profile.js":
/*!*******************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/profile.js ***!
  \*******************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  return {
    contains: [
      hljs.C_NUMBER_MODE,
      {
        begin: '[a-zA-Z_][\\da-zA-Z_]+\\.[\\da-zA-Z_]{1,3}', end: ':',
        excludeEnd: true
      },
      {
        begin: '(ncalls|tottime|cumtime)', end: '$',
        keywords: 'ncalls tottime|10 cumtime|10 filename',
        relevance: 10
      },
      {
        begin: 'function calls', end: '$',
        contains: [hljs.C_NUMBER_MODE],
        relevance: 10
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\\(', end: '\\)$',
        excludeBegin: true, excludeEnd: true,
        relevance: 0
      }
    ]
  };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_profile.6e1b59c3af932feae2c7.js.map