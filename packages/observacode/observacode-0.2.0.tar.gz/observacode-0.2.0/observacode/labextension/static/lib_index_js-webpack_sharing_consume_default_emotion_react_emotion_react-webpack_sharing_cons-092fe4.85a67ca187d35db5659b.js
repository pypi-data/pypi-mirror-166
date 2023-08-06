"use strict";
(self["webpackChunkobservacode"] = self["webpackChunkobservacode"] || []).push([["lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4"],{

/***/ "./lib/2dViz.js":
/*!**********************!*\
  !*** ./lib/2dViz.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PlotViz": () => (/* binding */ PlotViz)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(d3__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/linear.js");
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/sequential.js");
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/log.js");



;
;
class PlotViz extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.userCurrentEvent = {};
        this.paths = {};
        this.contourData = [];
        const WIDTH = this.props.width;
        const HEIGHT = this.props.height;
        const maxNumber = this.props.maxNumber;
        this.scalerX = (0,d3_scale__WEBPACK_IMPORTED_MODULE_2__["default"])().domain([this.props.minX, this.props.maxX]).range([0, WIDTH]);
        this.scalerY = (0,d3_scale__WEBPACK_IMPORTED_MODULE_2__["default"])().domain([this.props.minY, this.props.maxY]).range([0, HEIGHT]);
        this.scalerR = (0,d3_scale__WEBPACK_IMPORTED_MODULE_2__["default"])().domain([0, maxNumber]).range([0, 40]);
        this.scalerColor = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])(d3__WEBPACK_IMPORTED_MODULE_1__.interpolateRdYlGn).domain([0, 1]);
        this.props.activeUsers.forEach((name, index) => {
            this.userCurrentEvent[name] = this.props.events[name][0];
            this.paths[name] = d3__WEBPACK_IMPORTED_MODULE_1__.path();
            this.paths[name].moveTo(this.scalerX(this.props.events[name][0].x), this.scalerY(this.props.events[name][0].y));
        });
        this.setEventHappen();
    }
    setEventHappen() {
        var activeUsers = this.props.activeUsers;
        var events = this.props.events;
        const scope = this;
        const scalerTime = (0,d3_scale__WEBPACK_IMPORTED_MODULE_4__["default"])()
            .domain([1, 46272942000])
            .range([0, 60 * 1000]);
        // var maxTime = -Infinity;
        activeUsers.forEach((name) => {
            events[name].forEach((event, index) => {
                // if (event.timeOffset>maxTime){
                //     maxTime = event.timeOffset;
                // }
                console.log(event.timeOffset + 1, scalerTime(event.timeOffset + 1));
                setTimeout(() => {
                    scope.userCurrentEvent[name] = event;
                    scope.paths[name].lineTo(scope.scalerX(event.x), scope.scalerY(event.y));
                    scope.updateGraph(name);
                }, scalerTime(event.timeOffset + 1));
            });
        });
        // console.log(maxTime);
    }
    updateGraph(name) {
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        const scalerX = this.scalerX;
        const scalerY = this.scalerY;
        const WIDTH = this.props.width;
        const HEIGHT = this.props.height;
        var scope = this;
        var userCurrentEvent = this.userCurrentEvent;
        var d3Paths = this.paths;
        // update current dot
        var dot = graph.selectAll('.current-dot').select(function (d, i) { return d === name ? this : null; });
        dot.selectAll('circle')
            .transition()
            .duration(5000)
            .attr('cx', function (d, i) { return scalerX(userCurrentEvent[d].x); })
            .attr('cy', function (d, i) { return scalerY(userCurrentEvent[d].y); })
            .attr('fill', function (d, i) { return userCurrentEvent[d].passTest ? 'green' : 'red'; })
            .on('end', function (d, i) {
            // update contour
            scope.contourData[scope.props.activeUsers.indexOf(name)] = [scalerX(userCurrentEvent[name].x), scalerY(userCurrentEvent[name].y)];
            var contours = d3__WEBPACK_IMPORTED_MODULE_1__.contourDensity()
                .x(d => d[0])
                .y(d => d[1])
                .size([WIDTH, HEIGHT])
                .thresholds(3)(scope.contourData);
            var demapContours = [];
            contours.forEach((ring) => {
                ring.coordinates.forEach((value) => {
                    demapContours.push({ 'type': ring.type, 'value': ring.value, 'coordinates': [value] });
                });
            });
            var blob = graph.select('.blob');
            blob.selectAll('path')
                .data(demapContours)
                .join('path')
                .attr("stroke-width", 1)
                .attr("d", d3__WEBPACK_IMPORTED_MODULE_1__.geoPath())
                .on('mouseover', function (event, d) {
                const eventList = [];
                scope.props.activeUsers.forEach((name) => {
                    var _a;
                    var point = ((_a = this.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement).createSVGPoint();
                    point.x = scalerX(userCurrentEvent[name].x);
                    point.y = scalerY(userCurrentEvent[name].y);
                    if (this.isPointInFill(point)) {
                        console.log(name);
                        eventList.push(userCurrentEvent[name]);
                    }
                });
                scope.props.circleMouseOverFn(eventList);
            });
        });
        // update path
        var path = graph.selectAll('.path').select(function (d, i) { return d === name ? this : null; });
        path.selectAll("path")
            .transition()
            .delay(5000)
            .ease(d3__WEBPACK_IMPORTED_MODULE_1__.easeLinear)
            .attr('d', function (d, i) {
            return d3Paths[d].toString();
        });
    }
    addNodeToTree(nodeID) {
        const nSample = this.props.nSample;
        var node = this.props.treeNodes[nodeID];
        while (node !== null) {
            // if it is a leaf, update count, leafIDs
            if (node.id < nSample) {
                node.count += 1;
                node.leafIDs = [node.id];
            }
            // need to update node 1) count, 2) leafIDs, 3) x, 4) y
            else {
                node.count = node.leftChild.count + node.rightChild.count;
                node.leafIDs = node.leftChild.leafIDs.concat(node.rightChild.leafIDs);
                if (node.count !== 0) {
                    this.calculateNode(node);
                }
            }
            node = node.parent;
        }
    }
    initGroup() {
        var activeUsers = this.props.activeUsers;
        var events = this.props.events;
        var userCurrentEvent = this.userCurrentEvent;
        var d3Paths = this.paths;
        var scope = this;
        const WIDTH = this.props.width;
        const HEIGHT = this.props.height;
        const scalerX = this.scalerX;
        const scalerY = this.scalerY;
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas')
            .attr('width', WIDTH)
            .attr('height', HEIGHT);
        activeUsers.forEach((value, index) => {
            this.contourData.push([scalerX(events[value][0].x), scalerY(events[value][0].y)]);
        });
        // draw contour
        var contours = d3__WEBPACK_IMPORTED_MODULE_1__.contourDensity()
            .x(d => d[0])
            .y(d => d[1])
            .size([WIDTH, HEIGHT])
            .thresholds(3)(this.contourData);
        console.log(contours.length);
        var demapContours = [];
        contours.forEach((ring) => {
            ring.coordinates.forEach((value) => {
                demapContours.push({ 'type': ring.type, 'value': ring.value, 'coordinates': [value] });
            });
        });
        var blob = graph.append('g')
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr('class', 'blob');
        blob.selectAll('path')
            .data(demapContours)
            .join('path')
            .attr("stroke-width", 1)
            .attr('fill', 'none')
            .attr("d", d3__WEBPACK_IMPORTED_MODULE_1__.geoPath())
            .on('mouseover', function (event, d) {
            const eventList = [];
            scope.props.activeUsers.forEach((name) => {
                var _a;
                var point = ((_a = this.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement).createSVGPoint();
                point.x = scalerX(scope.userCurrentEvent[name].x);
                point.y = scalerY(scope.userCurrentEvent[name].y);
                if (this.isPointInFill(point)) {
                    console.log(name);
                    eventList.push(scope.userCurrentEvent[name]);
                }
            });
            scope.props.circleMouseOverFn(eventList);
        });
        // draw current dots
        var dots = graph.selectAll('.current-dot')
            .data(this.props.activeUsers)
            .enter()
            .append('g')
            .attr('class', 'current-dot')
            .attr('id', function (d, i) { return d; });
        dots.append('circle')
            .attr('r', 2)
            .attr('cx', function (d, i) { return scalerX(userCurrentEvent[d].x); })
            .attr('cy', function (d, i) { return scalerY(userCurrentEvent[d].y); })
            .attr('fill', function (d, i) { return userCurrentEvent[d].passTest ? 'green' : 'red'; });
        // draw history dots
        var historyDots = graph.selectAll('.history-dot')
            .data(activeUsers)
            .enter()
            .append('g')
            .attr('class', 'history-dot')
            .attr('id', function (d, i) { return d; });
        historyDots.each(function (d, i) {
            events[d].forEach((value, index) => {
                d3__WEBPACK_IMPORTED_MODULE_1__.select(this)
                    .append('circle')
                    .datum(value)
                    .attr('r', 2)
                    .attr('cx', function (d, i) { return scalerX(d.x); })
                    .attr('cy', function (d, i) { return scalerX(d.y); })
                    .attr('fill', function (d, i) { return d.passTest ? 'green' : 'red'; })
                    .attr('opacity', '0%');
            });
        });
        // draw moving paths, this changes as events happen
        var paths = graph.selectAll('.path')
            .data(activeUsers)
            .enter()
            .append('g')
            .attr('class', 'path')
            .attr('id', function (d, i) { return d; });
        paths.append("path")
            .style('stroke', 'gray')
            .style('stroke-width', '0.1')
            .style('fill', 'none')
            .attr('d', function (d, i) { return d3Paths[d].toString(); });
    }
    calculateNode(node) {
        if (node.leftChild.count === 0) {
            node.x = node.rightChild.x;
            node.y = node.rightChild.y;
            node.radius = node.rightChild.radius;
        }
        else if (node.rightChild.count === 0) {
            node.x = node.leftChild.x;
            node.y = node.leftChild.y;
            node.radius = node.leftChild.radius;
        }
        else {
            var leftX = node.leftChild.x;
            var leftY = node.leftChild.y;
            var rightX = node.rightChild.x;
            var rightY = node.rightChild.y;
            var deltaX = leftX - rightX;
            var deltaY = leftY - rightY;
            var d = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            var rLeft = node.leftChild.radius;
            var rRight = node.rightChild.radius;
            node.x = d === 0 ? leftX : (leftX * (d - rRight + rLeft) + rightX * (rRight - rLeft + d)) / (2 * d),
                node.y = d === 0 ? leftY : (leftY * (d - rRight + rLeft) + rightY * (rRight - rLeft + d)) / (2 * d),
                node.radius = (d + rLeft + rRight) / 2;
        }
    }
    componentDidMount() {
        this.initGroup();
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { id: '2d-viz-canvas', className: 'viz-canvas' });
    }
}



