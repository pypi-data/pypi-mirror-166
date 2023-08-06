(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_ceylon"],{

/***/ "./node_modules/highlight.js/lib/languages/ceylon.js":
/*!***********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/ceylon.js ***!
  \***********************************************************/
/***/ ((module) => {

/*
Language: Ceylon
Author: Lucas Werkmeister <mail@lucaswerkmeister.de>
Website: https://ceylon-lang.org
*/

/** @type LanguageFn */
function ceylon(hljs) {
  // 2.3. Identifiers and keywords
  const KEYWORDS =
    'assembly module package import alias class interface object given value ' +
    'assign void function new of extends satisfies abstracts in out return ' +
    'break continue throw assert dynamic if else switch case for while try ' +
    'catch finally then let this outer super is exists nonempty';
  // 7.4.1 Declaration Modifiers
  const DECLARATION_MODIFIERS =
    'shared abstract formal default actual variable late native deprecated ' +
    'final sealed annotation suppressWarnings small';
  // 7.4.2 Documentation
  const DOCUMENTATION =
    'doc by license see throws tagged';
  const SUBST = {
    className: 'subst',
    excludeBegin: true,
    excludeEnd: true,
    begin: /``/,
    end: /``/,
    keywords: KEYWORDS,
    relevance: 10
  };
  const EXPRESSIONS = [
    {
      // verbatim string
      className: 'string',
      begin: '"""',
      end: '"""',
      relevance: 10
    },
    {
      // string literal or template
      className: 'string',
      begin: '"',
      end: '"',
      contains: [SUBST]
    },
    {
      // character literal
      className: 'string',
      begin: "'",
      end: "'"
    },
    {
      // numeric literal
      className: 'number',
      begin: '#[0-9a-fA-F_]+|\\$[01_]+|[0-9_]+(?:\\.[0-9_](?:[eE][+-]?\\d+)?)?[kMGTPmunpf]?',
      relevance: 0
    }
  ];
  SUBST.contains = EXPRESSIONS;

  return {
    name: 'Ceylon',
    keywords: {
      keyword: KEYWORDS + ' ' + DECLARATION_MODIFIERS,
      meta: DOCUMENTATION
    },
    illegal: '\\$[^01]|#[^0-9a-fA-F]',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.COMMENT('/\\*', '\\*/', {
        contains: ['self']
      }),
      {
        // compiler annotation
        className: 'meta',
        begin: '@[a-z]\\w*(?::"[^"]*")?'
      }
    ].concat(EXPRESSIONS)
  };
}

module.exports = ceylon;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/ceylon.js":
/*!******************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/ceylon.js ***!
  \******************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  // 2.3. Identifiers and keywords
  var KEYWORDS =
    'assembly module package import alias class interface object given value ' +
    'assign void function new of extends satisfies abstracts in out return ' +
    'break continue throw assert dynamic if else switch case for while try ' +
    'catch finally then let this outer super is exists nonempty';
  // 7.4.1 Declaration Modifiers
  var DECLARATION_MODIFIERS =
    'shared abstract formal default actual variable late native deprecated' +
    'final sealed annotation suppressWarnings small';
  // 7.4.2 Documentation
  var DOCUMENTATION =
    'doc by license see throws tagged';
  var SUBST = {
    className: 'subst', excludeBegin: true, excludeEnd: true,
    begin: /``/, end: /``/,
    keywords: KEYWORDS,
    relevance: 10
  };
  var EXPRESSIONS = [
    {
      // verbatim string
      className: 'string',
      begin: '"""',
      end: '"""',
      relevance: 10
    },
    {
      // string literal or template
      className: 'string',
      begin: '"', end: '"',
      contains: [SUBST]
    },
    {
      // character literal
      className: 'string',
      begin: "'",
      end: "'"
    },
    {
      // numeric literal
      className: 'number',
      begin: '#[0-9a-fA-F_]+|\\$[01_]+|[0-9_]+(?:\\.[0-9_](?:[eE][+-]?\\d+)?)?[kMGTPmunpf]?',
      relevance: 0
    }
  ];
  SUBST.contains = EXPRESSIONS;

  return {
    keywords: {
      keyword: KEYWORDS + ' ' + DECLARATION_MODIFIERS,
      meta: DOCUMENTATION
    },
    illegal: '\\$[^01]|#[^0-9a-fA-F]',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.COMMENT('/\\*', '\\*/', {contains: ['self']}),
      {
        // compiler annotation
        className: 'meta',
        begin: '@[a-z]\\w*(?:\\:\"[^\"]*\")?'
      }
    ].concat(EXPRESSIONS)
  };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_ceylon.ef038ad9a4409486bce0.js.map