(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_vbscriptHtml"],{

/***/ "./node_modules/highlight.js/lib/languages/vbscript-html.js":
/*!******************************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/vbscript-html.js ***!
  \******************************************************************/
/***/ ((module) => {

/*
Language: VBScript in HTML
Requires: xml.js, vbscript.js
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Description: "Bridge" language defining fragments of VBScript in HTML within <% .. %>
Website: https://en.wikipedia.org/wiki/VBScript
Category: scripting
*/

function vbscriptHtml(hljs) {
  return {
    name: 'VBScript in HTML',
    subLanguage: 'xml',
    contains: [
      {
        begin: '<%',
        end: '%>',
        subLanguage: 'vbscript'
      }
    ]
  };
}

module.exports = vbscriptHtml;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/vbscript-html.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/vbscript-html.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  return {
    subLanguage: 'xml',
    contains: [
      {
        begin: '<%', end: '%>',
        subLanguage: 'vbscript'
      }
    ]
  };
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_vbscriptHtml.022935cbf6d73cb5196d.js.map