"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_refractor_io"],{

/***/ "./node_modules/react-code-blocks/node_modules/refractor/lang/io.js":
/*!**************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/refractor/lang/io.js ***!
  \**************************************************************************/
/***/ ((module) => {



module.exports = io
io.displayName = 'io'
io.aliases = []
function io(Prism) {
  Prism.languages.io = {
    comment: [
      {
        pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,
        lookbehind: true
      },
      {
        pattern: /(^|[^\\])\/\/.*/,
        lookbehind: true
      },
      {
        pattern: /(^|[^\\])#.*/,
        lookbehind: true
      }
    ],
    'triple-quoted-string': {
      pattern: /"""(?:\\[\s\S]|(?!""")[^\\])*"""/,
      greedy: true,
      alias: 'string'
    },
    string: {
      pattern: /"(?:\\.|[^\\\r\n"])*"/,
      greedy: true
    },
    keyword: /\b(?:activate|activeCoroCount|asString|block|break|catch|clone|collectGarbage|compileString|continue|do|doFile|doMessage|doString|else|elseif|exit|for|foreach|forward|getSlot|getEnvironmentVariable|hasSlot|if|ifFalse|ifNil|ifNilEval|ifTrue|isActive|isNil|isResumable|list|message|method|parent|pass|pause|perform|performWithArgList|print|println|proto|raise|raiseResumable|removeSlot|resend|resume|schedulerSleepSeconds|self|sender|setSchedulerSleepSeconds|setSlot|shallowCopy|slotNames|super|system|then|thisBlock|thisContext|call|try|type|uniqueId|updateSlot|wait|while|write|yield)\b/,
    builtin: /\b(?:Array|AudioDevice|AudioMixer|Block|Box|Buffer|CFunction|CGI|Color|Curses|DBM|DNSResolver|DOConnection|DOProxy|DOServer|Date|Directory|Duration|DynLib|Error|Exception|FFT|File|Fnmatch|Font|Future|GL|GLE|GLScissor|GLU|GLUCylinder|GLUQuadric|GLUSphere|GLUT|Host|Image|Importer|LinkList|List|Lobby|Locals|MD5|MP3Decoder|MP3Encoder|Map|Message|Movie|Notification|Number|Object|OpenGL|Point|Protos|Regex|SGML|SGMLElement|SGMLParser|SQLite|Server|Sequence|ShowMessage|SleepyCat|SleepyCatCursor|Socket|SocketManager|Sound|Soup|Store|String|Tree|UDPSender|UPDReceiver|URL|User|Warning|WeakLink|Random|BigNum|Sequence)\b/,
    boolean: /\b(?:true|false|nil)\b/,
    number: /\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e-?\d+)?/i,
    operator: /[=!*/%+-^&|]=|>>?=?|<<?=?|:?:?=|\+\+?|--?|\*\*?|\/\/?|%|\|\|?|&&?|(\b(?:return|and|or|not)\b)|@@?|\?\??|\.\./,
    punctuation: /[{}[\];(),.:]/
  }
}


/***/ }),

/***/ "./node_modules/refractor/lang/io.js":
/*!*******************************************!*\
  !*** ./node_modules/refractor/lang/io.js ***!
  \*******************************************/
/***/ ((module) => {



module.exports = io
io.displayName = 'io'
io.aliases = []
function io(Prism) {
  Prism.languages.io = {
    comment: {
      pattern: /(^|[^\\])(?:\/\*[\s\S]*?(?:\*\/|$)|\/\/.*|#.*)/,
      lookbehind: true,
      greedy: true
    },
    'triple-quoted-string': {
      pattern: /"""(?:\\[\s\S]|(?!""")[^\\])*"""/,
      greedy: true,
      alias: 'string'
    },
    string: {
      pattern: /"(?:\\.|[^\\\r\n"])*"/,
      greedy: true
    },
    keyword:
      /\b(?:activate|activeCoroCount|asString|block|break|call|catch|clone|collectGarbage|compileString|continue|do|doFile|doMessage|doString|else|elseif|exit|for|foreach|forward|getEnvironmentVariable|getSlot|hasSlot|if|ifFalse|ifNil|ifNilEval|ifTrue|isActive|isNil|isResumable|list|message|method|parent|pass|pause|perform|performWithArgList|print|println|proto|raise|raiseResumable|removeSlot|resend|resume|schedulerSleepSeconds|self|sender|setSchedulerSleepSeconds|setSlot|shallowCopy|slotNames|super|system|then|thisBlock|thisContext|try|type|uniqueId|updateSlot|wait|while|write|yield)\b/,
    builtin:
      /\b(?:Array|AudioDevice|AudioMixer|BigNum|Block|Box|Buffer|CFunction|CGI|Color|Curses|DBM|DNSResolver|DOConnection|DOProxy|DOServer|Date|Directory|Duration|DynLib|Error|Exception|FFT|File|Fnmatch|Font|Future|GL|GLE|GLScissor|GLU|GLUCylinder|GLUQuadric|GLUSphere|GLUT|Host|Image|Importer|LinkList|List|Lobby|Locals|MD5|MP3Decoder|MP3Encoder|Map|Message|Movie|Notification|Number|Object|OpenGL|Point|Protos|Random|Regex|SGML|SGMLElement|SGMLParser|SQLite|Sequence|Server|ShowMessage|SleepyCat|SleepyCatCursor|Socket|SocketManager|Sound|Soup|Store|String|Tree|UDPSender|UPDReceiver|URL|User|Warning|WeakLink)\b/,
    boolean: /\b(?:false|nil|true)\b/,
    number: /\b0x[\da-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e-?\d+)?/i,
    operator:
      /[=!*/%+\-^&|]=|>>?=?|<<?=?|:?:?=|\+\+?|--?|\*\*?|\/\/?|%|\|\|?|&&?|\b(?:and|not|or|return)\b|@@?|\?\??|\.\./,
    punctuation: /[{}[\];(),.:]/
  }
}


/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_io.f3fc51e5fbd0ea7223cd.js.map