/***/ }),

/***/ "./lib/cellTypeButton.js":
/*!*******************************!*\
  !*** ./lib/cellTypeButton.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellTypeSwitcher": () => (/* binding */ CellTypeSwitcher)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! uuid */ "./node_modules/uuid/index.js");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(uuid__WEBPACK_IMPORTED_MODULE_4__);





const TOOLBAR_CELLTYPE_CLASS = 'jp-Notebook-toolbarCellType';
const TOOLBAR_CELLTYPE_DROPDOWN_CLASS = 'jp-Notebook-toolbarExerciseTypeDropdown';
/**
 * A toolbar widget that switches cell types.
 */
class CellTypeSwitcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /**
     * Construct a new cell type switcher.
     */
    constructor(widget, translator) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (event.target.value !== '-') {
                for (const widget of this._notebook.widgets) {
                    if (this._notebook.isSelectedOrActive(widget)) {
                        widget.model.metadata.set('exerciseType', event.target.value);
                        if (!widget.model.metadata.has('cellID')) {
                            widget.model.metadata.set('cellID', (0,uuid__WEBPACK_IMPORTED_MODULE_4__.v4)());
                        }
                    }
                }
                console.log('new type', event.target.value);
                this._notebook.activate();
                this.update();
            }
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._notebook.activate();
            }
        };
        this._trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        this.addClass(TOOLBAR_CELLTYPE_CLASS);
        this._notebook = widget;
        if (widget.model) {
            this.update();
        }
        widget.activeCellChanged.connect(this.update, this);
        // Follow a change in the selection.
        widget.selectionChanged.connect(this.update, this);
    }
    render() {
        let value = '-';
        if (this._notebook.activeCell) {
            if (this._notebook.activeCell.model.metadata.has('exerciseType')) {
                value = this._notebook.activeCell.model.metadata.get('exerciseType');
                console.log(value);
            }
        }
        for (const widget of this._notebook.widgets) {
            if (this._notebook.isSelectedOrActive(widget)) {
                if (widget.model.metadata.get('exerciseType') !== value) {
                    value = '-';
                    break;
                }
            }
        }
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.HTMLSelect, { className: TOOLBAR_CELLTYPE_DROPDOWN_CLASS, onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: value, "aria-label": this._trans.__('Cell type'), title: this._trans.__('Select the cell type') },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "-" }, "-"),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "description" }, this._trans.__('Description')),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "solution" }, this._trans.__('Solution')),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "test" }, this._trans.__('Test'))));
    }
}


/***/ }),

/***/ "./lib/clusterWidget.js":
/*!******************************!*\
  !*** ./lib/clusterWidget.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BasicClusterWidget": () => (/* binding */ BasicClusterWidget),
/* harmony export */   "ClusterWidget": () => (/* binding */ ClusterWidget),
/* harmony export */   "MyTag": () => (/* binding */ MyTag),
/* harmony export */   "OverCodeClusterWidget": () => (/* binding */ OverCodeClusterWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_code_blocks__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-code-blocks */ "webpack/sharing/consume/default/react-code-blocks/react-code-blocks");
/* harmony import */ var react_code_blocks__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_code_blocks__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _color__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./color */ "./lib/color.js");



;
;
class ClusterWidget extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
    }
    render() {
        const title = this.props.errorType;
        const count = this.props.errorMessages.length;
        const codeExamples = this.props.errorMessages.map((value) => { return value.code; });
        const messages = this.props.errorMessages.map((value) => { return value.eMessage; });
        const highlightLineNumbers = this.props.errorMessages.map((value) => { return value.lineIndex; });
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(BasicClusterWidget, { title: title, count: count, codeExamples: codeExamples, messages: messages, highlightLineNumbers: highlightLineNumbers, timelineButtonFn: this.props.timelineButtonFn, extraClassName: "error" });
    }
}
;
;
class OverCodeClusterWidget extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
    }
    render() {
        const title = `Cluster ${this.props.cluster_id}`;
        const count = this.props.cluster.count;
        const codeExamples = this.props.cluster.members;
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(BasicClusterWidget, { title: title, count: count, codeExamples: codeExamples, timelineButtonFn: this.props.timelineButtonFn, extraClassName: "overcode" });
    }
}
;
;
class BasicClusterWidget extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.state = {
            selectedIndex: 0,
            selectedCode: this.props.codeExamples[0],
            selectedMessage: this.props.messages ? this.props.messages[0] : undefined,
            selectedHighlightLineNumber: this.props.highlightLineNumbers ? this.props.highlightLineNumbers[0] : undefined,
        };
        this.previous = this.previous.bind(this);
        this.next = this.next.bind(this);
    }
    previous() {
        var index = this.state.selectedIndex;
        index -= 1;
        if (index === -1) {
            index += this.props.count;
        }
        this.setState({
            selectedCode: this.props.codeExamples[index],
            selectedMessage: this.props.messages ? this.props.messages[index] : undefined,
            selectedHighlightLineNumber: this.props.highlightLineNumbers ? this.props.highlightLineNumbers[index] : undefined,
            selectedIndex: index,
        });
    }
    next() {
        var index = this.state.selectedIndex;
        index += 1;
        if (index === this.props.count) {
            index = 0;
        }
        this.setState({
            selectedCode: this.props.codeExamples[index],
            selectedMessage: this.props.messages ? this.props.messages[index] : undefined,
            selectedHighlightLineNumber: this.props.highlightLineNumbers ? this.props.highlightLineNumbers[index] : undefined,
            selectedIndex: index,
        });
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: this.props.extraClassName ? `code-group-block ${this.props.extraClassName}` : 'code-group-block', "data-index": this.state.selectedIndex, "data-title": this.props.title },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                this.props.title,
                ", ",
                this.props.count,
                " solutions"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, this.state.selectedMessage)),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-editor-preview' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_code_blocks__WEBPACK_IMPORTED_MODULE_1__.CodeBlock, { text: this.state.selectedCode, language: "python", highlight: this.state.selectedHighlightLineNumber ? String(this.state.selectedHighlightLineNumber) : "" })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.previous }, "Prev"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.next }, "Next"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.timelineButtonFn ? this.props.timelineButtonFn : () => { } }, "Timeline")));
    }
}
;
;
class MyTag extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
    }
    tagColor(value) {
        if (value.startsWith('cluster')) {
            if (value === 'cluster -1') {
                return _color__WEBPACK_IMPORTED_MODULE_2__.COLOR_MAP["cluster-1"];
            }
            else {
                return 'silver';
            }
        }
        else {
            return _color__WEBPACK_IMPORTED_MODULE_2__.COLOR_MAP[value];
        }
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'solution-group-tag', "data-value": this.props.value, style: { backgroundColor: this.tagColor(this.props.value) }, onClick: this.props.onClick },
            this.props.value,
            " ",
            this.props.count);
    }
}


/***/ }),

/***/ "./lib/color.js":
/*!**********************!*\
  !*** ./lib/color.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "COLOR_MAP": () => (/* binding */ COLOR_MAP)
/* harmony export */ });
const COLOR_MAP = {
    'SyntaxError': 'yellow',
    'ValueError': 'coral',
    'KeyError': 'thistle',
    'NameError': 'darkgoldenrod',
    'TypeError': 'violet',
    'IndentationError': 'gold',
    'AttributeError': 'lavender',
    'cluster-1': 'deeppink',
    'correct': 'green',
};


/***/ }),

/***/ "./lib/configWidget.js":
/*!*****************************!*\
  !*** ./lib/configWidget.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConfigPanel": () => (/* binding */ ConfigPanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Switch__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Switch */ "./node_modules/@mui/material/Switch/Switch.js");
/* harmony import */ var _mui_material_FormGroup__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/FormGroup */ "./node_modules/@mui/material/FormGroup/FormGroup.js");
/* harmony import */ var _mui_material_FormControlLabel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/FormControlLabel */ "./node_modules/@mui/material/FormControlLabel/FormControlLabel.js");




class ConfigPanel extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'config-panel' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_FormGroup__WEBPACK_IMPORTED_MODULE_1__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_FormControlLabel__WEBPACK_IMPORTED_MODULE_2__["default"], { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Switch__WEBPACK_IMPORTED_MODULE_3__["default"], { checked: this.props.typingActivityMode, onChange: this.props.setTypingActivityMode }), label: "Typing Activities" })));
    }
}


/***/ }),

/***/ "./lib/dlView.js":
/*!***********************!*\
  !*** ./lib/dlView.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/user */ "webpack/sharing/consume/default/@jupyterlab/user");
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _dlViewWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dlViewWidget */ "./lib/dlViewWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");








class ButtonExtension {
    createNew(widget, context) {
        function callback() {
            var events = {};
            // var treeData: number[][] = [];
            var distanceData = [];
            // load data from server end
            (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('get_dl_view_results')
                .then(data => {
                events = data.events;
                // treeData = data.tree;
                distanceData = data.distance;
                console.log(distanceData);
                const keySolutionWidgetMap = new Map();
                widget.content.widgets.forEach((cell, index) => {
                    var solutionViewModel = new _dlViewWidget__WEBPACK_IMPORTED_MODULE_6__.DLViewModel(events);
                    var solutionViewWidget = new _dlViewWidget__WEBPACK_IMPORTED_MODULE_6__.DLViewWidget(solutionViewModel);
                    keySolutionWidgetMap.set(cell.model.metadata.get('cellID'), solutionViewWidget);
                    cell.layout.addWidget(solutionViewWidget);
                });
                const keyCellMap = new Map();
                widget.content.widgets.forEach((cell, index) => {
                    keyCellMap.set(cell.model.metadata.get('cellID'), index);
                });
            })
                .catch(reason => {
                console.error(`The observacode server extension appears to be missing.\n${reason}`);
            });
        }
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'observe-button',
            label: 'Deep Learning View',
            onClick: callback,
            tooltip: `Observe students' progress in 2d view`
        });
        widget.toolbar.insertItem(13, 'dlbutton', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
const pluginDLView = {
    id: 'ovservacode:dl-plugin',
    autoStart: true,
    requires: [_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__.ICurrentUser, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: activatePlugin
};
function activatePlugin(app, user, palette, rendermime, restorer) {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (pluginDLView);


/***/ }),

/***/ "./lib/dlViewWidget.js":
/*!*****************************!*\
  !*** ./lib/dlViewWidget.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DLViewModel": () => (/* binding */ DLViewModel),
/* harmony export */   "DLViewWidget": () => (/* binding */ DLViewWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _2dViz__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./2dViz */ "./lib/2dViz.js");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-syntax-highlighter */ "webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?18b7");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_2__);




class DLViewModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor(events) {
        super();
        this.activeUsers = [];
        this.currentPosition = {};
        this.events = {};
        this.treeNodes = {};
        this.leafEvents = {};
        this.minX = Infinity;
        this.minY = Infinity;
        this.maxX = -Infinity;
        this.maxY = -Infinity;
        // selectedLeafIDs: number[] = [];
        this.selectedEvents = [];
        this.loadEvents(events);
    }
    loadEvents(events) {
        // init variables
        var n_samples = 0;
        // set events
        this.events = events;
        // set minX, minY, maxX, maxY, nSample
        for (let name in events) {
            events[name].forEach((event) => {
                this.minX = event.x < this.minX ? event.x : this.minX;
                this.minY = event.y < this.minY ? event.y : this.minY;
                this.maxX = event.x > this.maxX ? event.x : this.maxX;
                this.maxY = event.y > this.maxY ? event.y : this.maxY;
                n_samples += 1;
                this.treeNodes[event.treeid] = {
                    id: event.treeid,
                    leftChild: null,
                    rightChild: null,
                    parent: null,
                    count: 1,
                    leafIDs: [event.treeid],
                    x: event.x,
                    y: event.y,
                    distance: null,
                    radius: 5,
                    code: event.code,
                };
                this.leafEvents[event.treeid] = event;
            });
            this.activeUsers.push(name);
        }
        this.nSample = n_samples;
    }
    circleMouseOver() {
        const scope = this;
        function fn(eventList) {
            // scope.selectedLeafIDs = leafIDs;
            scope.selectedEvents = eventList;
            scope.stateChanged.emit();
        }
        return fn;
    }
}
class DLViewWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model) {
        super(model);
    }
    circleMouseOut() {
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.UseSignal, { signal: this.model.stateChanged }, () => {
                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'dl-view', id: 'two-d-viz' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_2dViz__WEBPACK_IMPORTED_MODULE_3__.PlotViz, { activeUsers: this.model.activeUsers, events: this.model.events, treeNodes: this.model.treeNodes, rootNode: this.model.rootNode, leafEvents: this.model.leafEvents, nSample: this.model.nSample, minX: this.model.minX, minY: this.model.minY, maxX: this.model.maxX, maxY: this.model.maxY, width: 1200, height: 800, radius: 8, interval: 1500, maxNumber: 10, maxDistance: 10, circleMouseOverFn: this.model.circleMouseOver(), circleMouseOutFn: this.circleMouseOut })),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: 'code-view' }, this.model.selectedEvents.map((event) => {
                        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                            react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_2___default()), { language: 'python' }, event.code));
                    })));
            }));
    }
}



/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'observacode', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar.js");
/* harmony import */ var _realtime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./realtime */ "./lib/realtime.js");
/* harmony import */ var _observeCode__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./observeCode */ "./lib/observeCode.js");
/* harmony import */ var _dlView__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dlView */ "./lib/dlView.js");
/* harmony import */ var _scatterView__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./scatterView */ "./lib/scatterView.js");






/**
 * Initialization data for the observacode extension.
 */
const plugin = {
    id: 'observacode:plugin',
    autoStart: true,
    activate: (app) => {
        console.log('JupyterLab extension observacode is activated!');
        (0,_handler__WEBPACK_IMPORTED_MODULE_0__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The observacode server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, _toolbar__WEBPACK_IMPORTED_MODULE_1__["default"], _realtime__WEBPACK_IMPORTED_MODULE_2__["default"], _observeCode__WEBPACK_IMPORTED_MODULE_3__["default"], _dlView__WEBPACK_IMPORTED_MODULE_4__["default"], _scatterView__WEBPACK_IMPORTED_MODULE_5__["default"]]);
// export {plugin, plugintest};


/***/ }),

/***/ "./lib/observeCode.js":
/*!****************************!*\
  !*** ./lib/observeCode.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/user */ "webpack/sharing/consume/default/@jupyterlab/user");
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var y_websocket__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! y-websocket */ "webpack/sharing/consume/default/y-websocket/y-websocket");
/* harmony import */ var y_websocket__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(y_websocket__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _observeWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./observeWidget */ "./lib/observeWidget.js");









class ButtonExtension {
    createNew(widget, context) {
        function callback() {
            const keySolutionWidgetMap = new Map();
            widget.content.widgets.forEach((cell, index) => {
                var solutionViewModel = new _observeWidget__WEBPACK_IMPORTED_MODULE_7__.ObserveViewModel();
                var solutionViewWidget = new _observeWidget__WEBPACK_IMPORTED_MODULE_7__.ObserveViewWidget(solutionViewModel);
                keySolutionWidgetMap.set(cell.model.metadata.get('cellID'), solutionViewWidget);
                cell.layout.addWidget(solutionViewWidget);
            });
            const ydoc = new yjs__WEBPACK_IMPORTED_MODULE_5__.Doc();
            const websocketProvider = new y_websocket__WEBPACK_IMPORTED_MODULE_6__.WebsocketProvider('ws://localhost:1234', 'count-demo', ydoc);
            websocketProvider.connect();
            const keyCellMap = new Map();
            widget.content.widgets.forEach((cell, index) => {
                keyCellMap.set(cell.model.metadata.get('cellID'), index);
            });
            // bind observer
            function bindObserver() {
                for (const studentName of ydoc.share.keys()) {
                    const studentSource = ydoc.getMap(studentName);
                    studentSource.observe(event => {
                        event.changes.keys.forEach((change, key) => {
                            if (change.action === 'delete') {
                                return;
                            }
                            if (key.endsWith('-output')) {
                                const kkey = key.slice(0, -7);
                                if (keyCellMap.has(kkey)) {
                                    var solutionViewWidget = keySolutionWidgetMap.get(kkey);
                                    solutionViewWidget.model.setOutput(studentName, event.currentTarget.get(key).toArray());
                                }
                            }
                            else {
                                if (keyCellMap.has(key)) {
                                    const masterCopy = widget.content.widgets[keyCellMap.get(key)].model.sharedModel.getSource();
                                    var solutionViewWidget = keySolutionWidgetMap.get(key);
                                    solutionViewWidget.model.setSolution(studentName, event.currentTarget.get(key).toString(), masterCopy);
                                }
                            }
                        });
                    });
                }
            }
            // ydoc shared keys are not loaded yet
            websocketProvider.on('sync', () => {
                bindObserver();
            });
        }
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'observe-button',
            label: 'Observe Code',
            onClick: callback,
            tooltip: `Observe students' progress`
        });
        widget.toolbar.insertItem(12, 'observebutton', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
const pluginObserveCode = {
    id: 'ovservacode:observe-plugin',
    autoStart: true,
    requires: [_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__.ICurrentUser, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: activatePlugin
};
function activatePlugin(app, user, palette, rendermime, restorer) {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (pluginObserveCode);


/***/ }),

/***/ "./lib/observeWidget.js":
/*!******************************!*\
  !*** ./lib/observeWidget.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObserveViewModel": () => (/* binding */ ObserveViewModel),
/* harmony export */   "ObserveViewWidget": () => (/* binding */ ObserveViewWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _timelineWidget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./timelineWidget */ "./lib/timelineWidget.js");
/* harmony import */ var _clusterWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./clusterWidget */ "./lib/clusterWidget.js");
/* harmony import */ var _configWidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./configWidget */ "./lib/configWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






class ObserveViewModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor(displayAll = false) {
        super();
        this.solutions = new Map();
        this.outputs = new Map();
        this.activeUsers = [];
        this.queryFilter = {};
        this.events = new Map();
        this.typingActivities = new Map();
        this.startTime = new Map();
        this.nAccEdits = new Map();
        this.lastCommitEdits = new Map();
        this.eMessages = {};
        this.typingStatus = new Map();
        this.typingActivityMode = false;
        this.overCodeClusters = {};
        this.overCodeCandidates = {};
        this.overCodeResults = {};
        this.rawOverCodeResults = [];
        this.clusterIDs = [];
        this.occurCounter = {};
        this.allLines = {};
        this.sortedLines = [];
        // highlightedLines: string[] = [];
        this.pinnedName = "";
        this.displayAll = displayAll;
        this.setOverCodeResult();
    }
    setOverCodeResult() {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('get_overcode_results')
            .then(data => {
            console.log(data);
            var overcode_result = data.data;
            this.rawOverCodeResults = data.data;
            for (const cluster of overcode_result) {
                var cluster_id = cluster.id;
                for (const member of cluster.members) {
                    this.overCodeResults[member] = cluster_id;
                }
            }
            this.stateChanged.emit();
        })
            .catch(reason => {
            console.error(`The observacode server extension appears to be missing.\n${reason}`);
        });
    }
    setTypingActivityMode() {
        this.typingActivityMode = this.typingActivityMode ? false : true;
        this.stateChanged.emit();
    }
    setSolution(name, solution, masterCopy) {
        if (!this.nAccEdits.has(name)) {
            this.nAccEdits.set(name, 0);
            this.lastCommitEdits.set(name, 0);
        }
        this.nAccEdits.set(name, this.nAccEdits.get(name) + 1);
        if (this.solutions.has(name) && solution !== this.solutions.get(name)) {
            if (!this.activeUsers.includes(name)) {
                this.activeUsers.push(name);
                this.queryFilter[name] = 0;
                this.occurCounter[name] = {};
                this.stateChanged.emit();
            }
            this.solutions.set(name, solution);
        }
        else {
            if (this.displayAll) {
                if (!this.activeUsers.includes(name)) {
                    this.activeUsers.push(name);
                    this.occurCounter[name] = {};
                    this.queryFilter[name] = 0;
                }
                this.solutions.set(name, solution);
                this.stateChanged.emit();
            }
            else {
                this.solutions.set(name, solution);
            }
            this.startTime.set(name, Date.now());
        }
        this.typingStatus.set(name, true);
        this.addTypingActivity(name);
        setTimeout(() => { this.typingStatus.set(name, false); }, 5000);
    }
    setOutput(name, outputs) {
        this.outputs.set(name, outputs);
        if (outputs.length > 0) {
            this.addEvent(name);
        }
        // this.stateChanged.emit();
    }
    parseErrorMessage(eMessage) {
        var tokens = eMessage.split(' ');
        var errorType = tokens[0].slice(0, -1);
        var lineIndex;
        if (errorType === 'IndentationError') {
            lineIndex = parseInt(tokens[11]);
        }
        else {
            lineIndex = parseInt(tokens.slice(-1)[0]);
        }
        return { errorType, lineIndex };
    }
    addTypingActivity(name) {
        var _a;
        const activity = {
            timestamp: Date.now() - this.startTime.get(name)
        };
        if (!this.typingActivities.has(name)) {
            this.typingActivities.set(name, []);
        }
        (_a = this.typingActivities.get(name)) === null || _a === void 0 ? void 0 : _a.push(activity);
    }
    addEvent(name) {
        var _a, _b;
        const output = (_a = this.outputs.get(name)) === null || _a === void 0 ? void 0 : _a.slice(-1)[0];
        const emessage = output.output;
        const correct = output.passTest;
        const event = {
            value: this.solutions.get(name),
            radius: this.nAccEdits.get(name) - this.lastCommitEdits.get(name) + 1,
            startTime: Date.now() - this.startTime.get(name),
            correct: correct,
            tooltip: this.solutions.get(name),
            eMessage: emessage,
        };
        // set last commit edit number
        this.lastCommitEdits.set(name, this.nAccEdits.get(name));
        // add code lines to all lines
        var lines = this.solutions.get(name).split('\n');
        lines.forEach((value) => {
            const cleanV = value.trim();
            if (cleanV.startsWith('#')) {
                return;
            }
            else if (cleanV.startsWith('print')) {
                return;
            }
            else if (cleanV === '') {
                return;
            }
            else {
                if (!(cleanV in this.allLines)) {
                    this.allLines[cleanV] = { count: 0, names: [] };
                    // this.sortedLines = Object.keys(this.allLines).
                    this.sortedLines.push(cleanV);
                    this.sortedLines.sort();
                }
                this.allLines[cleanV].count += 1;
                if (!this.allLines[cleanV].names.includes(name)) {
                    this.allLines[cleanV].names.push(name);
                }
            }
        });
        // set error message
        if (emessage !== 'success') {
            const { errorType, lineIndex } = this.parseErrorMessage(emessage);
            if (!(errorType in this.eMessages)) {
                this.eMessages[errorType] = [];
            }
            this.eMessages[errorType].push({
                eMessage: emessage,
                eType: errorType,
                lineIndex: lineIndex,
                code: this.solutions.get(name),
                name: name,
                submissionIndex: this.outputs.get(name).length - 1,
            });
            event.errorType = errorType;
            if (!(errorType in this.occurCounter[name])) {
                this.occurCounter[name][errorType] = 0;
            }
            this.occurCounter[name][errorType] += 1;
        }
        else {
            if (!(name in this.overCodeCandidates)) {
                this.overCodeCandidates[name] = [];
            }
            this.overCodeCandidates[name].push(this.solutions.get(name));
            var cluster_id = this.updateOverCodeResults(name);
            if (!(cluster_id in this.occurCounter[name])) {
                this.occurCounter[name][cluster_id] = 0;
            }
            this.occurCounter[name][cluster_id] += 1;
        }
        if (!this.events.has(name)) {
            this.events.set(name, []);
        }
        (_b = this.events.get(name)) === null || _b === void 0 ? void 0 : _b.push(event);
        this.stateChanged.emit();
    }
    updateOverCodeResults(name) {
        var idx = this.overCodeCandidates[name].length - 1;
        var new_name = name.split('@')[0];
        var key = new_name + '_' + idx;
        var cluster_id = this.overCodeResults[key];
        if (this.rawOverCodeResults[cluster_id - 1].correct && !(this.clusterIDs.includes(cluster_id))) {
            this.clusterIDs.push(cluster_id);
        }
        else if (!(this.clusterIDs.includes(-1))) {
            this.clusterIDs.push(-1);
        }
        if (this.rawOverCodeResults[cluster_id - 1].correct && !(cluster_id in this.overCodeClusters)) {
            this.overCodeClusters[cluster_id] = {
                id: cluster_id,
                correct: this.rawOverCodeResults[cluster_id - 1].correct,
                count: 0,
                members: [],
                names: [],
            };
        }
        else if (!(-1 in this.overCodeClusters)) {
            this.overCodeClusters[-1] = {
                id: -1,
                correct: this.rawOverCodeResults[cluster_id - 1].correct,
                count: 0,
                members: [],
                names: [],
            };
        }
        if (this.rawOverCodeResults[cluster_id - 1].correct) {
            this.overCodeClusters[cluster_id].members.push(this.overCodeCandidates[name][idx]);
            this.overCodeClusters[cluster_id].names.push(name);
            this.overCodeClusters[cluster_id].count += 1;
        }
        else {
            this.overCodeClusters[-1].members.push(this.overCodeCandidates[name][idx]);
            this.overCodeClusters[-1].names.push(name);
            this.overCodeClusters[-1].count += 1;
        }
        this.stateChanged.emit();
        if (this.rawOverCodeResults[cluster_id - 1].correct) {
            return cluster_id;
        }
        else {
            return -1;
        }
    }
    setTimelineFocus() {
        var scope = this;
        function fn(event) {
            var _a;
            var targetBlock = (_a = event.currentTarget.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement;
            var index = parseInt(targetBlock.getAttribute('data-index'));
            var name;
            if (targetBlock.classList.contains('error')) {
                var errorType = targetBlock.getAttribute('data-title');
                name = scope.eMessages[errorType][index].name;
            }
            else if (targetBlock.classList.contains('overcode')) {
                var cluster_id = parseInt(targetBlock.getAttribute('data-title').split(' ').slice(-1)[0]);
                name = scope.overCodeClusters[cluster_id].names[index];
            }
            var targetLine = document.getElementById(name);
            targetLine === null || targetLine === void 0 ? void 0 : targetLine.classList.add('focus');
            setTimeout(() => { targetLine === null || targetLine === void 0 ? void 0 : targetLine.classList.remove('focus'); }, 5000);
        }
        return fn;
    }
    findSimilar(seedName) {
        // sort timeline by frequency diff
        var targetCounter = this.occurCounter[seedName];
        const sum = Object.values(targetCounter).reduce((a, b) => a + b, 0);
        var targetFreq = {};
        Object.keys(targetCounter).forEach((value) => {
            targetFreq[value] = targetCounter[value] / sum;
        });
        var diffs = {};
        this.activeUsers.forEach((name) => {
            var refCounter = this.occurCounter[name];
            var refSum = Object.values(refCounter).reduce((a, b) => a + b, 0);
            var refFreq = {};
            Object.keys(refCounter).forEach((value) => {
                refFreq[value] = refCounter[value] / refSum;
            });
            var keys = [...new Set(Object.keys(targetFreq).concat(Object.keys(refFreq)))];
            var squareDiff = keys.reduce((a, b) => {
                return a + ((targetFreq[b] ? targetFreq[b] : 0) - (refFreq[b] ? refFreq[b] : 0)) ** 2;
            }, 0);
            diffs[name] = squareDiff;
        });
        this.activeUsers = this.activeUsers.sort((a, b) => {
            var delta = diffs[a] - diffs[b];
            return delta;
        });
        // set pinned name
        this.pinnedName = seedName;
        this.stateChanged.emit();
    }
    phraseOnClick() {
        var scope = this;
        function fn(event) {
            var target = event.currentTarget;
            var key = target.getAttribute('data-key');
            // var 
            var names = scope.allLines[key].names;
            scope.activeUsers = scope.activeUsers.sort((a, b) => {
                // var delta = (names.includes(a))
                if (names.includes(a) && !names.includes(b)) {
                    return -1;
                }
                else if (!names.includes(a) && names.includes(b)) {
                    return 1;
                }
                else {
                    return 0;
                }
            });
            scope.stateChanged.emit();
        }
        return fn;
    }
    findSimilarTimeline() {
        var scope = this;
        function fn(event) {
            var target = event.currentTarget;
            var pinTitle = target.getAttribute('data-title');
            scope.findSimilar(pinTitle);
        }
        return fn;
    }
    queryUserNames(query) {
        var names;
        if (query.startsWith('cluster')) {
            var cluster_id = parseInt(query.split(' ').slice(-1)[0]);
            names = [...new Set(this.overCodeClusters[cluster_id].names)];
        }
        else {
            var errorType = query;
            names = [...new Set(this.eMessages[errorType].map((value) => { return value.name; }))];
        }
        return names;
    }
    addQuery(query) {
        var names = this.queryUserNames(query);
        for (const value of names) {
            this.queryFilter[value] += 1;
        }
        this.activeUsers = this.activeUsers.sort((a, b) => {
            return this.queryFilter[b] - this.queryFilter[a];
        });
        this.stateChanged.emit();
    }
    removeQuery(query) {
        var names = this.queryUserNames(query);
        for (const value of names) {
            this.queryFilter[value] -= 1;
        }
        this.activeUsers = this.activeUsers.sort((a, b) => {
            return this.queryFilter[b] - this.queryFilter[a];
        });
        this.stateChanged.emit();
    }
}
class ObserveViewWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model) {
        super(model);
        this.addClass('jp-ReactWidget');
        this.addClass('sideview');
    }
    setTypingActivityMode() {
        var scope = this;
        function fn() {
            scope.model.setTypingActivityMode();
        }
        return fn;
    }
    tagOnClick() {
        var scope = this;
        function fn(event) {
            console.log(event.currentTarget);
            var target = event.currentTarget;
            if (target.classList.contains('selected')) {
                target.classList.remove('selected');
                scope.model.removeQuery(target.getAttribute('data-value'));
            }
            else {
                target.classList.add('selected');
                scope.model.addQuery(target.getAttribute('data-value'));
            }
        }
        return fn;
    }
    render() {
        const errorTypes = Object.keys(this.model.eMessages);
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.UseSignal, { signal: this.model.stateChanged }, () => {
                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'configuration' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_configWidget__WEBPACK_IMPORTED_MODULE_3__.ConfigPanel, { typingActivityMode: this.model.typingActivityMode, setTypingActivityMode: this.setTypingActivityMode() })),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'timeline', id: 'left-panel' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_timelineWidget__WEBPACK_IMPORTED_MODULE_4__.TimeLine, { width: 800, height: 4000, lanes: this.model.activeUsers, queryFilter: this.model.queryFilter, events: this.model.events, typingActivities: this.model.typingActivities, typingStatus: this.model.typingStatus, tooltipMode: true, typingActivityMode: this.model.typingActivityMode, dotOnClick: () => { }, dotOnDragStart: () => { }, dotOnHover: () => { }, similarButtonOnClick: this.model.findSimilarTimeline() })),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: 'middle-panel' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("ul", null, this.model.sortedLines.map((key) => {
                            if (this.model.allLines[key].names.includes(this.model.pinnedName)) {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("li", { className: 'highlighted', "data-key": key, onClick: this.model.phraseOnClick() },
                                    this.model.allLines[key].count,
                                    " ",
                                    key);
                            }
                            else {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("li", { "data-key": key, onClick: this.model.phraseOnClick() },
                                    this.model.allLines[key].count,
                                    " ",
                                    key);
                            }
                        }))),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: 'right-panel' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                            errorTypes.map((value) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_clusterWidget__WEBPACK_IMPORTED_MODULE_5__.MyTag, { value: value, count: this.model.eMessages[value].length, onClick: this.tagOnClick() });
                            }),
                            this.model.clusterIDs.map((cluster_id) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_clusterWidget__WEBPACK_IMPORTED_MODULE_5__.MyTag, { value: `cluster ${cluster_id}`, count: this.model.overCodeClusters[cluster_id].count, onClick: this.tagOnClick() });
                            })),
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                            errorTypes.map((value) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_clusterWidget__WEBPACK_IMPORTED_MODULE_5__.ClusterWidget, { errorType: value, errorMessages: this.model.eMessages[value], events: this.model.events, timelineButtonFn: this.model.setTimelineFocus() });
                            }),
                            this.model.clusterIDs.map((cluster_id) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_clusterWidget__WEBPACK_IMPORTED_MODULE_5__.OverCodeClusterWidget, { cluster_id: cluster_id, cluster: this.model.overCodeClusters[cluster_id], timelineButtonFn: this.model.setTimelineFocus() });
                            }))),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null));
            }));
    }
}



