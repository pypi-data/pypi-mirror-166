(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["react-syntax-highlighter_languages_highlight_julia"],{

/***/ "./node_modules/highlight.js/lib/languages/julia.js":
/*!**********************************************************!*\
  !*** ./node_modules/highlight.js/lib/languages/julia.js ***!
  \**********************************************************/
/***/ ((module) => {

/*
Language: Julia
Description: Julia is a high-level, high-performance, dynamic programming language.
Author: Kenta Sato <bicycle1885@gmail.com>
Contributors: Alex Arslan <ararslan@comcast.net>, Fredrik Ekre <ekrefredrik@gmail.com>
Website: https://julialang.org
*/

function julia(hljs) {
  // Since there are numerous special names in Julia, it is too much trouble
  // to maintain them by hand. Hence these names (i.e. keywords, literals and
  // built-ins) are automatically generated from Julia 1.5.2 itself through
  // the following scripts for each.

  // ref: https://docs.julialang.org/en/v1/manual/variables/#Allowed-Variable-Names
  var VARIABLE_NAME_RE = '[A-Za-z_\\u00A1-\\uFFFF][A-Za-z_0-9\\u00A1-\\uFFFF]*';

  // # keyword generator, multi-word keywords handled manually below (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String["in", "isa", "where"]
  // for kw in collect(x.keyword for x in REPLCompletions.complete_keyword(""))
  //     if !(contains(kw, " ") || kw == "struct")
  //         push!(res, kw)
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var KEYWORD_LIST = [
    'baremodule',
    'begin',
    'break',
    'catch',
    'ccall',
    'const',
    'continue',
    'do',
    'else',
    'elseif',
    'end',
    'export',
    'false',
    'finally',
    'for',
    'function',
    'global',
    'if',
    'import',
    'in',
    'isa',
    'let',
    'local',
    'macro',
    'module',
    'quote',
    'return',
    'true',
    'try',
    'using',
    'where',
    'while',
  ];

  // # literal generator (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String["true", "false"]
  // for compl in filter!(x -> isa(x, REPLCompletions.ModuleCompletion) && (x.parent === Base || x.parent === Core),
  //                     REPLCompletions.completions("", 0)[1])
  //     try
  //         v = eval(Symbol(compl.mod))
  //         if !(v isa Function || v isa Type || v isa TypeVar || v isa Module || v isa Colon)
  //             push!(res, compl.mod)
  //         end
  //     catch e
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var LITERAL_LIST = [
    'ARGS',
    'C_NULL',
    'DEPOT_PATH',
    'ENDIAN_BOM',
    'ENV',
    'Inf',
    'Inf16',
    'Inf32',
    'Inf64',
    'InsertionSort',
    'LOAD_PATH',
    'MergeSort',
    'NaN',
    'NaN16',
    'NaN32',
    'NaN64',
    'PROGRAM_FILE',
    'QuickSort',
    'RoundDown',
    'RoundFromZero',
    'RoundNearest',
    'RoundNearestTiesAway',
    'RoundNearestTiesUp',
    'RoundToZero',
    'RoundUp',
    'VERSION|0',
    'devnull',
    'false',
    'im',
    'missing',
    'nothing',
    'pi',
    'stderr',
    'stdin',
    'stdout',
    'true',
    'undef',
    'π',
    'ℯ',
  ];

  // # built_in generator (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String[]
  // for compl in filter!(x -> isa(x, REPLCompletions.ModuleCompletion) && (x.parent === Base || x.parent === Core),
  //                     REPLCompletions.completions("", 0)[1])
  //     try
  //         v = eval(Symbol(compl.mod))
  //         if (v isa Type || v isa TypeVar) && (compl.mod != "=>")
  //             push!(res, compl.mod)
  //         end
  //     catch e
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var BUILT_IN_LIST = [
    'AbstractArray',
    'AbstractChannel',
    'AbstractChar',
    'AbstractDict',
    'AbstractDisplay',
    'AbstractFloat',
    'AbstractIrrational',
    'AbstractMatrix',
    'AbstractRange',
    'AbstractSet',
    'AbstractString',
    'AbstractUnitRange',
    'AbstractVecOrMat',
    'AbstractVector',
    'Any',
    'ArgumentError',
    'Array',
    'AssertionError',
    'BigFloat',
    'BigInt',
    'BitArray',
    'BitMatrix',
    'BitSet',
    'BitVector',
    'Bool',
    'BoundsError',
    'CapturedException',
    'CartesianIndex',
    'CartesianIndices',
    'Cchar',
    'Cdouble',
    'Cfloat',
    'Channel',
    'Char',
    'Cint',
    'Cintmax_t',
    'Clong',
    'Clonglong',
    'Cmd',
    'Colon',
    'Complex',
    'ComplexF16',
    'ComplexF32',
    'ComplexF64',
    'CompositeException',
    'Condition',
    'Cptrdiff_t',
    'Cshort',
    'Csize_t',
    'Cssize_t',
    'Cstring',
    'Cuchar',
    'Cuint',
    'Cuintmax_t',
    'Culong',
    'Culonglong',
    'Cushort',
    'Cvoid',
    'Cwchar_t',
    'Cwstring',
    'DataType',
    'DenseArray',
    'DenseMatrix',
    'DenseVecOrMat',
    'DenseVector',
    'Dict',
    'DimensionMismatch',
    'Dims',
    'DivideError',
    'DomainError',
    'EOFError',
    'Enum',
    'ErrorException',
    'Exception',
    'ExponentialBackOff',
    'Expr',
    'Float16',
    'Float32',
    'Float64',
    'Function',
    'GlobalRef',
    'HTML',
    'IO',
    'IOBuffer',
    'IOContext',
    'IOStream',
    'IdDict',
    'IndexCartesian',
    'IndexLinear',
    'IndexStyle',
    'InexactError',
    'InitError',
    'Int',
    'Int128',
    'Int16',
    'Int32',
    'Int64',
    'Int8',
    'Integer',
    'InterruptException',
    'InvalidStateException',
    'Irrational',
    'KeyError',
    'LinRange',
    'LineNumberNode',
    'LinearIndices',
    'LoadError',
    'MIME',
    'Matrix',
    'Method',
    'MethodError',
    'Missing',
    'MissingException',
    'Module',
    'NTuple',
    'NamedTuple',
    'Nothing',
    'Number',
    'OrdinalRange',
    'OutOfMemoryError',
    'OverflowError',
    'Pair',
    'PartialQuickSort',
    'PermutedDimsArray',
    'Pipe',
    'ProcessFailedException',
    'Ptr',
    'QuoteNode',
    'Rational',
    'RawFD',
    'ReadOnlyMemoryError',
    'Real',
    'ReentrantLock',
    'Ref',
    'Regex',
    'RegexMatch',
    'RoundingMode',
    'SegmentationFault',
    'Set',
    'Signed',
    'Some',
    'StackOverflowError',
    'StepRange',
    'StepRangeLen',
    'StridedArray',
    'StridedMatrix',
    'StridedVecOrMat',
    'StridedVector',
    'String',
    'StringIndexError',
    'SubArray',
    'SubString',
    'SubstitutionString',
    'Symbol',
    'SystemError',
    'Task',
    'TaskFailedException',
    'Text',
    'TextDisplay',
    'Timer',
    'Tuple',
    'Type',
    'TypeError',
    'TypeVar',
    'UInt',
    'UInt128',
    'UInt16',
    'UInt32',
    'UInt64',
    'UInt8',
    'UndefInitializer',
    'UndefKeywordError',
    'UndefRefError',
    'UndefVarError',
    'Union',
    'UnionAll',
    'UnitRange',
    'Unsigned',
    'Val',
    'Vararg',
    'VecElement',
    'VecOrMat',
    'Vector',
    'VersionNumber',
    'WeakKeyDict',
    'WeakRef',
  ];

  var KEYWORDS = {
    $pattern: VARIABLE_NAME_RE,
    keyword: KEYWORD_LIST,
    literal: LITERAL_LIST,
    built_in: BUILT_IN_LIST,
  };

  // placeholder for recursive self-reference
  var DEFAULT = {
    keywords: KEYWORDS, illegal: /<\//
  };

  // ref: https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/
  var NUMBER = {
    className: 'number',
    // supported numeric literals:
    //  * binary literal (e.g. 0x10)
    //  * octal literal (e.g. 0o76543210)
    //  * hexadecimal literal (e.g. 0xfedcba876543210)
    //  * hexadecimal floating point literal (e.g. 0x1p0, 0x1.2p2)
    //  * decimal literal (e.g. 9876543210, 100_000_000)
    //  * floating pointe literal (e.g. 1.2, 1.2f, .2, 1., 1.2e10, 1.2e-10)
    begin: /(\b0x[\d_]*(\.[\d_]*)?|0x\.\d[\d_]*)p[-+]?\d+|\b0[box][a-fA-F0-9][a-fA-F0-9_]*|(\b\d[\d_]*(\.[\d_]*)?|\.\d[\d_]*)([eEfF][-+]?\d+)?/,
    relevance: 0
  };

  var CHAR = {
    className: 'string',
    begin: /'(.|\\[xXuU][a-zA-Z0-9]+)'/
  };

  var INTERPOLATION = {
    className: 'subst',
    begin: /\$\(/, end: /\)/,
    keywords: KEYWORDS
  };

  var INTERPOLATED_VARIABLE = {
    className: 'variable',
    begin: '\\$' + VARIABLE_NAME_RE
  };

  // TODO: neatly escape normal code in string literal
  var STRING = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    variants: [
      { begin: /\w*"""/, end: /"""\w*/, relevance: 10 },
      { begin: /\w*"/, end: /"\w*/ }
    ]
  };

  var COMMAND = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    begin: '`', end: '`'
  };

  var MACROCALL = {
    className: 'meta',
    begin: '@' + VARIABLE_NAME_RE
  };

  var COMMENT = {
    className: 'comment',
    variants: [
      { begin: '#=', end: '=#', relevance: 10 },
      { begin: '#', end: '$' }
    ]
  };

  DEFAULT.name = 'Julia';
  DEFAULT.contains = [
    NUMBER,
    CHAR,
    STRING,
    COMMAND,
    MACROCALL,
    COMMENT,
    hljs.HASH_COMMENT_MODE,
    {
      className: 'keyword',
      begin:
        '\\b(((abstract|primitive)\\s+)type|(mutable\\s+)?struct)\\b'
    },
    {begin: /<:/}  // relevance booster
  ];
  INTERPOLATION.contains = DEFAULT.contains;

  return DEFAULT;
}

module.exports = julia;


/***/ }),

