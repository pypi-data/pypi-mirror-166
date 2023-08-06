"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_csp"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/csp.js":
/*!***************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/csp.js ***!
  \***************************************************************************/
/***/ ((module) => {



module.exports = csp
csp.displayName = 'csp'
csp.aliases = []
function csp(Prism) {
  /**
   * Original by Scott Helme.
   *
   * Reference: https://scotthelme.co.uk/csp-cheat-sheet/
   *
   * Supports the following:
   *  - CSP Level 1
   *  - CSP Level 2
   *  - CSP Level 3
   */
  Prism.languages.csp = {
    directive: {
      pattern: /\b(?:(?:base-uri|form-action|frame-ancestors|plugin-types|referrer|reflected-xss|report-to|report-uri|require-sri-for|sandbox) |(?:block-all-mixed-content|disown-opener|upgrade-insecure-requests)(?: |;)|(?:child|connect|default|font|frame|img|manifest|media|object|script|style|worker)-src )/i,
      alias: 'keyword'
    },
    safe: {
      pattern: /'(?:self|none|strict-dynamic|(?:nonce-|sha(?:256|384|512)-)[a-zA-Z\d+=/]+)'/,
      alias: 'selector'
    },
    unsafe: {
      pattern: /(?:'unsafe-inline'|'unsafe-eval'|'unsafe-hashed-attributes'|\*)/,
      alias: 'function'
    }
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/csp.js":
/*!********************************************!*\
  !*** ./node_modules/refractor/lang/csp.js ***!
  \********************************************/
/***/ ((module) => {



module.exports = csp
csp.displayName = 'csp'
csp.aliases = []
function csp(Prism) {
  /**
   * Original by Scott Helme.
   *
   * Reference: https://scotthelme.co.uk/csp-cheat-sheet/
   *
   * Supports the following:
   *  - https://www.w3.org/TR/CSP1/
   *  - https://www.w3.org/TR/CSP2/
   *  - https://www.w3.org/TR/CSP3/
   */
  ;(function (Prism) {
    /**
     * @param {string} source
     * @returns {RegExp}
     */
    function value(source) {
      return RegExp(
        /([ \t])/.source + '(?:' + source + ')' + /(?=[\s;]|$)/.source,
        'i'
      )
    }
    Prism.languages.csp = {
      directive: {
        pattern:
          /(^|[\s;])(?:base-uri|block-all-mixed-content|(?:child|connect|default|font|frame|img|manifest|media|object|prefetch|script|style|worker)-src|disown-opener|form-action|frame-(?:ancestors|options)|input-protection(?:-(?:clip|selectors))?|navigate-to|plugin-types|policy-uri|referrer|reflected-xss|report-(?:to|uri)|require-sri-for|sandbox|(?:script|style)-src-(?:attr|elem)|upgrade-insecure-requests)(?=[\s;]|$)/i,
        lookbehind: true,
        alias: 'property'
      },
      scheme: {
        pattern: value(/[a-z][a-z0-9.+-]*:/.source),
        lookbehind: true
      },
      none: {
        pattern: value(/'none'/.source),
        lookbehind: true,
        alias: 'keyword'
      },
      nonce: {
        pattern: value(/'nonce-[-+/\w=]+'/.source),
        lookbehind: true,
        alias: 'number'
      },
      hash: {
        pattern: value(/'sha(?:256|384|512)-[-+/\w=]+'/.source),
        lookbehind: true,
        alias: 'number'
      },
      host: {
        pattern: value(
          /[a-z][a-z0-9.+-]*:\/\/[^\s;,']*/.source +
            '|' +
            /\*[^\s;,']*/.source +
            '|' +
            /[a-z0-9-]+(?:\.[a-z0-9-]+)+(?::[\d*]+)?(?:\/[^\s;,']*)?/.source
        ),
        lookbehind: true,
        alias: 'url',
        inside: {
          important: /\*/
        }
      },
      keyword: [
        {
          pattern: value(/'unsafe-[a-z-]+'/.source),
          lookbehind: true,
          alias: 'unsafe'
        },
        {
          pattern: value(/'[a-z-]+'/.source),
          lookbehind: true,
          alias: 'safe'
        }
      ],
      punctuation: /;/
    }
  })(Prism)
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_csp.1a7661a2b0bae637924a.js.map