/***/ }),

/***/ "./lib/realtime.js":
/*!*************************!*\
  !*** ./lib/realtime.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/user */ "webpack/sharing/consume/default/@jupyterlab/user");
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var y_websocket__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! y-websocket */ "webpack/sharing/consume/default/y-websocket/y-websocket");
/* harmony import */ var y_websocket__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(y_websocket__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _solutionWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./solutionWidget */ "./lib/solutionWidget.js");









class ButtonExtension {
    createNew(widget, context) {
        function callback() {
            const keySolutionWidgetMap = new Map();
            widget.content.widgets.forEach((cell, index) => {
                var solutionViewModel = new _solutionWidget__WEBPACK_IMPORTED_MODULE_7__.SolutionViewModel();
                var solutionViewWidget = new _solutionWidget__WEBPACK_IMPORTED_MODULE_7__.SolutionViewWidget(solutionViewModel);
                keySolutionWidgetMap.set(cell.model.metadata.get('cellID'), solutionViewWidget);
                cell.layout.addWidget(solutionViewWidget);
            });
            const ydoc = new yjs__WEBPACK_IMPORTED_MODULE_5__.Doc();
            const websocketProvider = new y_websocket__WEBPACK_IMPORTED_MODULE_6__.WebsocketProvider('ws://localhost:1234', 'count-demo', ydoc);
            websocketProvider.connect();
            const keyCellMap = new Map();
            widget.content.widgets.forEach((cell, index) => {
                keyCellMap.set(cell.model.metadata.get('cellID'), index);
            });
            // bind observer
            function bindObserver() {
                for (const studentName of ydoc.share.keys()) {
                    const studentSource = ydoc.getMap(studentName);
                    studentSource.observe(event => {
                        event.changes.keys.forEach((change, key) => {
                            if (change.action === 'delete') {
                                return;
                            }
                            if (key.endsWith('-output')) {
                                const kkey = key.slice(0, -7);
                                if (keyCellMap.has(kkey)) {
                                    keySolutionWidgetMap.get(kkey).model.setOutput(studentName, event.currentTarget.get(key).toArray());
                                }
                            }
                            else {
                                if (keyCellMap.has(key)) {
                                    const masterCopy = widget.content.widgets[keyCellMap.get(key)].model.sharedModel.getSource();
                                    var solutionViewWidget = keySolutionWidgetMap.get(key);
                                    solutionViewWidget.model.setSolution(studentName, event.currentTarget.get(key).toString(), masterCopy);
                                }
                            }
                        });
                    });
                }
            }
            // ydoc shared keys are not loaded yet
            websocketProvider.on('sync', () => {
                bindObserver();
            });
        }
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'sharing-button',
            label: 'Real Time View',
            onClick: callback,
            tooltip: 'Start Sharing'
        });
        widget.toolbar.insertItem(11, 'realtimebutton', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
const pluginShare = {
    id: 'ovservacode:share-plugin',
    autoStart: true,
    requires: [_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__.ICurrentUser, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: activatePluginTest
};
function activatePluginTest(app, user, palette, rendermime, restorer) {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (pluginShare);


/***/ }),

/***/ "./lib/scatterView.js":
/*!****************************!*\
  !*** ./lib/scatterView.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/user */ "webpack/sharing/consume/default/@jupyterlab/user");
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _scatterViewWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./scatterViewWidget */ "./lib/scatterViewWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");








class ButtonExtension {
    createNew(widget, context) {
        function callback() {
            var events = {};
            // var treeData: number[][] = [];
            // var distanceData: number[] = [];
            // load data from server end
            (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('get_dl_view_results')
                .then(data => {
                events = data.events;
                // treeData = data.tree;
                // distanceData = data.distance;
                // console.log(distanceData);
                // console.log(events);
                const keySolutionWidgetMap = new Map();
                widget.content.widgets.forEach((cell, index) => {
                    var solutionViewModel = new _scatterViewWidget__WEBPACK_IMPORTED_MODULE_6__.ScatterViewModel(events);
                    var solutionViewWidget = new _scatterViewWidget__WEBPACK_IMPORTED_MODULE_6__.ScatterViewWidget(solutionViewModel);
                    keySolutionWidgetMap.set(cell.model.metadata.get('cellID'), solutionViewWidget);
                    cell.layout.addWidget(solutionViewWidget);
                });
                const keyCellMap = new Map();
                widget.content.widgets.forEach((cell, index) => {
                    keyCellMap.set(cell.model.metadata.get('cellID'), index);
                });
            })
                .catch(reason => {
                console.error(`The observacode server extension appears to be missing.\n${reason}`);
            });
        }
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'observe-button',
            label: 'Scatter Plot View',
            onClick: callback,
            tooltip: `Scatter plot view`
        });
        widget.toolbar.insertItem(14, 'scatterbutton', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
const pluginScatterView = {
    id: 'ovservacode:scatter-plugin',
    autoStart: true,
    requires: [_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__.ICurrentUser, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: activatePlugin
};
function activatePlugin(app, user, palette, rendermime, restorer) {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (pluginScatterView);


/***/ }),

/***/ "./lib/scatterViewWidget.js":
/*!**********************************!*\
  !*** ./lib/scatterViewWidget.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScatterViewModel": () => (/* binding */ ScatterViewModel),
/* harmony export */   "ScatterViewWidget": () => (/* binding */ ScatterViewWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(d3__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-syntax-highlighter */ "webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?18b7");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _scatterViz__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./scatterViz */ "./lib/scatterViz.js");






var overcode_result;
(0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('get_overcode_results')
    .then(data => {
    overcode_result = data.data;
})
    .catch(reason => {
    console.error(`The observacode server extension appears to be missing.\n${reason}`);
});
// const KEEP_CLUSTER_IDS = [];
class ScatterViewModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor(events) {
        super();
        this.activeUsers = [];
        this.currentPosition = {};
        this.events = {};
        this.treeNodes = {};
        this.leafEvents = {};
        this.overCodeCandidates = {};
        this.overCodeResults = {};
        this.rawOverCodeResults = [];
        this.clusterIDs = [];
        this.overCodeClusters = {};
        this.position = {};
        this.minX = Infinity;
        this.minY = Infinity;
        this.maxX = -Infinity;
        this.maxY = -Infinity;
        // selectedLeafIDs: number[] = [];
        this.selectedEvents = [];
        this.rawOverCodeResults = overcode_result;
        for (const cluster of overcode_result) {
            var cluster_id = cluster.id;
            for (const member of cluster.members) {
                this.overCodeResults[member] = cluster_id;
            }
        }
        this.loadEvents(events);
    }
    updateOverCodeResults(name, event) {
        var _a, _b;
        var idx = this.overCodeCandidates[name].length - 1;
        var new_name = name.split('@')[0];
        var key = new_name + '_' + idx;
        var cluster_id = this.overCodeResults[key];
        // a few special cases
        if (['19114', '7071'].includes(event.id)) {
            cluster_id = 12;
        }
        event.clusterID = cluster_id;
        if (this.rawOverCodeResults[cluster_id - 1].correct && !(this.clusterIDs.includes(cluster_id))) {
            this.clusterIDs.push(cluster_id);
        }
        if (this.rawOverCodeResults[cluster_id - 1].correct && !(cluster_id in this.overCodeClusters)) {
            this.overCodeClusters[cluster_id] = {
                id: cluster_id,
                correct: this.rawOverCodeResults[cluster_id - 1].correct,
                count: 0,
                members: [],
                names: [],
                positions: [],
                events: [],
            };
        }
        if (this.rawOverCodeResults[cluster_id - 1].correct) {
            this.overCodeClusters[cluster_id].members.push(this.overCodeCandidates[name][idx]);
            this.overCodeClusters[cluster_id].names.push(name);
            (_a = this.overCodeClusters[cluster_id].positions) === null || _a === void 0 ? void 0 : _a.push({ x: event.x, y: event.y });
            (_b = this.overCodeClusters[cluster_id].events) === null || _b === void 0 ? void 0 : _b.push(event);
            this.overCodeClusters[cluster_id].count += 1;
        }
        if (this.rawOverCodeResults[cluster_id - 1].correct) {
            return cluster_id;
        }
        else {
            return null;
        }
    }
    averagePosition(positions) {
        var l = positions.length;
        var sumX = positions.reduce((a, b) => { return a + b.x; }, 0);
        var sumY = positions.reduce((a, b) => { return a + b.y; }, 0);
        var averagePosition = { x: sumX / l, y: sumY / l };
        return averagePosition;
    }
    sortClusterIDs() {
        function dist(posA, posB) {
            return (posA.x - posB.x) ** 2 + (posA.y - posB.y) ** 2;
        }
        // find largest cluster id
        var maxN = -Infinity;
        var maxID = -1;
        this.clusterIDs.forEach((id) => {
            if (this.overCodeClusters[id].count > maxN) {
                maxID = id;
                maxN = this.overCodeClusters[id].count;
            }
        });
        var position = {};
        this.clusterIDs.forEach((id) => {
            position[id] = this.averagePosition(this.overCodeClusters[id].positions);
        });
        this.position = position;
        // sort 2d array
        // directly sort this.clusterIDs
        this.clusterIDs.sort((a, b) => {
            var positionA = position[a];
            var positionB = position[b];
            return dist(positionA, position[maxID]) - dist(positionB, position[maxID]);
        });
    }
    loadEvents(events) {
        // init variables
        var n_samples = 0;
        // set events
        this.events = events;
        // set minX, minY, maxX, maxY, nSample
        for (let name in events) {
            events[name].forEach((event, index) => {
                this.minX = event.x < this.minX ? event.x : this.minX;
                this.minY = event.y < this.minY ? event.y : this.minY;
                this.maxX = event.x > this.maxX ? event.x : this.maxX;
                this.maxY = event.y > this.maxY ? event.y : this.maxY;
                n_samples += 1;
                if (event.type === 'run' && event.output === 'success') {
                    // get overcode cluster id
                    if (!(name in this.overCodeCandidates)) {
                        this.overCodeCandidates[name] = [];
                    }
                    this.overCodeCandidates[name].push(event.code);
                    this.updateOverCodeResults(name, event);
                }
            });
            this.activeUsers.push(name);
        }
        this.nSample = n_samples;
        // sort clusters by edit dist
        this.sortClusterIDs();
        this.stateChanged.emit();
    }
    circleMouseOver() {
        const scope = this;
        function fn(clusterID, correctSolutions, incorrectSolutions, correctNames, incorrectNames) {
            scope.selectedClusterID = clusterID;
            scope.selectedCorrectSolutions = correctSolutions;
            scope.selectedIncorrectSolutions = incorrectSolutions;
            scope.selectedCorrectNames = correctNames;
            scope.selectedIncorrectNames = incorrectNames;
            scope.stateChanged.emit();
        }
        return fn;
    }
    circleMouseOut() {
        const scope = this;
        function fn() {
            scope.stateChanged.emit();
        }
        return fn;
    }
    onBrushChange() {
        const scope = this;
        function fn(events) {
            scope.selectedEvents = events;
            scope.feedback = "";
            scope.stateChanged.emit();
        }
        return fn;
    }
    userOnClick() {
        const scope = this;
        function fn(event) {
            var target = event.currentTarget;
            // update right panel - selected solutions are user's commits
            const graph = d3__WEBPACK_IMPORTED_MODULE_2__.select('.viz-canvas');
            var currentDots = graph.selectAll('.current-dot');
            var paths = graph.selectAll('.trajectory');
            var historyDots = graph.selectAll('.history-dot');
            currentDots.filter(function (d, i) { return d !== target.id; })
                .attr('visibility', 'hidden');
            paths.filter(function (d, i) { return d !== target.id; })
                .attr('visibility', 'hidden');
            historyDots.filter(function (d, i) { return d !== target.id; })
                .attr('visibility', 'hidden');
            // focus on user
            // only show events that have happened
            var count = historyDots.select(function (d, i) { return d === target.id ? this : null; })
                .selectAll('circle')
                .size();
            scope.selectedEvents = scope.events[target.id].filter((e) => { return e.type === 'run'; }).slice(0, count);
            scope.feedback = "";
            scope.stateChanged.emit();
        }
        return fn;
    }
    feedbackSubmit() {
        var scope = this;
        function fn(event) {
            scope.selectedEvents.forEach((e) => {
                e.hasFeedback = true;
            });
            event.preventDefault();
            scope.stateChanged.emit();
        }
        return fn;
    }
    feedbackChange() {
        var scope = this;
        function fn(event) {
            scope.feedback = event.currentTarget.value;
            scope.stateChanged.emit();
        }
        return fn;
    }
}
class ScatterViewWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model) {
        super(model);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.UseSignal, { signal: this.model.stateChanged }, () => {
                var _a, _b, _c, _d;
                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'scatter-left-view' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_scatterViz__WEBPACK_IMPORTED_MODULE_5__.ScatterViz, { activeUsers: this.model.activeUsers, events: this.model.events, clusterIDs: this.model.clusterIDs, overCodeClusters: this.model.overCodeClusters, position: this.model.position, minX: this.model.minX, minY: this.model.minY, maxX: this.model.maxX, maxY: this.model.maxY, width: 1200, height: 800, radius: 8, circleMouseOverFn: this.model.circleMouseOver(), circleMouseOutFn: this.model.circleMouseOut(), onBrushChangeFn: this.model.onBrushChange() })),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'scatter-middle-view' },
                        this.model.selectedClusterID ? react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", null,
                            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", { style: { color: 'green' } }, (_a = this.model.selectedCorrectSolutions) === null || _a === void 0 ? void 0 : _a.length),
                            " correct solutions, ",
                            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", { style: { color: 'red' } }, (_b = this.model.selectedIncorrectSolutions) === null || _b === void 0 ? void 0 : _b.length),
                            " incorrect solutions.") : null,
                        this.model.selectedClusterID ? react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, (_c = this.model.selectedCorrectNames) === null || _c === void 0 ? void 0 :
                            _c.map((name) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'userbox correct', id: name, onClick: this.model.userOnClick() },
                                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, name.split('@')[0]));
                            }), (_d = this.model.selectedIncorrectNames) === null || _d === void 0 ? void 0 :
                            _d.map((name) => {
                                return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'userbox incorrect', id: name, onClick: this.model.userOnClick() },
                                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, name.split('@')[0]));
                            })) : null,
                        this.model.selectedClusterID ? react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default()), { language: 'python' }, this.model.overCodeClusters[this.model.selectedClusterID].members[0]) : null,
                        this.model.selectedIncorrectSolutions ? react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, this.model.selectedIncorrectSolutions.map((code) => {
                            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default()), { language: 'python', customStyle: {
                                    backgroundColor: "#FEDFE1"
                                } }, code);
                        })) : null),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'scatter-right-view' },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("form", { onSubmit: this.model.feedbackSubmit() },
                            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                                "Feedback:",
                                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "text", value: this.model.feedback, onChange: this.model.feedbackChange() })),
                            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "submit", value: "Submit" })),
                        this.model.selectedEvents.map((event, index) => {
                            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                                event.passTest ? null : react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, event.output === 'success' ? 'Failed the test case' : event.output),
                                react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default()), { language: 'python', showLineNumbers: true, wrapLines: true, customStyle: {
                                        backgroundColor: event.passTest ? "#F0F0F0" : "#FEDFE1",
                                        opacity: event.hasFeedback ? "50%" : "100%",
                                    }, lineProps: (lineNumber) => {
                                        var _a;
                                        const style = { display: "block", width: "100%" };
                                        if ((_a = event.output.match(/\d+/g)) === null || _a === void 0 ? void 0 : _a.includes(lineNumber.toString())) {
                                            style.backgroundColor = "#F596AA";
                                        }
                                        return { style };
                                    } }, event.code));
                        })));
            }));
    }
}



