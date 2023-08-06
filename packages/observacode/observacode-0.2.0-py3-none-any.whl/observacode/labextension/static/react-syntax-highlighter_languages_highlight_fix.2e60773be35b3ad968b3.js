(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_fix"],{

/***/ "./node_modules/highlight.js/lib/languages/fix.js":
/*!********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/fix.js ***!
  \********************************************************/
/***/ ((module) => {

/*
Language: FIX
Author: Brent Bradbury <brent@brentium.com>
*/

/** @type LanguageFn */
function fix(hljs) {
  return {
    name: 'FIX',
    contains: [{
      begin: /[^\u2401\u0001]+/,
      end: /[\u2401\u0001]/,
      excludeEnd: true,
      returnBegin: true,
      returnEnd: false,
      contains: [
        {
          begin: /([^\u2401\u0001=]+)/,
          end: /=([^\u2401\u0001=]+)/,
          returnEnd: true,
          returnBegin: false,
          className: 'attr'
        },
        {
          begin: /=/,
          end: /([\u2401\u0001])/,
          excludeEnd: true,
          excludeBegin: true,
          className: 'string'
        }
      ]
    }],
    case_insensitive: true
  };
}

module.exports = fix;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/fix.js":
/*!***************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/fix.js ***!
  \***************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  return {
    contains: [
    {
      begin: /[^\u2401\u0001]+/,
      end: /[\u2401\u0001]/,
      excludeEnd: true,
      returnBegin: true,
      returnEnd: false,
      contains: [
      {
        begin: /([^\u2401\u0001=]+)/,
        end: /=([^\u2401\u0001=]+)/,
        returnEnd: true,
        returnBegin: false,
        className: 'attr'
      },
      {
        begin: /=/,
        end: /([\u2401\u0001])/,
        excludeEnd: true,
        excludeBegin: true,
        className: 'string'
      }]
    }],
    case_insensitive: true
  };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_fix.2e60773be35b3ad968b3.js.map