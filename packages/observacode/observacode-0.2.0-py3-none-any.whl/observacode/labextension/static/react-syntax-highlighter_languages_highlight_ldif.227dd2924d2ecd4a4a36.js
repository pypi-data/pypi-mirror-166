(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_ldif"],{

/***/ "./node_modules/highlight.js/lib/languages/ldif.js":
/*!*********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/ldif.js ***!
  \*********************************************************/
/***/ ((module) => {

/*
Language: LDIF
Contributors: Jacob Childress <jacobc@gmail.com>
Category: enterprise, config
Website: https://en.wikipedia.org/wiki/LDAP_Data_Interchange_Format
*/
function ldif(hljs) {
  return {
    name: 'LDIF',
    contains: [
      {
        className: 'attribute',
        begin: '^dn',
        end: ': ',
        excludeEnd: true,
        starts: {
          end: '$',
          relevance: 0
        },
        relevance: 10
      },
      {
        className: 'attribute',
        begin: '^\\w',
        end: ': ',
        excludeEnd: true,
        starts: {
          end: '$',
          relevance: 0
        }
      },
      {
        className: 'literal',
        begin: '^-',
        end: '$'
      },
      hljs.HASH_COMMENT_MODE
    ]
  };
}

module.exports = ldif;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/ldif.js":
/*!****************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/ldif.js ***!
  \****************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  return {
    contains: [
      {
        className: 'attribute',
        begin: '^dn', end: ': ', excludeEnd: true,
        starts: {end: '$', relevance: 0},
        relevance: 10
      },
      {
        className: 'attribute',
        begin: '^\\w', end: ': ', excludeEnd: true,
        starts: {end: '$', relevance: 0}
      },
      {
        className: 'literal',
        begin: '^-', end: '$'
      },
      hljs.HASH_COMMENT_MODE
    ]
  };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_ldif.227dd2924d2ecd4a4a36.js.map