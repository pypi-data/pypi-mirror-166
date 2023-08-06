var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/observacode":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_d3-scale_src_sequential_js"), __webpack_require__.e("vendors-node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_mui_mat-39df4f"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_yjs"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_8f22"), __webpack_require__.e("lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_d3-scale_src_sequential_js"), __webpack_require__.e("vendors-node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_mui_mat-39df4f"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_yjs"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_8f22"), __webpack_require__.e("lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./style": () => {
		return __webpack_require__.e("style_index_js").then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/create fake namespace object */
/******/ 	(() => {
/******/ 		var getProto = Object.getPrototypeOf ? (obj) => (Object.getPrototypeOf(obj)) : (obj) => (obj.__proto__);
/******/ 		var leafPrototypes;
/******/ 		// create a fake namespace object
/******/ 		// mode & 1: value is a module id, require it
/******/ 		// mode & 2: merge all properties of value into the ns
/******/ 		// mode & 4: return value when already ns object
/******/ 		// mode & 16: return value when it's Promise-like
/******/ 		// mode & 8|1: behave like require
/******/ 		__webpack_require__.t = function(value, mode) {
/******/ 			if(mode & 1) value = this(value);
/******/ 			if(mode & 8) return value;
/******/ 			if(typeof value === 'object' && value) {
/******/ 				if((mode & 4) && value.__esModule) return value;
/******/ 				if((mode & 16) && typeof value.then === 'function') return value;
/******/ 			}
/******/ 			var ns = Object.create(null);
/******/ 			__webpack_require__.r(ns);
/******/ 			var def = {};
/******/ 			leafPrototypes = leafPrototypes || [null, getProto({}), getProto([]), getProto(getProto)];
/******/ 			for(var current = mode & 2 && value; typeof current == 'object' && !~leafPrototypes.indexOf(current); current = getProto(current)) {
/******/ 				Object.getOwnPropertyNames(current).forEach((key) => (def[key] = () => (value[key])));
/******/ 			}
/******/ 			def['default'] = () => (value);
/******/ 			__webpack_require__.d(ns, def);
/******/ 			return ns;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js":"0073d9f556e2aacdb658","vendors-node_modules_d3-scale_src_sequential_js":"4994df1a51bf931a4ada","vendors-node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_mui_mat-39df4f":"1956b7a09666ed08cbfe","webpack_sharing_consume_default_react":"4860292e9b6a1038e34a","webpack_sharing_consume_default_yjs":"dbfc0f57c120605703e7","webpack_sharing_consume_default_emotion_react_emotion_react-_8f22":"8ebc564eac2b1aacb2fa","lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4":"407c28f95fd7a88adc01","style_index_js":"7e5448bd989d1d9d4271","vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9":"29b780ba4851f1fa7d3f","vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js":"fb48a32f0ad0f0fdf718","node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_memoize_dist_emotion-m-00c0260":"35932ec095d2f2093fec","vendors-node_modules_emotion_styled_dist_emotion-styled_browser_esm_js":"5048569ffed16c3ca3c5","webpack_sharing_consume_default_emotion_react_emotion_react-_1cec":"9f5ced690e461f77388b","node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_memoize_dist_emotion-m-00c0261":"b5a6070243a46d97f7d7","vendors-node_modules_d3_src_index_js":"5c8f35a7e0e4cbeb7e21","node_modules_levenshtein-edit-distance_index_js":"aa92ce9aa78d05d2d564","vendors-node_modules_react-code-blocks_dist_react-code-blocks_esm_js":"eba33c910b2be35da16f","webpack_sharing_consume_default_react-syntax-highlighter_react-syntax-highlighter":"98959b96c6a2a6d0dbbf","node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_react-is_index_js":"80afb95048a19f27fda8","vendors-node_modules_babel_runtime_helpers_esm_asyncToGenerator_js-node_modules_babel_runtime-4278be":"6308ab38a3d429439be1","react-syntax-highlighter/refractor-core-import":"c5303c4f7853901c5291","react-syntax-highlighter_languages_refractor_mel":"4f78ee0a4e32182b9638","vendors-node_modules_react-code-blocks_node_modules_refractor_lang_opencl_js":"26fe317a12efdd12731d","react-syntax-highlighter_languages_refractor_vim":"da7a874677a030b63049","react-syntax-highlighter_languages_refractor_markdown":"5460b896aa4ce3874414","react-syntax-highlighter_languages_refractor_gherkin":"143a4a3492b71b406adf","react-syntax-highlighter/refractor-import":"25549795363acc65c38f","react-syntax-highlighter_languages_highlight_isbl":"517d5e8e85a4e6607b39","react-syntax-highlighter_languages_highlight_mathematica":"c1aba4e7bd92caa266a2","react-syntax-highlighter_languages_highlight_oneC":"5e2d8b44fda78e549b05","react-syntax-highlighter_languages_highlight_gml":"dbea868ac314ea8964dd","react-syntax-highlighter/lowlight-import":"c8127f7e2ba48b3903c3","react-syntax-highlighter_languages_highlight_sqf":"898b549daed5f2b6bc87","vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_powershell_js":"14e958901a677a50ba57","vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_maxima_js":"b1e42a704f63a06e6ea6","react-syntax-highlighter_languages_highlight_pgsql":"706fda8f7e219fc29b03","react-syntax-highlighter_languages_highlight_x86asm":"af2c62a66fecefa20a0a","react-syntax-highlighter_languages_highlight_mel":"34d68dab710132e56cb5","react-syntax-highlighter_languages_highlight_gauss":"3bfbb1f07ceb67372a1e","react-syntax-highlighter_languages_highlight_stata":"632733cb576e3e125f61","vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_sql_js":"9b1360207748e7e1c3d2","vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_lsl_js":"ff3777429ea6aa732b21","react-syntax-highlighter_languages_highlight_vim":"9f9f59d1e9f13ccec958","vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_autoit_js":"59dec43e0002967de781","vendors-node_modules_babel_runtime_helpers_esm_assertThisInitialized_js-node_modules_babel_ru-3f0775":"518e527bec4e11f7e691","vendors-node_modules_refractor_lang_csharp_js":"621cc4a722afcec84234","vendors-node_modules_refractor_lang_php_js":"548ad94e5fb93f690d22","vendors-node_modules_refractor_core_js":"6971a150a10e9cefec8a","vendors-node_modules_refractor_lang_mel_js":"8e93f7347b696f3f41e3","react-syntax-highlighter_languages_refractor_opencl":"7ed326ba1001cac527c0","vendors-node_modules_refractor_lang_vim_js":"42145d240e9ea50a8c44","vendors-node_modules_refractor_lang_markdown_js":"cad18d7e18d9c2add7f7","vendors-node_modules_refractor_lang_sas_js":"77c978cfa0c350dcc8e5","vendors-node_modules_refractor_lang_gherkin_js":"239f0e8214b798e2154d","vendors-node_modules_refractor_lang_haml_js":"b656de0daee77205c915","vendors-node_modules_refractor_lang_textile_js":"37067c82684a568e266e","vendors-node_modules_refractor_lang_bash_js":"ba8d331200e1801a1cf2","vendors-node_modules_refractor_index_js":"38c222a8178d14df4172","vendors-node_modules_highlight_js_lib_languages_mathematica_js":"b03dcc73f9ec685caa12","vendors-node_modules_highlight_js_lib_languages_isbl_js":"ff7377c037821eb02653","vendors-node_modules_lowlight_lib_core_js":"41e9ca2839ed850e1594","vendors-node_modules_highlight_js_lib_languages_1c_js":"94cdc5b61299f3d9bbcf","vendors-node_modules_highlight_js_lib_languages_gml_js":"1b70e8bf68656622b4bc","vendors-node_modules_highlight_js_lib_languages_sqf_js":"948b34ee1b1458d5f0df","react-syntax-highlighter_languages_highlight_maxima":"e57112e8b71cec8e2c03","vendors-node_modules_highlight_js_lib_languages_pgsql_js":"e0a0c28c364368e730bc","vendors-node_modules_highlight_js_lib_languages_x86asm_js":"0e47a4aea4398d61987e","vendors-node_modules_highlight_js_lib_languages_swift_js":"8baf278f0586375d901c","vendors-node_modules_highlight_js_lib_languages_mel_js":"42f867b2ef1ebaa24015","vendors-node_modules_highlight_js_lib_languages_stata_js":"a60b492a55391db26275","vendors-node_modules_highlight_js_lib_languages_gauss_js":"9842f5cf9974f10a5676","vendors-node_modules_highlight_js_lib_languages_typescript_js":"50892079ede7aaab2091","vendors-node_modules_highlight_js_lib_languages_arduino_js":"a9cda5fd5847c83e234e","vendors-node_modules_highlight_js_lib_languages_javascript_js":"5e0cc5bbdfd7bff388c1","vendors-node_modules_highlight_js_lib_languages_less_js":"f6b1b0b9ee282092b0da","react-syntax-highlighter_languages_highlight_lsl":"5b796f4763d624aec13f","react-syntax-highlighter_languages_highlight_sql":"dbfe05a98e4dee0815ab","vendors-node_modules_highlight_js_lib_languages_css_js":"345af41bf0faaefbf84f","vendors-node_modules_highlight_js_lib_languages_scss_js":"dcac8d827ed6d0263f09","vendors-node_modules_highlight_js_lib_languages_stylus_js":"912c6fe4c585df0f06a9","vendors-node_modules_highlight_js_lib_languages_stan_js":"970500d37c9dec3985f7","vendors-node_modules_highlight_js_lib_languages_vim_js":"67649b04f78c1b5b5fe7","vendors-node_modules_highlight_js_lib_languages_livecodeserver_js":"e000c9153530d5e9f466","vendors-node_modules_highlight_js_lib_languages_cpp_js":"31886e85da36dfb25c49","vendors-node_modules_react-syntax-highlighter_dist_esm_index_js":"f236015a734999d0ffd3","node_modules_babel_runtime_helpers_esm_assertThisInitialized_js-node_modules_babel_runtime_he-99d734":"871ea0e6ba2198a33c49","vendors-node_modules_y-websocket_src_y-websocket_js":"43275ff1302164fae23b","react-syntax-highlighter_languages_highlight_abnf":"2f61ba60cb9a19e73640","react-syntax-highlighter_languages_highlight_accesslog":"75038b6106d1a1514d22","react-syntax-highlighter_languages_highlight_actionscript":"90624f58a49439ae477c","react-syntax-highlighter_languages_highlight_ada":"4cb96aa7ce4528316268","react-syntax-highlighter_languages_highlight_angelscript":"83bafea67b82472d1bbf","react-syntax-highlighter_languages_highlight_apache":"ac54ebfd9c9bf6792c4e","react-syntax-highlighter_languages_highlight_applescript":"4b50d9bfbdd7bffb301d","react-syntax-highlighter_languages_highlight_arcade":"65401dacf6af8fda71fd","react-syntax-highlighter_languages_highlight_arduino":"875a8d1d3bd0765686af","react-syntax-highlighter_languages_highlight_armasm":"534787656f48e06cf4af","react-syntax-highlighter_languages_highlight_asciidoc":"b01a75fcd5a9b04bd68e","react-syntax-highlighter_languages_highlight_aspectj":"7948f989affb8fb45495","react-syntax-highlighter_languages_highlight_autohotkey":"18142a724abe58040754","react-syntax-highlighter_languages_highlight_autoit":"22afcdb79c0552931e2f","react-syntax-highlighter_languages_highlight_avrasm":"4df4d86e241701ed125b","react-syntax-highlighter_languages_highlight_awk":"c86bfbd62c69639be2c8","react-syntax-highlighter_languages_highlight_axapta":"8a77d41e712e71825490","react-syntax-highlighter_languages_highlight_bash":"1dd290e6ed0f3f198e4b","react-syntax-highlighter_languages_highlight_basic":"73996628c113fb87d93a","react-syntax-highlighter_languages_highlight_bnf":"27a9b94e0f4f9c9aac78","react-syntax-highlighter_languages_highlight_brainfuck":"d08b8a499446dc9598e7","react-syntax-highlighter_languages_highlight_cal":"8d88500eb7db489b9e08","react-syntax-highlighter_languages_highlight_capnproto":"9994e8fd57b5ca203805","react-syntax-highlighter_languages_highlight_ceylon":"ef038ad9a4409486bce0","react-syntax-highlighter_languages_highlight_clean":"0f6bdc15bc8681dfd105","react-syntax-highlighter_languages_highlight_clojureRepl":"1d89b248fc41a50e9884","react-syntax-highlighter_languages_highlight_clojure":"6e639fbfa807b15a22e3","react-syntax-highlighter_languages_highlight_cmake":"f3b12eead0268c85245d","react-syntax-highlighter_languages_highlight_coffeescript":"f22cee9c7c4e883f0c69","react-syntax-highlighter_languages_highlight_coq":"27599ae7b7d0325f4d87","react-syntax-highlighter_languages_highlight_cos":"38994ed906741becb70a","react-syntax-highlighter_languages_highlight_cpp":"607faf94b4f1c2bc9625","react-syntax-highlighter_languages_highlight_crmsh":"a938dc01a7cbec5a1d57","react-syntax-highlighter_languages_highlight_crystal":"6afba921448367cfbab2","react-syntax-highlighter_languages_highlight_csp":"c258156b46a06cb74218","react-syntax-highlighter_languages_highlight_css":"5bf46a96550697d6ba31","react-syntax-highlighter_languages_highlight_d":"df0b323357cd9887fc0c","react-syntax-highlighter_languages_highlight_dart":"0456df0e4ba99f7f4649","react-syntax-highlighter_languages_highlight_delphi":"904db097e411208a567d","react-syntax-highlighter_languages_highlight_diff":"7c069d99505ce42f56cc","react-syntax-highlighter_languages_highlight_django":"f62a055af7f7bb736fcf","react-syntax-highlighter_languages_highlight_dns":"b537290c76e87df2881b","react-syntax-highlighter_languages_highlight_dockerfile":"96033dcafc4724d05d91","react-syntax-highlighter_languages_highlight_dos":"cd13bf236155a72736b0","react-syntax-highlighter_languages_highlight_dsconfig":"1b5ff9dcb6ace6440b67","react-syntax-highlighter_languages_highlight_dts":"2a07905aa8d4761af77d","react-syntax-highlighter_languages_highlight_dust":"e6106f7193554db4bb7a","react-syntax-highlighter_languages_highlight_ebnf":"527ee3001339b43d7b59","react-syntax-highlighter_languages_highlight_elixir":"ae7d532ca45e17723779","react-syntax-highlighter_languages_highlight_elm":"02714a5615b5fe5dcd17","react-syntax-highlighter_languages_highlight_erb":"acc97660f28e669341c2","react-syntax-highlighter_languages_highlight_erlangRepl":"b4b027f45b337165f2e2","react-syntax-highlighter_languages_highlight_erlang":"2f6874972a5363a0541e","react-syntax-highlighter_languages_highlight_excel":"0080236822819fe2ffa3","react-syntax-highlighter_languages_highlight_fix":"2e60773be35b3ad968b3","react-syntax-highlighter_languages_highlight_flix":"248ec627b16134be8399","react-syntax-highlighter_languages_highlight_fortran":"4942ffdb78c8d7b26d60","react-syntax-highlighter_languages_highlight_fsharp":"428a8eb236b2e48fec9c","react-syntax-highlighter_languages_highlight_gams":"369c5f0bbf640890f888","react-syntax-highlighter_languages_highlight_gcode":"463a516484b6382f513a","react-syntax-highlighter_languages_highlight_gherkin":"96e4499314b9acbe6e3e","react-syntax-highlighter_languages_highlight_glsl":"f1a8b15692def454749f","react-syntax-highlighter_languages_highlight_go":"e41518b78d499295be32","react-syntax-highlighter_languages_highlight_golo":"b6fe488e56b9ca0e2a8b","react-syntax-highlighter_languages_highlight_gradle":"5eecb768d80837cbb627","react-syntax-highlighter_languages_highlight_groovy":"48fef13ef3cbe0e501fa","react-syntax-highlighter_languages_highlight_haml":"c147b68d196eb6baa9f3","react-syntax-highlighter_languages_highlight_handlebars":"b8a6ecab061b5f45e946","react-syntax-highlighter_languages_highlight_haskell":"3ea401059cc8b41b1377","react-syntax-highlighter_languages_highlight_haxe":"7681b6b24326699e17bc","react-syntax-highlighter_languages_highlight_hsp":"eadb34122d0ea68c34e0","react-syntax-highlighter_languages_highlight_htmlbars":"7a232ade5b2e473adeea","react-syntax-highlighter_languages_highlight_http":"9c7fc8501ed524e4f363","react-syntax-highlighter_languages_highlight_hy":"db5901c43abd481d0f08","react-syntax-highlighter_languages_highlight_inform7":"e9fb8a986bf555a384fa","react-syntax-highlighter_languages_highlight_ini":"32866a0e1c52823a12f7","react-syntax-highlighter_languages_highlight_irpf90":"cf5e17ff1a78d0ca548b","react-syntax-highlighter_languages_highlight_java":"0ded6f12cbc07a161cba","react-syntax-highlighter_languages_highlight_javascript":"d6947fc4f17cba911d10","react-syntax-highlighter_languages_highlight_jbossCli":"6035c422a6f679a7bd4e","react-syntax-highlighter_languages_highlight_json":"1006356719ef2debcb22","react-syntax-highlighter_languages_highlight_juliaRepl":"230fcd50e7f8f0ca674c","react-syntax-highlighter_languages_highlight_julia":"2c2cb37b206b28fb4d5a","react-syntax-highlighter_languages_highlight_kotlin":"2eefcf73c6ca1e7cb6e4","react-syntax-highlighter_languages_highlight_lasso":"16b64d7bd467bf448a2d","react-syntax-highlighter_languages_highlight_ldif":"227dd2924d2ecd4a4a36","react-syntax-highlighter_languages_highlight_leaf":"3a4c7ab8a942df8ba512","react-syntax-highlighter_languages_highlight_less":"41b4c21ef4689bbf6e29","react-syntax-highlighter_languages_highlight_lisp":"09b2d72dc2d0a629bb2e","react-syntax-highlighter_languages_highlight_livecodeserver":"154bed6211088e2d6853","react-syntax-highlighter_languages_highlight_livescript":"012fcfbca4e1de9d10ca","react-syntax-highlighter_languages_highlight_llvm":"4c0d08d33196999cbbb3","react-syntax-highlighter_languages_highlight_lua":"b4b53b32f679ac0455a8","react-syntax-highlighter_languages_highlight_makefile":"5a1e0473d5b97fa7c041","react-syntax-highlighter_languages_highlight_markdown":"8b65723a7e45f6fb4fc3","react-syntax-highlighter_languages_highlight_matlab":"16132a14e1929468336d","react-syntax-highlighter_languages_highlight_mercury":"d9d29f59dd63fde3f740","react-syntax-highlighter_languages_highlight_mipsasm":"bbae6183099d30e16f07","react-syntax-highlighter_languages_highlight_mizar":"4e39c0355810977c7621","react-syntax-highlighter_languages_highlight_mojolicious":"d7988ae6c54f3059ba54","react-syntax-highlighter_languages_highlight_monkey":"10cec0cfc4052694d775","react-syntax-highlighter_languages_highlight_moonscript":"b4af7ce114954cf761df","react-syntax-highlighter_languages_highlight_n1ql":"478c9b743d21f1d1439f","react-syntax-highlighter_languages_highlight_nginx":"e10492085bda38c252f3","react-syntax-highlighter_languages_highlight_nix":"041d119c076ca563c296","react-syntax-highlighter_languages_highlight_nsis":"8721f644ca695d8cfa0b","react-syntax-highlighter_languages_highlight_objectivec":"78f7883d976f07f2a2b9","react-syntax-highlighter_languages_highlight_ocaml":"42986e83f46c0e4890be","react-syntax-highlighter_languages_highlight_openscad":"bebd966b0be9746f772d","react-syntax-highlighter_languages_highlight_oxygene":"cfb64f41825730235726","react-syntax-highlighter_languages_highlight_parser3":"5f3d1212d76c7a11be44","react-syntax-highlighter_languages_highlight_perl":"1a6253825797f81ddadc","react-syntax-highlighter_languages_highlight_pf":"dae0c0778be2126cefec","react-syntax-highlighter_languages_highlight_php":"ea55e957228921d41f01","react-syntax-highlighter_languages_highlight_plaintext":"3b6f5b8bb08c4651701b","react-syntax-highlighter_languages_highlight_pony":"b493e9c9bb5220c498e1","react-syntax-highlighter_languages_highlight_powershell":"ede1ad6b38b92eb7f82c","react-syntax-highlighter_languages_highlight_processing":"5c82599ee23d871bb588","react-syntax-highlighter_languages_highlight_profile":"6e1b59c3af932feae2c7","react-syntax-highlighter_languages_highlight_prolog":"715ed425df9793f33a3f","react-syntax-highlighter_languages_highlight_properties":"e8bdbed760bc12a2434b","react-syntax-highlighter_languages_highlight_protobuf":"528e07eaae98431bddd2","react-syntax-highlighter_languages_highlight_puppet":"ab48635054cd7bc9d880","react-syntax-highlighter_languages_highlight_purebasic":"c78f9b78b65fd7af3e38","react-syntax-highlighter_languages_highlight_python":"a00ae04247c379f8a287","react-syntax-highlighter_languages_highlight_q":"c1e04952c2d5dd7f7403","react-syntax-highlighter_languages_highlight_qml":"73017d17b70fcc6b6cbe","react-syntax-highlighter_languages_highlight_r":"cbee399d75ad292b2c35","react-syntax-highlighter_languages_highlight_reasonml":"3ca2d0398c550d64b7ce","react-syntax-highlighter_languages_highlight_rib":"f70aecdb06db2183e4b1","react-syntax-highlighter_languages_highlight_roboconf":"d66f9ceac326ad83f06f","react-syntax-highlighter_languages_highlight_routeros":"86d475ffd5cf69930b64","react-syntax-highlighter_languages_highlight_rsl":"752590960c8f6aae3f66","react-syntax-highlighter_languages_highlight_ruby":"5320f3641ff8156bfa7d","react-syntax-highlighter_languages_highlight_ruleslanguage":"c403a733867988b85424","react-syntax-highlighter_languages_highlight_rust":"c9e382ba2358202f9478","react-syntax-highlighter_languages_highlight_sas":"19b71193e4153c07c2d0","react-syntax-highlighter_languages_highlight_scala":"46fa8e209e73e9e57360","react-syntax-highlighter_languages_highlight_scheme":"130b6be2063ad9c29d8d","react-syntax-highlighter_languages_highlight_scilab":"e35e807d06ef8c3612e6","react-syntax-highlighter_languages_highlight_scss":"95493523e6bcae6a0929","react-syntax-highlighter_languages_highlight_shell":"911e5c60ba09edc54666","react-syntax-highlighter_languages_highlight_smali":"aabdccf88a09fc0b5727","react-syntax-highlighter_languages_highlight_smalltalk":"aefcd727dceaf0276491","react-syntax-highlighter_languages_highlight_sml":"1b35a83d317ebc634ace","react-syntax-highlighter_languages_highlight_stan":"7441949534dbe14e6bff","react-syntax-highlighter_languages_highlight_step21":"dac4b6f80d1640ed0bc5","react-syntax-highlighter_languages_highlight_stylus":"998e5efbab8b96a1cf08","react-syntax-highlighter_languages_highlight_subunit":"74823039d85feeb9d913","react-syntax-highlighter_languages_highlight_swift":"13c96e878afef880e133","react-syntax-highlighter_languages_highlight_taggerscript":"ca38f21a8a308cf41efc","react-syntax-highlighter_languages_highlight_tap":"b4ad2318630e6c87aa45","react-syntax-highlighter_languages_highlight_tcl":"66fc104dd52c3fbc1e3e","react-syntax-highlighter_languages_highlight_thrift":"5b51ce317e2f03e44043","react-syntax-highlighter_languages_highlight_tp":"a11fd5ee1cb15d247d70","react-syntax-highlighter_languages_highlight_twig":"fe8c4b5f7b14eb85140b","react-syntax-highlighter_languages_highlight_typescript":"57d8f9b8ae55bec6e3ca","react-syntax-highlighter_languages_highlight_vala":"57fa26206587772678da","react-syntax-highlighter_languages_highlight_vbnet":"8f3d87442a7e1e3e0cdb","react-syntax-highlighter_languages_highlight_vbscriptHtml":"022935cbf6d73cb5196d","react-syntax-highlighter_languages_highlight_vbscript":"2cb28913d14412359704","react-syntax-highlighter_languages_highlight_verilog":"943eecc5b68b3a002b56","react-syntax-highlighter_languages_highlight_vhdl":"538f4cbc4be97d14b60b","react-syntax-highlighter_languages_highlight_xl":"98aa622e19ed321257a4","react-syntax-highlighter_languages_highlight_xml":"1a53b9d680e516c9bd61","react-syntax-highlighter_languages_highlight_xquery":"9b6772388c188cf866fa","react-syntax-highlighter_languages_highlight_yaml":"67f6bdb3353d0ed9baef","react-syntax-highlighter_languages_highlight_zephir":"cfc74f2876719239d951","react-syntax-highlighter_languages_refractor_abap":"f817602687ce012f66fa","react-syntax-highlighter_languages_refractor_actionscript":"589c58e950c1d93875ef","react-syntax-highlighter_languages_refractor_ada":"86c9ea75db6a08871cc7","react-syntax-highlighter_languages_refractor_apacheconf":"ff1906a966d465f572cb","react-syntax-highlighter_languages_refractor_apl":"d5102373b9973e92144a","react-syntax-highlighter_languages_refractor_applescript":"37fe2b4614b9727ff4cf","react-syntax-highlighter_languages_refractor_arduino":"1102ebb21e47be439c22","react-syntax-highlighter_languages_refractor_arff":"40744a7278f4681b41bf","react-syntax-highlighter_languages_refractor_asciidoc":"2014151274158444a2ef","react-syntax-highlighter_languages_refractor_asm6502":"8e34964aca172d634146","react-syntax-highlighter_languages_refractor_aspnet":"73a6511146b9d8684a88","react-syntax-highlighter_languages_refractor_autohotkey":"ac049c53ae694de27685","react-syntax-highlighter_languages_refractor_autoit":"6e15e87cc956851949d5","react-syntax-highlighter_languages_refractor_bash":"9be978d3c6d356313914","react-syntax-highlighter_languages_refractor_basic":"a63552f6439defb620b9","react-syntax-highlighter_languages_refractor_batch":"bf3b4db37bf71e96576e","react-syntax-highlighter_languages_refractor_bison":"21dc296028f776315c1a","react-syntax-highlighter_languages_refractor_brainfuck":"bbaf0b463e94cfd8c204","react-syntax-highlighter_languages_refractor_bro":"2e7f557e3a23f191d664","react-syntax-highlighter_languages_refractor_c":"796e4cbe1d4d6d6bfd76","react-syntax-highlighter_languages_refractor_clike":"772823cef5392e0444da","react-syntax-highlighter_languages_refractor_clojure":"b73faa68c493cd6a3587","react-syntax-highlighter_languages_refractor_coffeescript":"d79a30d8b94c14151330","react-syntax-highlighter_languages_refractor_cpp":"83e3a5e69f8319362285","react-syntax-highlighter_languages_refractor_crystal":"dd89d8817ed4728c1cda","react-syntax-highlighter_languages_refractor_csharp":"8d063d5fb42eb292fa15","react-syntax-highlighter_languages_refractor_csp":"1a7661a2b0bae637924a","react-syntax-highlighter_languages_refractor_cssExtras":"f2fee95a1b3d95de5457","react-syntax-highlighter_languages_refractor_css":"4f92393722dc3047f1af","react-syntax-highlighter_languages_refractor_d":"5d18730067a7a1eb92e9","react-syntax-highlighter_languages_refractor_dart":"a7af9508692e3ac5c09c","react-syntax-highlighter_languages_refractor_diff":"d80a297b453ca08799a4","react-syntax-highlighter_languages_refractor_django":"a6784c842acca1900945","react-syntax-highlighter_languages_refractor_docker":"46489a7a25106857b5c5","react-syntax-highlighter_languages_refractor_eiffel":"0139820998e06d0e6c0e","react-syntax-highlighter_languages_refractor_elixir":"1aeadaa909f63d1c1e24","react-syntax-highlighter_languages_refractor_elm":"454bc7d196fb8051db6d","react-syntax-highlighter_languages_refractor_erb":"6aaa7256ff7ddb43910f","react-syntax-highlighter_languages_refractor_erlang":"6b75cec65f5dee2969fc","react-syntax-highlighter_languages_refractor_flow":"dea4cf8227efdf1bb242","react-syntax-highlighter_languages_refractor_fortran":"390559d64e77f66f56ae","react-syntax-highlighter_languages_refractor_fsharp":"09c8da0dcaf0e4129f70","react-syntax-highlighter_languages_refractor_gedcom":"0c066b29ec9adeb4d987","react-syntax-highlighter_languages_refractor_git":"e1bf9ca724551e4e1926","react-syntax-highlighter_languages_refractor_glsl":"c7b73637e3aa94f5d34d","react-syntax-highlighter_languages_refractor_go":"1df854cf0dbf13d03a1b","react-syntax-highlighter_languages_refractor_graphql":"d07ac4520f8175b7bc41","react-syntax-highlighter_languages_refractor_groovy":"8c20b4ff7f63fb3d4a01","react-syntax-highlighter_languages_refractor_haml":"fec0432255791470c14b","react-syntax-highlighter_languages_refractor_handlebars":"bc0cd51d4821391cf6cb","react-syntax-highlighter_languages_refractor_haskell":"79669c20970ac2e5e700","react-syntax-highlighter_languages_refractor_haxe":"cc7ad0e00606c7d234e0","react-syntax-highlighter_languages_refractor_hpkp":"8f905841a55244e32afe","react-syntax-highlighter_languages_refractor_hsts":"d9f135c42946ab8dc41f","react-syntax-highlighter_languages_refractor_http":"295c9c71f24b9e3d3319","react-syntax-highlighter_languages_refractor_ichigojam":"9fa13c754215d123e80e","react-syntax-highlighter_languages_refractor_icon":"d269d7d61da5e4fbc1b9","react-syntax-highlighter_languages_refractor_inform7":"50ad98bfc695c9cf0b20","react-syntax-highlighter_languages_refractor_ini":"0ae9282d96485a32de92","react-syntax-highlighter_languages_refractor_io":"f3fc51e5fbd0ea7223cd","react-syntax-highlighter_languages_refractor_j":"bc32324f3a5be45fe9d4","react-syntax-highlighter_languages_refractor_java":"c6f0d2d069feaa94c53b","react-syntax-highlighter_languages_refractor_javascript":"a36a1f9a4742a12a4eb0","react-syntax-highlighter_languages_refractor_jolie":"c0402cab9ac664687c85","react-syntax-highlighter_languages_refractor_json":"ce53741e45eba3e5f573","react-syntax-highlighter_languages_refractor_jsx":"c4286450ac1b060ab910","react-syntax-highlighter_languages_refractor_julia":"f7ae14cf4c979db6e1b2","react-syntax-highlighter_languages_refractor_keyman":"8f11fa741d0e587c4f18","react-syntax-highlighter_languages_refractor_kotlin":"4e8cd8719fbf53e2bd9f","react-syntax-highlighter_languages_refractor_latex":"2b549347004a0fcf55c0","react-syntax-highlighter_languages_refractor_less":"2349dd797c6178a49dc9","react-syntax-highlighter_languages_refractor_liquid":"6951c0182bec3b3f54c5","react-syntax-highlighter_languages_refractor_lisp":"15246953adbae2bbd96d","react-syntax-highlighter_languages_refractor_livescript":"cf980dc220985ae9a45b","react-syntax-highlighter_languages_refractor_lolcode":"6967428208fabbe46735","react-syntax-highlighter_languages_refractor_lua":"5cf775daa35d70c283fc","react-syntax-highlighter_languages_refractor_makefile":"419d3e24ada0f4948d28","react-syntax-highlighter_languages_refractor_markupTemplating":"d22367ad9d1f1e45cdfe","react-syntax-highlighter_languages_refractor_markup":"56b9d2fbadd63ef4476a","react-syntax-highlighter_languages_refractor_matlab":"353b54ad9f1252393147","react-syntax-highlighter_languages_refractor_mizar":"35d88a2fea82946d9f1e","react-syntax-highlighter_languages_refractor_monkey":"61c28ded7cbfa755e7d5","react-syntax-highlighter_languages_refractor_n4js":"5f51469cb3956b65fc46","react-syntax-highlighter_languages_refractor_nasm":"ad680c556ac1b54ddd19","react-syntax-highlighter_languages_refractor_nginx":"a3eb4f98a13d843f9dd8","react-syntax-highlighter_languages_refractor_nim":"d744e1c83f9dbda41e81","react-syntax-highlighter_languages_refractor_nix":"880c7c54b5f8bb4c7c4a","react-syntax-highlighter_languages_refractor_nsis":"337a4f84c710910b773e","react-syntax-highlighter_languages_refractor_objectivec":"3b532068246487935bb3","react-syntax-highlighter_languages_refractor_ocaml":"ac48d710b14a9f144d39","react-syntax-highlighter_languages_refractor_oz":"c4d623c118d513287277","react-syntax-highlighter_languages_refractor_parigp":"121de44dae1a38792e08","react-syntax-highlighter_languages_refractor_parser":"677c95ea0eb92c5ce496","react-syntax-highlighter_languages_refractor_pascal":"1785de2fb150d1c0d6ab","react-syntax-highlighter_languages_refractor_perl":"9668c2a3dee2150d4202","react-syntax-highlighter_languages_refractor_phpExtras":"1b2de112902914a8aae0","react-syntax-highlighter_languages_refractor_php":"c0a3c4d0d960b96f244f","react-syntax-highlighter_languages_refractor_plsql":"20333fff7d0018709366","react-syntax-highlighter_languages_refractor_powershell":"6f7259f94b9b1b4e811e","react-syntax-highlighter_languages_refractor_processing":"62aa0acc9ae1b5348de5","react-syntax-highlighter_languages_refractor_prolog":"d56599a326d2e628fc58","react-syntax-highlighter_languages_refractor_properties":"1443452c5e0ec13471d9","react-syntax-highlighter_languages_refractor_protobuf":"4608c47463576fbc0dc3","react-syntax-highlighter_languages_refractor_pug":"ae5ede2760e7da4fa2fe","react-syntax-highlighter_languages_refractor_puppet":"6a8de901d3c5775a87bd","react-syntax-highlighter_languages_refractor_pure":"91505590175b421861f1","react-syntax-highlighter_languages_refractor_python":"f87022c61449dd27eeee","react-syntax-highlighter_languages_refractor_q":"0a588b4b64bc04e19c1b","react-syntax-highlighter_languages_refractor_qore":"3d45af68ab7f21f60a96","react-syntax-highlighter_languages_refractor_r":"d9a51fe59a1a6e495418","react-syntax-highlighter_languages_refractor_reason":"65b420f498e31239d6eb","react-syntax-highlighter_languages_refractor_renpy":"65b3424b0f6164deaf7f","react-syntax-highlighter_languages_refractor_rest":"a5b61fb96e432ce04d55","react-syntax-highlighter_languages_refractor_rip":"e10d8f4edc1804aaf8d5","react-syntax-highlighter_languages_refractor_roboconf":"8f0af0dcc35236ceb7fb","react-syntax-highlighter_languages_refractor_ruby":"5b486ed436591f760694","react-syntax-highlighter_languages_refractor_rust":"560dc9332d597ce224d4","react-syntax-highlighter_languages_refractor_sas":"416700a59858c5c1e139","react-syntax-highlighter_languages_refractor_sass":"7068ff51ae35c9ea45ad","react-syntax-highlighter_languages_refractor_scala":"8662f1b920e446f689b1","react-syntax-highlighter_languages_refractor_scheme":"761f4b7a6b2c15e94b4d","react-syntax-highlighter_languages_refractor_scss":"e00034076e69c5bc9144","react-syntax-highlighter_languages_refractor_smalltalk":"dd4dc1a7bb36160718ad","react-syntax-highlighter_languages_refractor_smarty":"deba5d3447d22430cd1e","react-syntax-highlighter_languages_refractor_soy":"65a8bfa196f796617ea0","react-syntax-highlighter_languages_refractor_sql":"55ffa194235081aa49bf","react-syntax-highlighter_languages_refractor_stylus":"11fbf8291911ef75d1f9","react-syntax-highlighter_languages_refractor_swift":"bcba4a557be3e01a8bea","react-syntax-highlighter_languages_refractor_tap":"24c8acab6735ded88579","react-syntax-highlighter_languages_refractor_tcl":"6239642ffb3279b18c66","react-syntax-highlighter_languages_refractor_textile":"7ab3ca0e9ff46bd401a6","react-syntax-highlighter_languages_refractor_tsx":"060e3ea69425c69dc47d","react-syntax-highlighter_languages_refractor_tt2":"c8d07fdebbde347fce63","react-syntax-highlighter_languages_refractor_twig":"47ec127a141979492797","react-syntax-highlighter_languages_refractor_typescript":"ac925cf8df121eb22815","react-syntax-highlighter_languages_refractor_vbnet":"30d16650d0b4ff71579f","react-syntax-highlighter_languages_refractor_velocity":"43ef6e9097c1eca0cd44","react-syntax-highlighter_languages_refractor_verilog":"322d353b9f16fc01116b","react-syntax-highlighter_languages_refractor_vhdl":"e529d9bedb9bbc2396fa","react-syntax-highlighter_languages_refractor_visualBasic":"2998120a4555ea26fc07","react-syntax-highlighter_languages_refractor_wasm":"ed6c33b2c1cc4a8c3bfb","react-syntax-highlighter_languages_refractor_wiki":"4ab5ed2582aaa2f05cbb","react-syntax-highlighter_languages_refractor_xeora":"8f8b73b3d374cae400da","react-syntax-highlighter_languages_refractor_xojo":"6460032c90d994772144","react-syntax-highlighter_languages_refractor_xquery":"69fdf0b2e1333ef01023","react-syntax-highlighter_languages_refractor_yaml":"c5eda89ed502c11864c9"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "observacode:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "observacode";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@emotion/react", "11.9.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9"), __webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_memoize_dist_emotion-m-00c0260")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@emotion/react/dist/emotion-react.browser.esm.js */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))));
/******/ 					register("@emotion/styled", "11.9.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9"), __webpack_require__.e("vendors-node_modules_emotion_styled_dist_emotion-styled_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_8f22"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_1cec"), __webpack_require__.e("node_modules_babel_runtime_helpers_esm_extends_js-node_modules_emotion_memoize_dist_emotion-m-00c0261")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@emotion/styled/dist/emotion-styled.browser.esm.js */ "./node_modules/@emotion/styled/dist/emotion-styled.browser.esm.js"))))));
/******/ 					register("d3", "7.4.4", () => (Promise.all([__webpack_require__.e("vendors-node_modules_d3_src_index_js"), __webpack_require__.e("vendors-node_modules_d3-scale_src_sequential_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/d3/src/index.js */ "./node_modules/d3/src/index.js"))))));
/******/ 					register("levenshtein-edit-distance", "3.0.0", () => (__webpack_require__.e("node_modules_levenshtein-edit-distance_index_js").then(() => (() => (__webpack_require__(/*! ./node_modules/levenshtein-edit-distance/index.js */ "./node_modules/levenshtein-edit-distance/index.js"))))));
/******/ 					register("observacode", "0.1.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_d3-scale_src_sequential_js"), __webpack_require__.e("vendors-node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_mui_mat-39df4f"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_yjs"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_8f22"), __webpack_require__.e("lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("react-code-blocks", "0.0.9-0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react-code-blocks_dist_react-code-blocks_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-syntax-highlighter_react-syntax-highlighter"), __webpack_require__.e("node_modules_emotion_memoize_dist_emotion-memoize_browser_esm_js-node_modules_react-is_index_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-code-blocks/dist/react-code-blocks.esm.js */ "./node_modules/react-code-blocks/dist/react-code-blocks.esm.js"))))));
/******/ 					register("react-syntax-highlighter", "12.2.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_asyncToGenerator_js-node_modules_babel_runtime-4278be"), __webpack_require__.e("react-syntax-highlighter/refractor-core-import"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_mel"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_refractor_lang_opencl_js"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_vim"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_markdown"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_gherkin"), __webpack_require__.e("react-syntax-highlighter/refractor-import"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_isbl"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_mathematica"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_oneC"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_gml"), __webpack_require__.e("react-syntax-highlighter/lowlight-import"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_sqf"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_powershell_js"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_maxima_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_pgsql"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_x86asm"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_mel"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_gauss"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_stata"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_sql_js"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_lsl_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_vim"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_autoit_js"), __webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_assertThisInitialized_js-node_modules_babel_ru-3f0775"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-code-blocks/node_modules/react-syntax-highlighter/dist/esm/index.js */ "./node_modules/react-code-blocks/node_modules/react-syntax-highlighter/dist/esm/index.js"))))));
/******/ 					register("react-syntax-highlighter", "15.5.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_refractor_lang_csharp_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_php_js"), __webpack_require__.e("vendors-node_modules_refractor_core_js"), __webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_asyncToGenerator_js-node_modules_babel_runtime-4278be"), __webpack_require__.e("vendors-node_modules_refractor_lang_mel_js"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_opencl"), __webpack_require__.e("vendors-node_modules_refractor_lang_vim_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_markdown_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_sas_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_gherkin_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_haml_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_textile_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_bash_js"), __webpack_require__.e("vendors-node_modules_refractor_index_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_mathematica_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_isbl_js"), __webpack_require__.e("vendors-node_modules_lowlight_lib_core_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_1c_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_gml_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_sqf_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_maxima"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_pgsql_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_x86asm_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_swift_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_mel_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stata_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_gauss_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_typescript_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_arduino_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_javascript_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_less_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_lsl"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_sql"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_css_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_scss_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stylus_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stan_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_vim_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_livecodeserver_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_cpp_js"), __webpack_require__.e("vendors-node_modules_react-syntax-highlighter_dist_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_babel_runtime_helpers_esm_assertThisInitialized_js-node_modules_babel_runtime_he-99d734")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-syntax-highlighter/dist/esm/index.js */ "./node_modules/react-syntax-highlighter/dist/esm/index.js"))))));
/******/ 					register("y-websocket", "1.4.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_y-websocket_src_y-websocket_js"), __webpack_require__.e("webpack_sharing_consume_default_yjs")]).then(() => (() => (__webpack_require__(/*! ./node_modules/y-websocket/src/y-websocket.js */ "./node_modules/y-websocket/src/y-websocket.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,17,0,1])),
/******/ 			"webpack/sharing/consume/default/yjs": () => (loadSingletonVersionCheck("default", "yjs", [1,13,5,17])),
/******/ 			"webpack/sharing/consume/default/@emotion/react/@emotion/react?8f22": () => (loadFallback("default", "@emotion/react", () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9"), __webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js")]).then(() => (() => (__webpack_require__(/*! @emotion/react */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/coreutils": () => (loadSingletonVersionCheck("default", "@jupyterlab/coreutils", [1,6,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersionCheck("default", "@jupyterlab/services", [1,7,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application": () => (loadSingletonVersionCheck("default", "@jupyterlab/application", [1,4,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@lumino/disposable": () => (loadSingletonVersionCheck("default", "@lumino/disposable", [1,1,10,1])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,4,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/user": () => (loadSingletonVersionCheck("default", "@jupyterlab/user", [1,4,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": () => (loadSingletonVersionCheck("default", "@jupyterlab/rendermime", [1,4,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": () => (loadSingletonVersionCheck("default", "@jupyterlab/ui-components", [1,4,0,0,,"alpha",20])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/translation": () => (loadSingletonVersionCheck("default", "@jupyterlab/translation", [1,4,0,0,,"alpha",5])),
/******/ 			"webpack/sharing/consume/default/y-websocket/y-websocket": () => (loadStrictVersionCheckFallback("default", "y-websocket", [1,1,4,3], () => (__webpack_require__.e("vendors-node_modules_y-websocket_src_y-websocket_js").then(() => (() => (__webpack_require__(/*! y-websocket */ "./node_modules/y-websocket/src/y-websocket.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/styled/@emotion/styled": () => (loadStrictVersionCheckFallback("default", "@emotion/styled", [1,11,3,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9"), __webpack_require__.e("vendors-node_modules_emotion_styled_dist_emotion-styled_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_emotion_react_emotion_react-_1cec")]).then(() => (() => (__webpack_require__(/*! @emotion/styled */ "./node_modules/@emotion/styled/dist/emotion-styled.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/react/@emotion/react?9405": () => (loadStrictVersionCheckFallback("default", "@emotion/react", [1,11,4,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_serialize_dist_emotion-serialize_browser_esm_js-node_modules_emo-e86cc9"), __webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js")]).then(() => (() => (__webpack_require__(/*! @emotion/react */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/d3/d3": () => (loadStrictVersionCheckFallback("default", "d3", [1,7,1,1], () => (__webpack_require__.e("vendors-node_modules_d3_src_index_js").then(() => (() => (__webpack_require__(/*! d3 */ "./node_modules/d3/src/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?18b7": () => (loadStrictVersionCheckFallback("default", "react-syntax-highlighter", [1,15,5,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_refractor_lang_csharp_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_php_js"), __webpack_require__.e("vendors-node_modules_refractor_core_js"), __webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_asyncToGenerator_js-node_modules_babel_runtime-4278be"), __webpack_require__.e("vendors-node_modules_refractor_lang_mel_js"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_opencl"), __webpack_require__.e("vendors-node_modules_refractor_lang_vim_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_markdown_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_sas_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_gherkin_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_haml_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_textile_js"), __webpack_require__.e("vendors-node_modules_refractor_lang_bash_js"), __webpack_require__.e("vendors-node_modules_refractor_index_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_mathematica_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_isbl_js"), __webpack_require__.e("vendors-node_modules_lowlight_lib_core_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_1c_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_gml_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_sqf_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_maxima"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_pgsql_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_x86asm_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_swift_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_mel_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stata_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_gauss_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_typescript_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_arduino_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_javascript_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_less_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_lsl"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_sql"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_css_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_scss_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stylus_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_stan_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_vim_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_livecodeserver_js"), __webpack_require__.e("vendors-node_modules_highlight_js_lib_languages_cpp_js"), __webpack_require__.e("vendors-node_modules_react-syntax-highlighter_dist_esm_index_js")]).then(() => (() => (__webpack_require__(/*! react-syntax-highlighter */ "./node_modules/react-syntax-highlighter/dist/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-code-blocks/react-code-blocks": () => (loadStrictVersionCheckFallback("default", "react-code-blocks", [3,0,0,9,,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react-code-blocks_dist_react-code-blocks_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react-syntax-highlighter_react-syntax-highlighter")]).then(() => (() => (__webpack_require__(/*! react-code-blocks */ "./node_modules/react-code-blocks/dist/react-code-blocks.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/levenshtein-edit-distance/levenshtein-edit-distance": () => (loadStrictVersionCheckFallback("default", "levenshtein-edit-distance", [1,3,0,0], () => (__webpack_require__.e("node_modules_levenshtein-edit-distance_index_js").then(() => (() => (__webpack_require__(/*! levenshtein-edit-distance */ "./node_modules/levenshtein-edit-distance/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@emotion/react/@emotion/react?1cec": () => (loadStrictVersionCheckFallback("default", "@emotion/react", [1,11,0,0,,"rc",0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_emotion_cache_dist_emotion-cache_browser_esm_js-node_modules_react-is_index_js"), __webpack_require__.e("vendors-node_modules_emotion_react_dist_emotion-react_browser_esm_js")]).then(() => (() => (__webpack_require__(/*! @emotion/react */ "./node_modules/@emotion/react/dist/emotion-react.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?e21e": () => (loadStrictVersionCheckFallback("default", "react-syntax-highlighter", [1,12,2,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_asyncToGenerator_js-node_modules_babel_runtime-4278be"), __webpack_require__.e("react-syntax-highlighter/refractor-core-import"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_mel"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_refractor_lang_opencl_js"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_vim"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_markdown"), __webpack_require__.e("react-syntax-highlighter_languages_refractor_gherkin"), __webpack_require__.e("react-syntax-highlighter/refractor-import"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_isbl"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_mathematica"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_oneC"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_gml"), __webpack_require__.e("react-syntax-highlighter/lowlight-import"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_sqf"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_powershell_js"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_maxima_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_pgsql"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_x86asm"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_mel"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_gauss"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_stata"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_sql_js"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_lsl_js"), __webpack_require__.e("react-syntax-highlighter_languages_highlight_vim"), __webpack_require__.e("vendors-node_modules_react-code-blocks_node_modules_highlight_js_lib_languages_autoit_js"), __webpack_require__.e("vendors-node_modules_babel_runtime_helpers_esm_assertThisInitialized_js-node_modules_babel_ru-3f0775")]).then(() => (() => (__webpack_require__(/*! react-syntax-highlighter */ "./node_modules/react-code-blocks/node_modules/react-syntax-highlighter/dist/esm/index.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_yjs": [
/******/ 				"webpack/sharing/consume/default/yjs"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_emotion_react_emotion_react-_8f22": [
/******/ 				"webpack/sharing/consume/default/@emotion/react/@emotion/react?8f22"
/******/ 			],
/******/ 			"lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/coreutils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application",
/******/ 				"webpack/sharing/consume/default/@lumino/disposable",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/user",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/translation",
/******/ 				"webpack/sharing/consume/default/y-websocket/y-websocket",
/******/ 				"webpack/sharing/consume/default/@emotion/styled/@emotion/styled",
/******/ 				"webpack/sharing/consume/default/@emotion/react/@emotion/react?9405",
/******/ 				"webpack/sharing/consume/default/d3/d3",
/******/ 				"webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?18b7",
/******/ 				"webpack/sharing/consume/default/react-code-blocks/react-code-blocks",
/******/ 				"webpack/sharing/consume/default/levenshtein-edit-distance/levenshtein-edit-distance"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_emotion_react_emotion_react-_1cec": [
/******/ 				"webpack/sharing/consume/default/@emotion/react/@emotion/react?1cec"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-syntax-highlighter_react-syntax-highlighter": [
/******/ 				"webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?e21e"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"observacode": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(emotion_react_emotion_react\-_(1cec|8f22)|react(|\-syntax\-highlighter_react\-syntax\-highlighter)|yjs)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/observacode");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).observacode = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.d9c2cc7d0a1a8a6868b4.js.map