/***/ "./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/julia.js":
/*!*****************************************************************************************!*\
  !*** ./node_modules/react-code-blocks/node_modules/highlight.js/lib/languages/julia.js ***!
  \*****************************************************************************************/
/***/ ((module) => {

module.exports = function(hljs) {
  // Since there are numerous special names in Julia, it is too much trouble
  // to maintain them by hand. Hence these names (i.e. keywords, literals and
  // built-ins) are automatically generated from Julia v0.6 itself through
  // the following scripts for each.

  var KEYWORDS = {
    // # keyword generator, multi-word keywords handled manually below
    // foreach(println, ["in", "isa", "where"])
    // for kw in Base.REPLCompletions.complete_keyword("")
    //     if !(contains(kw, " ") || kw == "struct")
    //         println(kw)
    //     end
    // end
    keyword:
      'in isa where ' +
      'baremodule begin break catch ccall const continue do else elseif end export false finally for function ' +
      'global if import importall let local macro module quote return true try using while ' +
      // legacy, to be deprecated in the next release
      'type immutable abstract bitstype typealias ',

    // # literal generator
    // println("true")
    // println("false")
    // for name in Base.REPLCompletions.completions("", 0)[1]
    //     try
    //         v = eval(Symbol(name))
    //         if !(v isa Function || v isa Type || v isa TypeVar || v isa Module || v isa Colon)
    //             println(name)
    //         end
    //     end
    // end
    literal:
      'true false ' +
      'ARGS C_NULL DevNull ENDIAN_BOM ENV I Inf Inf16 Inf32 Inf64 InsertionSort JULIA_HOME LOAD_PATH MergeSort ' +
      'NaN NaN16 NaN32 NaN64 PROGRAM_FILE QuickSort RoundDown RoundFromZero RoundNearest RoundNearestTiesAway ' +
      'RoundNearestTiesUp RoundToZero RoundUp STDERR STDIN STDOUT VERSION catalan e|0 eu|0 eulergamma golden im ' +
      'nothing pi γ π φ ',

    // # built_in generator:
    // for name in Base.REPLCompletions.completions("", 0)[1]
    //     try
    //         v = eval(Symbol(name))
    //         if v isa Type || v isa TypeVar
    //             println(name)
    //         end
    //     end
    // end
    built_in:
      'ANY AbstractArray AbstractChannel AbstractFloat AbstractMatrix AbstractRNG AbstractSerializer AbstractSet ' +
      'AbstractSparseArray AbstractSparseMatrix AbstractSparseVector AbstractString AbstractUnitRange AbstractVecOrMat ' +
      'AbstractVector Any ArgumentError Array AssertionError Associative Base64DecodePipe Base64EncodePipe Bidiagonal '+
      'BigFloat BigInt BitArray BitMatrix BitVector Bool BoundsError BufferStream CachingPool CapturedException ' +
      'CartesianIndex CartesianRange Cchar Cdouble Cfloat Channel Char Cint Cintmax_t Clong Clonglong ClusterManager ' +
      'Cmd CodeInfo Colon Complex Complex128 Complex32 Complex64 CompositeException Condition ConjArray ConjMatrix ' +
      'ConjVector Cptrdiff_t Cshort Csize_t Cssize_t Cstring Cuchar Cuint Cuintmax_t Culong Culonglong Cushort Cwchar_t ' +
      'Cwstring DataType Date DateFormat DateTime DenseArray DenseMatrix DenseVecOrMat DenseVector Diagonal Dict ' +
      'DimensionMismatch Dims DirectIndexString Display DivideError DomainError EOFError EachLine Enum Enumerate ' +
      'ErrorException Exception ExponentialBackOff Expr Factorization FileMonitor Float16 Float32 Float64 Function ' +
      'Future GlobalRef GotoNode HTML Hermitian IO IOBuffer IOContext IOStream IPAddr IPv4 IPv6 IndexCartesian IndexLinear ' +
      'IndexStyle InexactError InitError Int Int128 Int16 Int32 Int64 Int8 IntSet Integer InterruptException ' +
      'InvalidStateException Irrational KeyError LabelNode LinSpace LineNumberNode LoadError LowerTriangular MIME Matrix ' +
      'MersenneTwister Method MethodError MethodTable Module NTuple NewvarNode NullException Nullable Number ObjectIdDict ' +
      'OrdinalRange OutOfMemoryError OverflowError Pair ParseError PartialQuickSort PermutedDimsArray Pipe ' +
      'PollingFileWatcher ProcessExitedException Ptr QuoteNode RandomDevice Range RangeIndex Rational RawFD ' +
      'ReadOnlyMemoryError Real ReentrantLock Ref Regex RegexMatch RemoteChannel RemoteException RevString RoundingMode ' +
      'RowVector SSAValue SegmentationFault SerializationState Set SharedArray SharedMatrix SharedVector Signed ' +
      'SimpleVector Slot SlotNumber SparseMatrixCSC SparseVector StackFrame StackOverflowError StackTrace StepRange ' +
      'StepRangeLen StridedArray StridedMatrix StridedVecOrMat StridedVector String SubArray SubString SymTridiagonal ' +
      'Symbol Symmetric SystemError TCPSocket Task Text TextDisplay Timer Tridiagonal Tuple Type TypeError TypeMapEntry ' +
      'TypeMapLevel TypeName TypeVar TypedSlot UDPSocket UInt UInt128 UInt16 UInt32 UInt64 UInt8 UndefRefError UndefVarError ' +
      'UnicodeError UniformScaling Union UnionAll UnitRange Unsigned UpperTriangular Val Vararg VecElement VecOrMat Vector ' +
      'VersionNumber Void WeakKeyDict WeakRef WorkerConfig WorkerPool '
  };

  // ref: http://julia.readthedocs.org/en/latest/manual/variables/#allowed-variable-names
  var VARIABLE_NAME_RE = '[A-Za-z_\\u00A1-\\uFFFF][A-Za-z_0-9\\u00A1-\\uFFFF]*';

  // placeholder for recursive self-reference
  var DEFAULT = {
    lexemes: VARIABLE_NAME_RE, keywords: KEYWORDS, illegal: /<\//
  };

  // ref: http://julia.readthedocs.org/en/latest/manual/integers-and-floating-point-numbers/
  var NUMBER = {
    className: 'number',
    // supported numeric literals:
    //  * binary literal (e.g. 0x10)
    //  * octal literal (e.g. 0o76543210)
    //  * hexadecimal literal (e.g. 0xfedcba876543210)
    //  * hexadecimal floating point literal (e.g. 0x1p0, 0x1.2p2)
    //  * decimal literal (e.g. 9876543210, 100_000_000)
    //  * floating pointe literal (e.g. 1.2, 1.2f, .2, 1., 1.2e10, 1.2e-10)
    begin: /(\b0x[\d_]*(\.[\d_]*)?|0x\.\d[\d_]*)p[-+]?\d+|\b0[box][a-fA-F0-9][a-fA-F0-9_]*|(\b\d[\d_]*(\.[\d_]*)?|\.\d[\d_]*)([eEfF][-+]?\d+)?/,
    relevance: 0
  };

  var CHAR = {
    className: 'string',
    begin: /'(.|\\[xXuU][a-zA-Z0-9]+)'/
  };

  var INTERPOLATION = {
    className: 'subst',
    begin: /\$\(/, end: /\)/,
    keywords: KEYWORDS
  };

  var INTERPOLATED_VARIABLE = {
    className: 'variable',
    begin: '\\$' + VARIABLE_NAME_RE
  };

  // TODO: neatly escape normal code in string literal
  var STRING = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    variants: [
      { begin: /\w*"""/, end: /"""\w*/, relevance: 10 },
      { begin: /\w*"/, end: /"\w*/ }
    ]
  };

  var COMMAND = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    begin: '`', end: '`'
  };

  var MACROCALL = {
    className: 'meta',
    begin: '@' + VARIABLE_NAME_RE
  };

  var COMMENT = {
    className: 'comment',
    variants: [
      { begin: '#=', end: '=#', relevance: 10 },
      { begin: '#', end: '$' }
    ]
  };

  DEFAULT.contains = [
    NUMBER,
    CHAR,
    STRING,
    COMMAND,
    MACROCALL,
    COMMENT,
    hljs.HASH_COMMENT_MODE,
    {
      className: 'keyword',
      begin:
        '\\b(((abstract|primitive)\\s+)type|(mutable\\s+)?struct)\\b'
    },
    {begin: /<:/}  // relevance booster
  ];
  INTERPOLATION.contains = DEFAULT.contains;

  return DEFAULT;
};

/***/ })

}]);
//# sourceMappingURL=react-syntax-highlighter_languages_highlight_julia.2c2cb37b206b28fb4d5a.js.map