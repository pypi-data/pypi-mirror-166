"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_keyman"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/keyman.js":
/*!******************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/keyman.js ***!
  \******************************************************************************/
/***/ ((module) => {



module.exports = keyman
keyman.displayName = 'keyman'
keyman.aliases = []
function keyman(Prism) {
  Prism.languages.keyman = {
    comment: /\bc\s.*/i,
    function: /\[\s*(?:(?:CTRL|SHIFT|ALT|LCTRL|RCTRL|LALT|RALT|CAPS|NCAPS)\s+)*(?:[TKU]_[\w?]+|".+?"|'.+?')\s*\]/i,
    // virtual key
    string: /("|').*?\1/,
    bold: [
      // header statements, system stores and variable system stores
      /&(?:baselayout|bitmap|capsononly|capsalwaysoff|shiftfreescaps|copyright|ethnologuecode|hotkey|includecodes|keyboardversion|kmw_embedcss|kmw_embedjs|kmw_helpfile|kmw_helptext|kmw_rtl|language|layer|layoutfile|message|mnemoniclayout|name|oldcharposmatching|platform|targets|version|visualkeyboard|windowslanguages)\b/i,
      /\b(?:bitmap|bitmaps|caps on only|caps always off|shift frees caps|copyright|hotkey|language|layout|message|name|version)\b/i
    ],
    keyword: /\b(?:any|baselayout|beep|call|context|deadkey|dk|if|index|layer|notany|nul|outs|platform|return|reset|save|set|store|use)\b/i,
    // rule keywords
    atrule: /\b(?:ansi|begin|unicode|group|using keys|match|nomatch)\b/i,
    // structural keywords
    number: /\b(?:U\+[\dA-F]+|d\d+|x[\da-f]+|\d+)\b/i,
    // U+####, x###, d### characters and numbers
    operator: /[+>\\,()]/,
    tag: /\$(?:keyman|kmfl|weaver|keymanweb|keymanonly):/i // prefixes
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/keyman.js":
/*!***********************************************!*\
  !*** ./node_modules/refractor/lang/keyman.js ***!
  \***********************************************/
/***/ ((module) => {



module.exports = keyman
keyman.displayName = 'keyman'
keyman.aliases = []
function keyman(Prism) {
  Prism.languages.keyman = {
    comment: {
      pattern: /\bc .*/i,
      greedy: true
    },
    string: {
      pattern: /"[^"\r\n]*"|'[^'\r\n]*'/,
      greedy: true
    },
    'virtual-key': {
      pattern:
        /\[\s*(?:(?:ALT|CAPS|CTRL|LALT|LCTRL|NCAPS|RALT|RCTRL|SHIFT)\s+)*(?:[TKU]_[\w?]+|[A-E]\d\d?|"[^"\r\n]*"|'[^'\r\n]*')\s*\]/i,
      greedy: true,
      alias: 'function' // alias for styles
    },
    // https://help.keyman.com/developer/language/guide/headers
    'header-keyword': {
      pattern: /&\w+/,
      alias: 'bold' // alias for styles
    },
    'header-statement': {
      pattern:
        /\b(?:bitmap|bitmaps|caps always off|caps on only|copyright|hotkey|language|layout|message|name|shift frees caps|version)\b/i,
      alias: 'bold' // alias for styles
    },
    'rule-keyword': {
      pattern:
        /\b(?:any|baselayout|beep|call|context|deadkey|dk|if|index|layer|notany|nul|outs|platform|reset|return|save|set|store|use)\b/i,
      alias: 'keyword'
    },
    'structural-keyword': {
      pattern: /\b(?:ansi|begin|group|match|nomatch|unicode|using keys)\b/i,
      alias: 'keyword'
    },
    'compile-target': {
      pattern: /\$(?:keyman|keymanonly|keymanweb|kmfl|weaver):/i,
      alias: 'property'
    },
    // U+####, x###, d### characters and numbers
    number: /\b(?:U\+[\dA-F]+|d\d+|x[\da-f]+|\d+)\b/i,
    operator: /[+>\\$]|\.\./,
    punctuation: /[()=,]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_keyman.8f11fa741d0e587c4f18.js.map