/***/ }),

/***/ "./lib/scatterViz.js":
/*!***************************!*\
  !*** ./lib/scatterViz.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScatterViz": () => (/* binding */ ScatterViz)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(d3__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/linear.js");
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/sequential.js");
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/log.js");
/* harmony import */ var levenshtein_edit_distance__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! levenshtein-edit-distance */ "webpack/sharing/consume/default/levenshtein-edit-distance/levenshtein-edit-distance");
/* harmony import */ var levenshtein_edit_distance__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(levenshtein_edit_distance__WEBPACK_IMPORTED_MODULE_2__);




;
;
class ScatterViz extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.userCurrentEvent = {};
        this.paths = {};
        this.userCluster = {}; // if -1, not in any cluster, other wise, is in the cluster 
        this.clusterProgress = {};
        this.userCorrectness = {};
        this.userCode = {};
        const WIDTH = this.props.width;
        const HEIGHT = this.props.height;
        this.scalerX = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])().domain([this.props.minX, this.props.maxX]).range([0, WIDTH]);
        this.scalerY = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])().domain([this.props.minY, this.props.maxY]).range([0, HEIGHT]);
        this.scalerColor = (0,d3_scale__WEBPACK_IMPORTED_MODULE_4__["default"])(d3__WEBPACK_IMPORTED_MODULE_1__.interpolateRdYlGn).domain([0, 1]);
        this.props.activeUsers.forEach((name, index) => {
            this.userCurrentEvent[name] = this.props.events[name][0];
            this.userCluster[name] = -1;
            this.userCorrectness[name] = false;
            this.paths[name] = d3__WEBPACK_IMPORTED_MODULE_1__.path();
            this.paths[name].moveTo(0, 0);
        });
        this.clusterProgress[-1] = { correct: [], incorrect: [], names: [] };
        this.props.clusterIDs.forEach((id) => {
            this.clusterProgress[id] = { correct: [], incorrect: [], names: [] };
        });
        this.setEventHappen();
    }
    setEventHappen() {
        var activeUsers = this.props.activeUsers;
        var events = this.props.events;
        const scope = this;
        const scalerTime = (0,d3_scale__WEBPACK_IMPORTED_MODULE_5__["default"])()
            .domain([1, 46272942000])
            .range([0, 60 * 1000]);
        activeUsers.forEach((name) => {
            events[name].forEach((event, index) => {
                setTimeout(() => {
                    var [x, y] = scope.calculatePos(name, event);
                    scope.userCode[name] = event.code;
                    // move path
                    scope.paths[name].lineTo(x, y);
                    scope.updateGraph(name, x, y, event.passTest, event);
                }, scalerTime(event.timeOffset + 1));
            });
        });
    }
    dist(posA, posB) {
        return (posA.x - posB.x) ** 2 + (posA.y - posB.y) ** 2;
    }
    distToCluster(event, clusterID) {
        var cluster = this.props.overCodeClusters[clusterID];
        var d = Infinity;
        for (var pos of cluster.positions) {
            var tempD = this.dist(pos, { x: event.x, y: event.y });
            if (tempD < d) {
                d = tempD;
            }
        }
        return d;
    }
    editDistanceToCluster(event, clusterID) {
        var cluster = this.props.overCodeClusters[clusterID];
        var d = Infinity;
        for (var e of cluster.events) {
            var editDist = this.editDistance(event.cleanedCode, e.cleanedCode);
            // console.log(editDist);
            if (editDist < d) {
                d = editDist;
            }
        }
        return d;
    }
    calculateY(event, name) {
        var clusterIDs = this.props.clusterIDs;
        const HEIGHT = this.props.height;
        if (event.type === 'run' && event.passTest) {
            if (event.clusterID) {
                var y = HEIGHT / clusterIDs.length * (clusterIDs.indexOf(event.clusterID) + 0.75);
                return [y, event.clusterID];
            }
            else {
                console.log('pass test but not have cluster id, need check here');
                return [0, 1];
            }
        }
        // find the position where it should be at
        var minDist = Infinity;
        var targetID = -1;
        for (var i of clusterIDs) {
            var dist = this.distToCluster(event, i);
            if (dist < minDist) {
                minDist = dist;
                targetID = i;
            }
        }
        var newClusterID = targetID;
        var y = HEIGHT / clusterIDs.length * (clusterIDs.indexOf(newClusterID) + 0.75);
        return [y, newClusterID];
    }
    editDistance(code1, code2) {
        return (0,levenshtein_edit_distance__WEBPACK_IMPORTED_MODULE_2__.levenshteinEditDistance)(code1, code2);
    }
    calculateX(event, newClusterID) {
        //   replace distance with edit distance
        const WIDTH = this.props.width;
        var scaler = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])().domain([0, WIDTH * 0.3]).range([0, WIDTH * 0.8]);
        if (event.type === 'run' && event.passTest) {
            if (event.clusterID) {
                return WIDTH * 0.8;
            }
            else {
                console.log('pass test but not have cluster id, need check here');
                return 0;
            }
        }
        var editDist = this.editDistanceToCluster(event, newClusterID);
        var x = WIDTH * 0.8 - scaler(editDist);
        return x;
    }
    calculatePos(name, event) {
        // log previous cluster
        var prevClusterID = this.userCluster[name];
        // calculate y
        // here y means which solution it is most close to
        var [y, newClusterID] = this.calculateY(event, name);
        this.userCluster[name] = newClusterID;
        if (newClusterID > 100) {
            console.log(name, event);
        }
        // every time y updates, should update how many dots are in each cluster
        this.updateClusterProgress(name, prevClusterID, newClusterID, event.passTest);
        // calculate x
        // here x means how far away the dot is from coresponding solution
        var x = this.calculateX(event, newClusterID);
        return [x, y];
    }
    updateClusterProgress(name, prevClusterID, newClusterID, newCorrectness) {
        // console.log(prevClusterID, newClusterID);
        if (prevClusterID !== -1) {
            if (this.clusterProgress[prevClusterID].correct.includes(name)) {
                // remove it from correct
                var index = this.clusterProgress[prevClusterID].correct.indexOf(name);
                this.clusterProgress[prevClusterID].correct.splice(index, 1);
            }
            else {
                // remove it from incorrect
                var index = this.clusterProgress[prevClusterID].incorrect.indexOf(name);
                this.clusterProgress[prevClusterID].incorrect.splice(index, 1);
            }
            var index = this.clusterProgress[prevClusterID].names.indexOf(name);
            this.clusterProgress[prevClusterID].names.splice(index, 1);
        }
        if (newCorrectness) {
            this.clusterProgress[newClusterID].correct.push(name);
        }
        else {
            this.clusterProgress[newClusterID].incorrect.push(name);
        }
        this.clusterProgress[newClusterID].names.push(name);
        this.updateProgressGraph(prevClusterID, newClusterID);
    }
    updateProgressGraph(prevClusterID, newClusterID) {
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        const WIDTH = this.props.width;
        var scope = this;
        var wScale = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])().domain([0, 1]).range([0, WIDTH * 0.1]);
        var progressBars = graph.selectAll('.progress-bar').filter(function (d, i) { return d === prevClusterID || d === newClusterID; });
        progressBars.selectAll('rect')
            .attr('width', function (d, i) { return wScale(scope.clusterProgress[d].correct.length / (scope.clusterProgress[d].correct.length + scope.clusterProgress[d].incorrect.length + 0.0001)); })
            .attr('fill', 'green');
    }
    updateGraph(name, x, y, passTest, event) {
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        var scope = this;
        // update dot
        var dot = graph.selectAll('.current-dot').select(function (d, i) { return d === name ? this : null; }).select('circle');
        dot.transition()
            .duration(500)
            .attr('cx', x)
            .attr('cy', y)
            .attr('fill', passTest ? 'green' : 'red');
        // update path
        var path = graph.selectAll('.trajectory').select(function (d, i) { return d === name ? this : null; }).select('path');
        path.transition()
            .delay(500)
            .attr('d', function (d, i) { return scope.paths[d].toString(); });
        if (event.type === 'run') {
            // add history dot
            var historyDots = graph.selectAll('.history-dot').select(function (d, i) { return d === name ? this : null; });
            historyDots.append('circle')
                .datum(event)
                .attr('r', 2)
                .attr('cx', x)
                .attr('cy', y)
                .attr('fill', passTest ? 'green' : 'red')
                .attr('opacity', '50%');
        }
    }
    updateBrush(scope, event) {
        function isBrushed(extent, cx, cy) {
            var x0 = extent[0][0], x1 = extent[1][0], y0 = extent[0][1], y1 = extent[1][1];
            var x = parseFloat(cx);
            var y = parseFloat(cy);
            return x >= x0 && x <= x1 && y >= y0 && y <= y1;
        }
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        var extent = d3__WEBPACK_IMPORTED_MODULE_1__.brushSelection(graph.select('.brush').node());
        var historyDots = graph.selectAll('.history-dot');
        if (extent) {
            historyDots.selectAll('circle')
                .classed("selected", function (d) { return isBrushed(extent, d3__WEBPACK_IMPORTED_MODULE_1__.select(this).attr('cx'), d3__WEBPACK_IMPORTED_MODULE_1__.select(this).attr('cy')) && d3__WEBPACK_IMPORTED_MODULE_1__.select(this.parentNode).attr('visibility') !== 'hidden'; });
            scope.props.onBrushChangeFn(historyDots.selectAll('circle.selected').data());
        }
    }
    focusSolution(scope, clusterID) {
        // get all names in this solution
        var names = scope.clusterProgress[clusterID].names;
        // get elements
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        var currentDots = graph.selectAll('.current-dot');
        var paths = graph.selectAll('.trajectory');
        var historyDots = graph.selectAll('.history-dot');
        // only show these names, hide others
        currentDots.filter(function (d, i) { return !names.includes(d); })
            .attr('visibility', 'hidden');
        paths.filter(function (d, i) { return !names.includes(d); })
            .attr('visibility', 'hidden');
        historyDots.filter(function (d, i) { return !names.includes(d); })
            .attr('visibility', 'hidden');
    }
    resetGraph(event) {
        // make all element visible
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas');
        var outsideSolutionTag = graph.selectAll('.solution-tag').selectAll('text').filter(function (d, i) { return this === event.target; }).empty();
        var outsideUserbox = d3__WEBPACK_IMPORTED_MODULE_1__.selectAll('.userbox').filter(function (d, i) { return this === event.target.parentElement; }).empty();
        if (outsideSolutionTag && outsideUserbox) {
            var currentDots = graph.selectAll('.current-dot');
            var paths = graph.selectAll('.trajectory');
            var historyDots = graph.selectAll('.history-dot');
            // only show these names, hide others
            currentDots.attr('visibility', 'visible');
            paths.attr('visibility', 'visible');
            historyDots.attr('visibility', 'visible');
        }
    }
    initGroup() {
        var activeUsers = this.props.activeUsers;
        var clusterIDs = this.props.clusterIDs;
        var scope = this;
        const WIDTH = this.props.width;
        const HEIGHT = this.props.height;
        const graph = d3__WEBPACK_IMPORTED_MODULE_1__.select('.viz-canvas')
            .attr('width', WIDTH)
            .attr('height', HEIGHT);
        // add brush to svg
        graph.append('g')
            .attr('class', 'brush')
            .call(d3__WEBPACK_IMPORTED_MODULE_1__.brush()
            .extent([[0, 0], [WIDTH * 0.8, HEIGHT]])
            .on("start brush end", function (event) {
            scope.updateBrush(scope, event);
        }), null);
        // draw init dots
        var dots = graph.selectAll('.current-dot')
            .data(activeUsers)
            .enter()
            .append('g')
            .attr('class', 'current-dot')
            .attr('id', function (d, i) { return d; });
        dots.append('circle')
            .attr('r', 2)
            .attr('cx', '0')
            .attr('cy', '0')
            .attr('fill', function (d, i) { return 'red'; });
        // add a path for each dot
        var paths = graph.selectAll('.trajectory')
            .data(activeUsers)
            .enter()
            .append('g')
            .attr('class', 'trajectory')
            .attr('id', function (d, i) { return d; });
        paths.append('path')
            .attr('d', function (d, i) { return scope.paths[d].toString(); })
            .style('stroke', 'gray')
            .style('stroke-width', '0.1')
            .style('fill', 'none');
        // add a group of history dots for each user
        graph.selectAll('.history-dot')
            .data(activeUsers)
            .enter()
            .append('g')
            .attr('class', 'history-dot')
            .attr('id', function (d, i) { return d; });
        // draw correct solution tags
        var tags = graph.selectAll('.solution-tag')
            .data(clusterIDs)
            .enter()
            .append('g')
            .attr('class', 'solution-tag')
            .attr('id', function (d, i) { return d; });
        tags.append('text')
            .text(function (d, i) { return `Solution ${i}`; })
            .attr('x', WIDTH * 0.8)
            .attr('y', function (d, i) { return HEIGHT / clusterIDs.length * (i + 1); })
            .attr('fill', 'black')
            .on('mouseover', function (event, d) {
            scope.props.circleMouseOverFn(d, scope.clusterProgress[d].correct.map((value) => { return scope.userCode[value]; }), scope.clusterProgress[d].incorrect.map((value) => { return scope.userCode[value]; }), scope.clusterProgress[d].correct, scope.clusterProgress[d].incorrect);
        })
            .on('click', function (event, d) {
            scope.focusSolution(scope, d);
        });
        // append progress bar to tag
        var wScale = (0,d3_scale__WEBPACK_IMPORTED_MODULE_3__["default"])().domain([0, 1]).range([0, WIDTH * 0.1]);
        var progressBars = graph.selectAll('.progress-bar')
            .data(clusterIDs)
            .enter()
            .append('g')
            .attr('class', 'progress-bar')
            .attr('id', function (d, i) { return d; });
        progressBars.append('rect')
            .attr('x', WIDTH * 0.9)
            .attr('y', function (d, i) { return HEIGHT / clusterIDs.length * (i + 0.5); })
            .attr('width', function (d, i) { return wScale(scope.clusterProgress[d].correct.length / (scope.clusterProgress[d].correct.length + scope.clusterProgress[d].incorrect.length + 0.0001)); })
            .attr('height', HEIGHT / clusterIDs.length * 0.5)
            .attr('fill', 'green');
        d3__WEBPACK_IMPORTED_MODULE_1__.select('body').on('click', function (event, d) {
            scope.resetGraph(event);
        });
    }
    componentDidMount() {
        this.initGroup();
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { id: '2d-viz-canvas', className: 'viz-canvas' });
    }
}



