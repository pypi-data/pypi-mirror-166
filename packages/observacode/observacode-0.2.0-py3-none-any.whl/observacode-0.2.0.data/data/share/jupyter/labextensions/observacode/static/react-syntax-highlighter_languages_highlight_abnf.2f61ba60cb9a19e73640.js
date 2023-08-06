(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_abnf"],{

/***/ "./node_modules/highlight.js/lib/languages/abnf.js":
/*!*********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/abnf.js ***!
  \*********************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: Augmented Backus-Naur Form
Author: Alex McKibben <alex@nullscope.net>
Website: https://tools.ietf.org/html/rfc5234
Audit: 2020
*/

/** @type LanguageFn */
function abnf(hljs) {
  const regexes = {
    ruleDeclaration: /^[a-zA-Z][a-zA-Z0-9-]*/,
    unexpectedChars: /[!@#$^&',?+~`|:]/
  };

  const keywords = [
    "ALPHA",
    "BIT",
    "CHAR",
    "CR",
    "CRLF",
    "CTL",
    "DIGIT",
    "DQUOTE",
    "HEXDIG",
    "HTAB",
    "LF",
    "LWSP",
    "OCTET",
    "SP",
    "VCHAR",
    "WSP"
  ];

  const commentMode = hljs.COMMENT(/;/, /$/);

  const terminalBinaryMode = {
    className: "symbol",
    begin: /%b[0-1]+(-[0-1]+|(\.[0-1]+)+){0,1}/
  };

  const terminalDecimalMode = {
    className: "symbol",
    begin: /%d[0-9]+(-[0-9]+|(\.[0-9]+)+){0,1}/
  };

  const terminalHexadecimalMode = {
    className: "symbol",
    begin: /%x[0-9A-F]+(-[0-9A-F]+|(\.[0-9A-F]+)+){0,1}/
  };

  const caseSensitivityIndicatorMode = {
    className: "symbol",
    begin: /%[si]/
  };

  const ruleDeclarationMode = {
    className: "attribute",
    begin: concat(regexes.ruleDeclaration, /(?=\s*=)/)
  };

  return {
    name: 'Augmented Backus-Naur Form',
    illegal: regexes.unexpectedChars,
    keywords: keywords,
    contains: [
      ruleDeclarationMode,
      commentMode,
      terminalBinaryMode,
      terminalDecimalMode,
      terminalHexadecimalMode,
      caseSensitivityIndicatorMode,
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = abnf;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/abnf.js":
/*!****************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/abnf.js ***!
  \****************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
    var regexes = {
        ruleDeclaration: "^[a-zA-Z][a-zA-Z0-9-]*",
        unexpectedChars: "[!@#$^&',?+~`|:]"
    };

    var keywords = [
        "ALPHA",
        "BIT",
        "CHAR",
        "CR",
        "CRLF",
        "CTL",
        "DIGIT",
        "DQUOTE",
        "HEXDIG",
        "HTAB",
        "LF",
        "LWSP",
        "OCTET",
        "SP",
        "VCHAR",
        "WSP"
    ];

    var commentMode = hljs.COMMENT(";", "$");

    var terminalBinaryMode = {
        className: "symbol",
        begin: /%b[0-1]+(-[0-1]+|(\.[0-1]+)+){0,1}/
    };

    var terminalDecimalMode = {
        className: "symbol",
        begin: /%d[0-9]+(-[0-9]+|(\.[0-9]+)+){0,1}/
    };

    var terminalHexadecimalMode = {
        className: "symbol",
        begin: /%x[0-9A-F]+(-[0-9A-F]+|(\.[0-9A-F]+)+){0,1}/,
    };

    var caseSensitivityIndicatorMode = {
        className: "symbol",
        begin: /%[si]/
    };

    var ruleDeclarationMode = {
        begin: regexes.ruleDeclaration + '\\s*=',
        returnBegin: true,
        end: /=/,
        relevance: 0,
        contains: [{className: "attribute", begin: regexes.ruleDeclaration}]
    };

    return {
      illegal: regexes.unexpectedChars,
      keywords: keywords.join(" "),
      contains: [
          ruleDeclarationMode,
          commentMode,
          terminalBinaryMode,
          terminalDecimalMode,
          terminalHexadecimalMode,
          caseSensitivityIndicatorMode,
          hljs.QUOTE_STRING_MODE,
          hljs.NUMBER_MODE
      ]
    };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_abnf.2f61ba60cb9a19e73640.js.map