/***/ }),

/***/ "./lib/solutionWidget.js":
/*!*******************************!*\
  !*** ./lib/solutionWidget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SolutionViewModel": () => (/* binding */ SolutionViewModel),
/* harmony export */   "SolutionViewWidget": () => (/* binding */ SolutionViewWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
// import { VDomRenderer, VDomModel, UseSignal } from '@jupyterlab/apputils';

// import { CodeBlock } from "react-code-blocks";

class SolutionViewModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor(displayAll = false) {
        super();
        this.solutions = new Map();
        this.outputs = new Map();
        this.activeUsers = [];
        this.displayAll = displayAll;
    }
    setSolution(name, solution, masterCopy) {
        if (this.solutions.has(name) && solution !== this.solutions.get(name)) {
            if (!this.activeUsers.includes(name)) {
                this.activeUsers.push(name);
            }
            this.solutions.set(name, solution);
            this.stateChanged.emit();
        }
        else {
            if (this.displayAll) {
                if (!this.activeUsers.includes(name)) {
                    this.activeUsers.push(name);
                }
                this.solutions.set(name, solution);
                this.stateChanged.emit();
            }
            else {
                this.solutions.set(name, solution);
            }
        }
    }
    setOutput(name, outputs) {
        this.outputs.set(name, outputs);
        this.stateChanged.emit();
    }
}
class SolutionViewWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model) {
        super(model);
        this.addClass('jp-ReactWidget');
        this.addClass('sideview');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null);
        // return <div> 
        //     <UseSignal signal={this.model.stateChanged} >
        //         {(): JSX.Element => {
        //             return <div>
        //                 {
        //                     this.model.activeUsers.map((name) => {
        //                         return <div>
        //                             <div className='name-label'>
        //                                 <span>{name}</span>
        //                             </div>
        //                             <CodeBlock
        //                             text={this.model.solutions.get(name)}
        //                             language={"python"}
        //                             showLineNumbers={false}
        //                             />
        //                             <div  className='output'>
        //                                 <span>{this.model.outputs.get(name)?.slice(-1)[0]}</span>
        //                             </div>
        //                         </div>
        //                     })
        //                 }
        //             </div>
        //         }}
        //     </UseSignal>
        // </div> 
    }
}



/***/ }),

/***/ "./lib/timelineWidget.js":
/*!*******************************!*\
  !*** ./lib/timelineWidget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TimeLine": () => (/* binding */ TimeLine)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(d3__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var d3_scale__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! d3-scale */ "./node_modules/d3-scale/src/log.js");
/* harmony import */ var react_dom_server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom/server */ "./node_modules/react-dom/server.browser.js");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-syntax-highlighter */ "webpack/sharing/consume/default/react-syntax-highlighter/react-syntax-highlighter?18b7");
/* harmony import */ var react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _color__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./color */ "./lib/color.js");






;
;
;
class TimeLine extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.width = 400;
        this.height = 200;
        if ('width' in props) {
            this.width = props.width;
        }
        if ('height' in props) {
            this.height = props.height;
        }
        this.state = {
            lanes: props.lanes,
        };
    }
    componentDidMount() {
        // create tooltip item
        d3__WEBPACK_IMPORTED_MODULE_1__.select('.timeline')
            .append('div')
            .classed('tooltip', true)
            .style("position", "fixed")
            .style("visibility", "hidden")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("white-space", "pre-line")
            .html("");
    }
    componentDidUpdate() {
        // set tooltip animation for each event item
        var tooltip = d3__WEBPACK_IMPORTED_MODULE_1__.select('.tooltip');
        var scope = this;
        d3__WEBPACK_IMPORTED_MODULE_1__.selectAll('.event-item')
            .each(function (p, j) {
            const code = d3__WEBPACK_IMPORTED_MODULE_1__.select(this).attr('data-tooltip');
            d3__WEBPACK_IMPORTED_MODULE_1__.select(this)
                .on("mouseover", function () {
                if (!scope.props.tooltipMode)
                    return;
                // set html for tooltip
                const node = (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react_syntax_highlighter__WEBPACK_IMPORTED_MODULE_3___default()), { language: 'python' }, code));
                const html = (0,react_dom_server__WEBPACK_IMPORTED_MODULE_2__.renderToString)(node);
                return tooltip.style("visibility", "visible")
                    .html(html);
            })
                .on("mousemove", function (event) {
                if (!scope.props.tooltipMode)
                    return;
                return tooltip.style("top", (event.clientY) + "px").style("left", (event.clientX) + "px");
            })
                .on("mouseout", function () {
                if (!scope.props.tooltipMode)
                    return;
                return tooltip.style("visibility", "hidden").html("");
            });
        });
    }
    barColor(correct, errorType) {
        if (correct) {
            return _color__WEBPACK_IMPORTED_MODULE_4__.COLOR_MAP.correct;
        }
        else if (errorType) {
            return _color__WEBPACK_IMPORTED_MODULE_4__.COLOR_MAP[errorType];
        }
        else {
            return _color__WEBPACK_IMPORTED_MODULE_4__.COLOR_MAP["cluster-1"];
        }
    }
    render() {
        var domainStart = undefined;
        var domainEnd = undefined;
        this.state.lanes.forEach((name) => {
            if (!this.props.events.has(name) || this.props.events.get(name).length === 0) {
                return;
            }
            // set domainStart
            domainStart = domainStart === undefined ? this.props.events.get(name)[0].startTime : Math.min(domainStart, this.props.events.get(name)[0].startTime);
            // set domainEnd
            domainEnd = domainEnd === undefined ? this.props.events.get(name)[this.props.events.get(name).length - 1].startTime : Math.max(domainEnd, this.props.events.get(name)[this.props.events.get(name).length - 1].startTime);
        });
        const timeScaler = (0,d3_scale__WEBPACK_IMPORTED_MODULE_5__["default"])()
            .domain((domainStart !== undefined && domainEnd !== undefined) ? [domainStart + 1, domainEnd + 1] : [1, 10])
            .range([30, this.width - 30]);
        const logScaler = (0,d3_scale__WEBPACK_IMPORTED_MODULE_5__["default"])()
            .domain([1, 1000])
            // .range([10,40])
            .range([this.height / (this.state.lanes.length + 1) * 0.25, this.height / (this.state.lanes.length + 1)]);
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: this.width, height: this.height },
            this.state.lanes.map((value, index) => {
                return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { key: index },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { className: 'x-axis', id: value, d: `M0 ${this.height / this.state.lanes.length * (index + 1)} L${this.width} ${this.height / this.state.lanes.length * (index + 1)}`, stroke: this.props.queryFilter[value] === 0 ? "black" : "teal" }));
            }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { id: "events" }, this.state.lanes.map((name) => {
                return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { key: name },
                    (this.props.events.has(name) ? this.props.events.get(name) : []).map((event, index) => {
                        const ref = react__WEBPACK_IMPORTED_MODULE_0___default().createRef();
                        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { key: index },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("rect", { ref: ref, className: 'event-item', height: logScaler(event.radius), width: 5, x: timeScaler(event.startTime + 1), y: this.height / this.state.lanes.length * ((this.state.lanes.indexOf(name)) + 1) - logScaler(event.radius), "data-index": index, "data-title": name, "data-tooltip": event.tooltip, 
                                // stroke={event.correct? 'green': 'red'}
                                fill: this.barColor(event.correct, event.errorType), fillOpacity: '90%', onMouseOver: this.props.dotOnHover, onClick: this.props.dotOnClick }));
                    }),
                    (this.props.typingActivityMode && this.props.typingActivities.has(name) ? this.props.typingActivities.get(name) : []).map((activity, index) => {
                        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { key: index },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("rect", { className: 'typing-activity', height: 5, width: 0.5, x: timeScaler(activity.timestamp + 1), y: this.height / this.state.lanes.length * ((this.state.lanes.indexOf(name)) + 1) - 5, fill: 'black' }));
                    }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("circle", { r: 10, cx: this.width - 5, cy: this.height / this.state.lanes.length * ((this.state.lanes.indexOf(name)) + 0.5), fill: 'gray', display: this.props.typingStatus.get(name) ? 'block' : 'none' }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("rect", { className: 'timeline-button', height: 10, width: 10, x: 5, y: this.height / this.state.lanes.length * ((this.state.lanes.indexOf(name)) + 1) - 5, "data-title": name, onClick: this.props.similarButtonOnClick }));
            })));
    }
}



/***/ }),

/***/ "./lib/toolbar.js":
/*!************************!*\
  !*** ./lib/toolbar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/user */ "webpack/sharing/consume/default/@jupyterlab/user");
/* harmony import */ var _jupyterlab_user__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! uuid */ "./node_modules/uuid/index.js");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(uuid__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _cellTypeButton__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./cellTypeButton */ "./lib/cellTypeButton.js");







function newOnMetadataChanged(panel, cell, user) {
    function fn(model, args) {
        switch (args.key) {
            case 'nbranch':
                for (var cell of panel.content.widgets) {
                    console.log(cell);
                    if (cell.model.metadata.has('owner') && cell.model.metadata.get('owner') !== user.name) {
                        cell.node.style.display = 'none';
                    }
                }
                break;
            default:
                break;
        }
    }
    return fn;
}
console.log(newOnMetadataChanged);
class ButtonExtension {
    constructor(user) {
        this.user = user;
    }
    createNew(widget, context) {
        const dropdownButton = new _cellTypeButton__WEBPACK_IMPORTED_MODULE_6__.CellTypeSwitcher(widget.content);
        widget.toolbar.insertItem(10, 'type', dropdownButton);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            dropdownButton.dispose();
        });
    }
}
const plugintest = {
    id: 'ovservacode:test-plugin',
    autoStart: true,
    requires: [_jupyterlab_user__WEBPACK_IMPORTED_MODULE_3__.ICurrentUser, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: activatePluginTest
};
function saveExercise(app) {
    function fn() {
        var _a, _b, _c, _d;
        console.log('save exercise fn');
        const { shell } = app;
        const nbPanel = shell.currentWidget;
        if ((_a = nbPanel.model) === null || _a === void 0 ? void 0 : _a.metadata.has('exerciseID')) {
            alert("Exercise ID already exists");
        }
        else {
            var exerciseName = prompt("Please enter exercise name");
            if (exerciseName === null) {
                alert("Exercise name can not be empty");
            }
            else {
                // assign uuid to this notebook
                (_b = nbPanel.model) === null || _b === void 0 ? void 0 : _b.metadata.set('exerciseID', (0,uuid__WEBPACK_IMPORTED_MODULE_5__.v4)());
                (_c = nbPanel.model) === null || _c === void 0 ? void 0 : _c.metadata.set('exerciseName', exerciseName);
                console.log((_d = nbPanel.model) === null || _d === void 0 ? void 0 : _d.metadata);
            }
        }
    }
    return fn;
}
function clearExercise(app) {
    function fn() {
        var _a, _b;
        console.log('clear exercise fn');
        const { shell } = app;
        const nbPanel = shell.currentWidget;
        (_a = nbPanel.model) === null || _a === void 0 ? void 0 : _a.metadata.delete('exerciseID');
        console.log((_b = nbPanel.model) === null || _b === void 0 ? void 0 : _b.metadata);
    }
    return fn;
}
function activatePluginTest(app, user, palette, rendermime, restorer) {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension(user));
    const { commands } = app;
    commands.addCommand('observacode/save-exercise:save', {
        execute: saveExercise(app),
        label: 'Save Exercise'
    });
    commands.addCommand('observacode/save-exercise:clear', {
        execute: clearExercise(app),
        label: 'Clear Exercise'
    });
    palette.addItem({
        command: 'observacode/save-exercise:save',
        category: 'Settings'
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugintest);


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4.85a67ca187d35db5659b.js.map