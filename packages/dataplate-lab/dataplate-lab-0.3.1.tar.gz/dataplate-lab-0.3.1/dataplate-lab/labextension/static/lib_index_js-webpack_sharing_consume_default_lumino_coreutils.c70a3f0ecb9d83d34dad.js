"use strict";
(self["webpackChunkdataplate_lab"] = self["webpackChunkdataplate_lab"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils"],{

/***/ "./lib/components/Alert.js":
/*!*********************************!*\
  !*** ./lib/components/Alert.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Alert": () => (/* binding */ Alert)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_Alert__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/Alert */ "./lib/style/Alert.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */


class Alert extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: `${_style_Alert__WEBPACK_IMPORTED_MODULE_1__.alert} ${this.alertClass(this.props.type)}` }, this.props.message);
    }
    alertClass(type) {
        const classes = {
            error: _style_Alert__WEBPACK_IMPORTED_MODULE_1__.alertDanger,
            alert: _style_Alert__WEBPACK_IMPORTED_MODULE_1__.alertWarning,
            notice: _style_Alert__WEBPACK_IMPORTED_MODULE_1__.alertInfo,
            success: _style_Alert__WEBPACK_IMPORTED_MODULE_1__.alertSuccess,
        };
        return classes[type] || classes.success;
    }
}


/***/ }),

/***/ "./lib/components/DatasetList.js":
/*!***************************************!*\
  !*** ./lib/components/DatasetList.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatasetList": () => (/* binding */ DatasetList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _SimpleTable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./SimpleTable */ "./lib/components/SimpleTable.js");
/* harmony import */ var _style_tables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/tables */ "./lib/style/tables.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */



const Headers = ['Name', 'Type'];
class DatasetList extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.extractRow = (dataset) => {
            return [
                dataset.name,
                dataset.type,
            ];
        };
        this.state = { datasets: props.model.datasets, error: null };
        props.model.datasetsChanged.connect(this.onDatasetsChanged, this);
    }
    onDatasetsChanged(_, datasetInfo) {
        this.setState({ datasets: datasetInfo.datasets, error: datasetInfo.error });
    }
    componentWillUnmount() {
        this.props.model.datasetsChanged.disconnect(this.onDatasetsChanged, this);
    }
    render() {
        let content;
        if (this.state.datasets) {
            // sometimes it seems that render gets called before the constructor ???
            const rows = this.state.datasets.map(this.extractRow);
            if (rows.length === 0) {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_1__.tableEmptyClass }, "No Datasets are allowed");
            }
            else {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_2__.SimpleTable, { headings: Headers, rows: rows });
            }
        }
        else if (this.state.error) {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_1__.tableEmptyClass },
                "Error retrieving datasets: ",
                this.state.error);
        }
        else {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_1__.tableEmptyClass }, "Loading datasets...");
        }
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_2__.SimpleTablePage, { title: "My Allowed Dataset List" }, content);
    }
}


/***/ }),

/***/ "./lib/components/InputColumn.js":
/*!***************************************!*\
  !*** ./lib/components/InputColumn.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InputColumn": () => (/* binding */ InputColumn),
/* harmony export */   "LabeledNumberInput": () => (/* binding */ LabeledNumberInput),
/* harmony export */   "LabeledPasswordInput": () => (/* binding */ LabeledPasswordInput),
/* harmony export */   "LabeledTextInput": () => (/* binding */ LabeledTextInput),
/* harmony export */   "LabeledTextInputMaxWidth": () => (/* binding */ LabeledTextInputMaxWidth)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_InputColumn__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/InputColumn */ "./lib/style/InputColumn.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */


class InputColumn extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("table", { className: _style_InputColumn__WEBPACK_IMPORTED_MODULE_1__.inputColumnClass + ' inputColumnMarker' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tbody", null, this.props.children)));
    }
}
class LabeledTextInput extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null, this.props.label),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", onChange: this.props.onChange, value: this.props.value, title: this.props.title, placeholder: this.props.placeholder }))));
    }
}
class LabeledTextInputMaxWidth extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null, this.props.label),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", onChange: this.props.onChange, value: this.props.value, title: this.props.title, placeholder: this.props.placeholder, style: { width: '200px' } }))));
    }
}
class LabeledNumberInput extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null, this.props.label),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", onChange: this.props.onChange, value: this.props.value, title: this.props.title, onKeyPress: (event) => {
                        if (!/[0-9]/.test(event.key)) {
                            event.preventDefault();
                        }
                    } }))));
    }
}
class LabeledPasswordInput extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null, this.props.label),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "password", onChange: this.props.onChange, value: this.props.value, title: this.props.title }))));
    }
}


/***/ }),

/***/ "./lib/components/ParameterEditor.js":
/*!*******************************************!*\
  !*** ./lib/components/ParameterEditor.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ParameterEditor": () => (/* binding */ ParameterEditor)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_ParameterEditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/ParameterEditor */ "./lib/style/ParameterEditor.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */


const METADATA_KEY = 'dataplate-lab';
class ParameterEditor extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.onAddClick = () => {
            const params = this.state.parameters;
            params.push({ name: '', value: '' });
            this.setState({ parameters: params });
        };
        this.onMinusClick = (i) => {
            const params = this.state.parameters;
            params.splice(i, 1);
            this.setState({ parameters: params });
            this.computeNewJSON(true);
        };
        this.nameChanged = (e, i) => {
            const params = this.state.parameters;
            params[i].name = e.target.value;
            this.setState({ parameters: params }, () => this.computeNewJSON(true));
        };
        this.valueChanged = (e, i) => {
            const params = this.state.parameters;
            params[i].value = e.target.value;
            this.setState({ parameters: params }, () => this.computeNewJSON(true));
        };
        this.notebookPanelChanged = props.notebookPanelChanged;
        this.currentNotebookPanel = props.notebookPanel;
        this.currentMetadata = null;
        this.onChange = props.onChange;
        this.state = { parameters: this.extractSavedParameters() };
        this.computeNewJSON(false);
        this.updateParameterTracker();
        this.notebookPanelChanged.connect(this.onNotebookPanelChanged, this);
    }
    componentWillUnmount() {
        this.notebookPanelChanged.disconnect(this.onNotebookPanelChanged, this);
    }
    onNotebookPanelChanged(_, notebookPanel) {
        this.currentNotebookPanel = notebookPanel;
        this.getSavedParameters();
        this.updateParameterTracker();
    }
    updateParameterTracker() {
        if (this.currentMetadata) {
            this.currentMetadata.changed.disconnect(this.getSavedParameters);
        }
        const panel = this.currentNotebookPanel;
        if (panel) {
            this.currentMetadata = panel.model.metadata;
            this.currentMetadata.changed.connect(this.getSavedParameters, this);
        }
    }
    extractSavedParameters() {
        let result = [];
        const panel = this.currentNotebookPanel;
        if (panel) {
            const metadata = panel.model.metadata.get(METADATA_KEY);
            const params = metadata && metadata['saved_parameters'];
            if (params) {
                result = params;
            }
        }
        return result;
    }
    getSavedParameters() {
        if (this.currentNotebookPanel) {
            this.setState({ parameters: this.extractSavedParameters() }, () => this.computeNewJSON(false));
        }
    }
    setSavedParameters() {
        const panel = this.currentNotebookPanel;
        if (panel) {
            const metadata = panel.model.metadata.get(METADATA_KEY) || {};
            metadata['saved_parameters'] = this.state.parameters;
            panel.model.metadata.set(METADATA_KEY, metadata);
            panel.model.dirty = true; // metadata.set should do this, but doesn't
        }
    }
    render() {
        let block;
        if (!this.state.parameters || this.state.parameters.length === 0) {
            block = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: _style_ParameterEditor__WEBPACK_IMPORTED_MODULE_1__.parameterEditorNoParametersClass }, "No parameters defined. Press \u201C+\u201D to add parameters."));
        }
        else {
            block = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("table", null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("thead", null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("tr", null,
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("th", null, "Name"),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("th", null, "Value"))),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("tbody", null, this.state.parameters.map((p, i) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement("tr", { key: `parameter-${i}` },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { type: "text", onChange: (e) => this.nameChanged(e, i), value: p.name, title: "Parameter" })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { type: "text", onChange: (e) => this.valueChanged(e, i), value: p.value, title: "Value" })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("td", { className: _style_ParameterEditor__WEBPACK_IMPORTED_MODULE_1__.closeIcon, onClick: () => this.onMinusClick(i) })))))));
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null, "Parameters:"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_ParameterEditor__WEBPACK_IMPORTED_MODULE_1__.parameterEditorTableClass },
                block,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(SmallButton, { onClick: this.onAddClick, label: "+", tooltip: "Add a parameter" }))));
    }
    computeNewJSON(updateMetadata) {
        let valid = true;
        const seen = new Set();
        const result = [];
        const nameErrors = {};
        const valueErrors = {};
        this.state.parameters.forEach((element, idx) => {
            if (element.name.length === 0) {
                valid = false;
                nameErrors[idx] = 'Name must be specified';
            }
            else {
                if (element.name in seen) {
                    valid = false;
                    nameErrors[idx] = 'Duplicate parameter';
                }
                else {
                    let val = element.value;
                    // this mostly exists to let folks pass numbers as numbers, but in theory they can pass any JSON through.
                    try {
                        val = JSON.parse(val);
                    }
                    catch (SyntaxError) { } // eslint-disable-line  no-empty
                    result.push({ name: element.name, value: val });
                    seen.add(element.name);
                }
            }
        });
        this.parametersObject = valid ? result : null;
        this.nameErrors = nameErrors;
        this.valueErrors = valueErrors;
        this.onChange(this);
        if (updateMetadata) {
            this.setSavedParameters();
        }
    }
    get value() {
        return this.parametersObject;
    }
    get errors() {
        return { nameErrors: this.nameErrors, valueErrors: this.valueErrors };
    }
}
function SmallButton(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { type: "button", className: _style_ParameterEditor__WEBPACK_IMPORTED_MODULE_1__.parameterEditorAddItemClass, onClick: props.onClick, value: props.label, title: props.tooltip }));
}


/***/ }),

/***/ "./lib/components/ProjectList.js":
/*!***************************************!*\
  !*** ./lib/components/ProjectList.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProjectList": () => (/* binding */ ProjectList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _SimpleTable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./SimpleTable */ "./lib/components/SimpleTable.js");
/* harmony import */ var _style_tables__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/tables */ "./lib/style/tables.js");
/* harmony import */ var _SubProjectsDialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./SubProjectsDialog */ "./lib/components/SubProjectsDialog.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




function viewSubProjects(projectName, serverURL, accessKey) {
    return (0,_SubProjectsDialog__WEBPACK_IMPORTED_MODULE_1__.showSubProjects)(projectName, serverURL, accessKey);
}
const Headers = ['Name', 'Created', 'LastModified', ''];
class ProjectList extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.extractRow = (project) => {
            return [
                project.Name,
                project.Created,
                project.LastModified,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { key: project.Name, onClick: viewSubProjects(project.Name, this.props.model.serverURL, this.props.model.accessKey), className: _style_tables__WEBPACK_IMPORTED_MODULE_2__.tableLinkClass }, "Sub-Projects")
            ];
        };
        this.state = { projects: props.model.projects, error: null };
        props.model.projectsChanged.connect(this.onProjectsChanged, this);
    }
    onProjectsChanged(_, projectInfo) {
        this.setState({ projects: projectInfo.projects, error: projectInfo.error });
    }
    componentWillUnmount() {
        this.props.model.projectsChanged.disconnect(this.onProjectsChanged, this);
    }
    render() {
        let content;
        if (this.state.projects) {
            // sometimes it seems that render gets called before the constructor ???
            const rows = this.state.projects.map(this.extractRow);
            if (rows.length === 0) {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_2__.tableEmptyClass }, "No Projects are available - or no proper permission");
            }
            else {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_3__.SimpleTable, { headings: Headers, rows: rows });
            }
        }
        else if (this.state.error) {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_2__.tableEmptyClass },
                "Error retrieving projects: ",
                this.state.error);
        }
        else {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_2__.tableEmptyClass }, "Loading projects...");
        }
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_3__.SimpleTablePage, { title: "Projects List" }, content);
    }
}


/***/ }),

/***/ "./lib/components/ReadonlyNotebookHeader.js":
/*!**************************************************!*\
  !*** ./lib/components/ReadonlyNotebookHeader.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ReadonlyNotebookHeader": () => (/* binding */ ReadonlyNotebookHeader)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* harmony import */ var classnames__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! classnames */ "webpack/sharing/consume/default/classnames/classnames");
/* harmony import */ var classnames__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(classnames__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _util_testId__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../util/testId */ "./lib/util/testId.js");
/* harmony import */ var _util_files__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../util/files */ "./lib/util/files.js");
/* harmony import */ var _style_icons__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons */ "./lib/style/icons.js");
/* harmony import */ var _RunDetailsDialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./RunDetailsDialog */ "./lib/components/RunDetailsDialog.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */








const messageClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    flex: '1 1 auto',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    marginRight: '12px',
});
const messageTitleClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    fontWeight: 'bold',
    marginBottom: '4px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
});
const messageBodyClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    overflow: 'hidden',
    textOverflow: 'ellipsis',
});
const actionClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    flex: '0 0 auto',
    marginLeft: 'auto',
    display: 'flex',
});
const snapshotDetailsButtonClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    background: 'var(--jp-layout-color1)',
    color: 'var(--jp-ui-font-color1) !important',
    border: 'var(--jp-border-width) solid var(--jp-border-color1) !important',
    lineHeight: 'calc(32px - 2 * var(--jp-border-width)) !important',
    marginRight: '8px',
    $nest: {
        '&:hover': {
            background: 'var(--jp-layout-color2)',
            borderColor: 'var(--jp-border-color0)',
        },
        '&:active': {
            background: 'var(--jp-layout-color3)',
            borderColor: 'var(--jp-border-color2)',
        },
    },
});
const infoIconClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    marginRight: '12px',
    alignSelf: 'flex-start',
    $nest: {
        svg: {
            height: '24px',
            width: '24px',
            stroke: 'var(--jp-info-color2)',
        },
    },
});
const ReadonlyNotebookHeader = ({ app, document, jobName }) => {
    /** Copies the file to the root JupyterLab directory with a unique filename, and opens it */
    const handleCopy = async () => {
        const { name } = document;
        const destinationPath = await (0,_util_files__WEBPACK_IMPORTED_MODULE_4__.getUniqueFilename)(app, name);
        await app.serviceManager.contents.save(destinationPath, document);
        app.commands.execute('docmanager:open', { path: destinationPath });
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon.resolveReact, { icon: _style_icons__WEBPACK_IMPORTED_MODULE_5__.ICON_INFO_CIRCLE, className: infoIconClass }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: messageClass },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: messageTitleClass }, "This is a read-only preview"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: messageBodyClass }, "To run and edit the notebook, create a copy to your workspace.")),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: actionClass },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", Object.assign({ type: "button", className: classnames__WEBPACK_IMPORTED_MODULE_2___default()('jp-mod-styled', snapshotDetailsButtonClass), onClick: (0,_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_6__.showRunDetails)(jobName, "", "") }, (0,_util_testId__WEBPACK_IMPORTED_MODULE_7__.testId)('snapshot-details-button')), "Execution details"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", Object.assign({ type: "button", className: "jp-mod-styled jp-mod-accept", onClick: handleCopy }, (0,_util_testId__WEBPACK_IMPORTED_MODULE_7__.testId)('copy-button')), "Create a copy"))));
};


/***/ }),

/***/ "./lib/components/RuleList.js":
/*!************************************!*\
  !*** ./lib/components/RuleList.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RulesList": () => (/* binding */ RulesList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _SimpleTable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./SimpleTable */ "./lib/components/SimpleTable.js");
/* harmony import */ var _style_tables__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/tables */ "./lib/style/tables.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */






const Headers = ['Name', 'Notebook', 'Parameters', 'Schedule', 'Event', 'Image', 'Instance', 'Role', 'State', ''];
class RulesList extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.extractRow = (rule) => {
            return [
                rule.name,
                rule.notebook,
                this.formatParameters(rule.parameters),
                rule.schedule,
                rule.event_pattern,
                rule.image,
                rule.instance,
                rule.role,
                rule.state,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { key: rule.name, onClick: this.deleteRule(rule.name), className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableLinkClass }, "Delete"),
            ];
        };
        this.state = { rules: props.model.rules, error: null };
        props.model.rulesChanged.connect(this.onRulesChanged, this);
    }
    onRulesChanged(_, ruleInfo) {
        this.setState({ rules: ruleInfo.rules, error: ruleInfo.error });
    }
    componentWillUnmount() {
        this.props.model.rulesChanged.disconnect(this.onRulesChanged, this);
    }
    // eslint-disable-next-line  @typescript-eslint/no-explicit-any
    formatParameters(params) {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null, Object.entries(params).map(([k, v]) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { key: `param-${k}` }, `${k}: ${JSON.stringify(v)}`)))));
    }
    render() {
        let content;
        if (this.state.rules) {
            // sometimes it seems that render gets called before the constructor ???
            const rows = this.state.rules.map(this.extractRow);
            if (rows.length === 0) {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass }, "No schedules defined");
            }
            else {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_5__.SimpleTable, { headings: Headers, rows: rows });
            }
        }
        else if (this.state.error) {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass },
                "Error retrieving rules: ",
                this.state.error);
        }
        else {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass }, "Loading rules...");
        }
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_5__.SimpleTablePage, { title: "Schedule and Event Rules" }, content);
    }
    deleteRule(rule) {
        return async () => {
            const deleteBtn = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.warnButton({ label: 'Delete' });
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                title: 'Delete Rule?',
                body: `Do you want to delete the rule ${rule}?`,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.cancelButton(), deleteBtn],
            });
            if (result.button.accept) {
                console.log(`deleting rule ${rule}`);
                const request = {
                    serverURL: this.props.model.serverURL,
                    accessKey: this.props.model.accessKey,
                };
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'schedule', rule), { method: 'DELETE', body: JSON.stringify(request) }, settings);
                if (!response.ok) {
                    const error = (await response.json());
                    let errorMessage;
                    if (error.error) {
                        errorMessage = error.error.message;
                    }
                    else {
                        errorMessage = JSON.stringify(error);
                    }
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                        title: 'Error deleting schedule',
                        body: react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, errorMessage),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: 'Close' })],
                    });
                    return;
                }
                this.props.model.refresh();
                return true;
            }
            return false;
        };
    }
}


/***/ }),

/***/ "./lib/components/RunDetailsDialog.js":
/*!********************************************!*\
  !*** ./lib/components/RunDetailsDialog.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunDetailsDialogBody": () => (/* binding */ RunDetailsDialogBody),
/* harmony export */   "processDate": () => (/* binding */ processDate),
/* harmony export */   "processRuntime": () => (/* binding */ processRuntime),
/* harmony export */   "showRunDetails": () => (/* binding */ showRunDetails)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/RunDetailsDialog */ "./lib/style/RunDetailsDialog.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */





async function loadDescription(jobName, serverURL, accessKey) {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    const request = {
        serverURL: serverURL,
        accessKey: accessKey,
    };
    const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'run', jobName), { method: 'POST', body: JSON.stringify(request) }, settings);
    if (!response.ok) {
        const error = (await response.json());
        if (error.error) {
            throw Error(error.error.message);
        }
        else {
            throw Error(JSON.stringify(error));
        }
    }
    const data = (await response.json());
    return data.run;
}
/**
 * Process the date string returned by the server for the start time into something we can
 * present in the UI. One option is that the server will not yet have set a date. This happens
 * if we've kicked off the job but SageMaker processing is still starting it.
 *
 * @param d The date string returned by the server
 * @param status The processing job status
 */
function processDate(d, status) {
    if (d == null) {
        if (status === 'InProgress') {
            return 'Starting';
        }
        else {
            return '';
        }
    }
    else {
        const c = d.toString().match(/^([-: \d]+)(\.\d+)?([+-])(\d+):(\d+)/);
        if (Array.isArray(c)) {
            if (c.length > 0) {
                const date = new Date(c[1].replace(/-/g, '/'));
                let offset = parseInt(c[4]) * 60 + parseInt(c[5]);
                if (c[3] === '-') {
                    offset = -offset;
                }
                offset += date.getTimezoneOffset();
                date.setMinutes(date.getMinutes() - offset);
                const result = date.toLocaleString();
                return result;
            }
            else {
                // var length = d.length-7;
                var date = parseInt((d.toString())); //.substring(6,length)
                return (new Date(date).toLocaleString());
            }
        }
        else {
            // var length = d.length-7;
            var date = parseInt((d.toString())); //.substring(6,length)
            return (new Date(date).toLocaleString());
        }
    }
}
function processRuntime(d, status) {
    if (d == null) {
        if (status === 'InProgress') {
            return 'Starting';
        }
        else {
            return '';
        }
    }
    else {
        const c = d.toString().match(/^([-: \d]+)(\.\d+)/);
        if (Array.isArray(c)) {
            if (c.length > 0) {
                return (d.toString());
            }
            else {
                var date = parseInt((d.toString()));
                var date_date = new Date(date);
                var offset = date_date.getTimezoneOffset();
                let cur_min = date_date.getHours() * 60 + date_date.getMinutes();
                var new_date = new Date(date_date);
                new_date.setHours(0);
                new_date.setMinutes(cur_min + offset);
                var datastr = new_date.toTimeString();
                datastr = datastr.split(' ')[0];
                var length = datastr.length;
                if (datastr.endsWith('AM') || datastr.endsWith('PM')) {
                    return (datastr.slice(0, length - 3));
                }
                else {
                    return (datastr);
                }
            }
        }
        else {
            var date = parseInt((d.toString()));
            var date_date = new Date(date);
            var offset = date_date.getTimezoneOffset();
            let cur_min = date_date.getHours() * 60 + date_date.getMinutes();
            var new_date = new Date(date_date);
            new_date.setHours(0);
            new_date.setMinutes(cur_min + offset);
            var datastr = new_date.toTimeString();
            datastr = datastr.split(' ')[0];
            var length = datastr.length;
            if (datastr.endsWith('AM') || datastr.endsWith('PM')) {
                return (datastr.slice(0, length - 3));
            }
            else {
                return (datastr);
            }
        }
    }
}
function showRunDetails(jobName, serverURL, accessKey) {
    return async () => {
        let run;
        let error;
        try {
            run = await loadDescription(jobName, serverURL, accessKey);
        }
        catch (e) {
            error = e.message;
        }
        let title;
        if (run) {
            if (run.Rule) {
                title = `Execution from rule "${run.Rule}"`;
            }
            else {
                title = `On-demand notebook execution`;
            }
        }
        else {
            title = 'Error retrieving details';
        }
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
            title: title,
            body: react__WEBPACK_IMPORTED_MODULE_2___default().createElement(RunDetailsDialogBody, { jobName: jobName, description: run, error: error }),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: 'Close' })],
        });
    };
}
const LabeledRow = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("tr", { className: _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.labeledRowClass },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("td", null,
            props.label,
            ":"),
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("td", null, props.content)));
};
class RunDetailsDialogBody extends (react__WEBPACK_IMPORTED_MODULE_2___default().Component) {
    constructor(props) {
        super(props);
        this.state = { runDescription: props.description, error: props.error };
    }
    render() {
        if (this.state.error) {
            return react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", null,
                "Error loading run description: ",
                this.state.error);
        }
        const desc = this.state.runDescription;
        if (!desc) {
            return react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", null, "Loading...");
        }
        let status;
        if (desc.Status === 'Failed') {
            status = `${desc.Status} (${desc.Failure})`;
        }
        else {
            status = desc.Status;
        }
        const s3Locations = (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.kvContainer },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null, "Input:"),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null, desc.Input),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null, "Output:"),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null, desc.Result)));
        const params = this.formatParameters(desc.Parameters);
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.sectionClass },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("header", null,
                    "Notebook \u201C",
                    desc.Notebook,
                    "\u201D run at ",
                    processDate(desc.Created, desc.Status)),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("table", null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Status", content: status }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Parameters", content: params }))),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.sectionClass },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("header", null, "Timings:"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("table", null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Started", content: processDate(desc.Start, desc.Status) }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Ended", content: processDate(desc.End, desc.Status) }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Run time", content: processRuntime(desc.Elapsed, desc.Status) }))),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.sectionClass },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("header", null, "Processing job info:"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("table", null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Job name", content: desc.Job }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Instance type", content: desc.Instance }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "S3 locations", content: s3Locations }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "Container image", content: desc.Image }),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(LabeledRow, { label: "IAM role", content: desc.Role })))));
    }
    formatParameters(params) {
        try {
            // eslint-disable-next-line  @typescript-eslint/no-explicit-any
            const parsed = JSON.parse(params);
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null, Object.entries(parsed).map(([k, v]) => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { key: `param-${k}` }, `${k}: ${JSON.stringify(v)}`)))));
        }
        catch (SyntaxError) {
            return params;
        }
    }
}


/***/ }),

/***/ "./lib/components/RunList.js":
/*!***********************************!*\
  !*** ./lib/components/RunList.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunList": () => (/* binding */ RunList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _SimpleTable__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./SimpleTable */ "./lib/components/SimpleTable.js");
/* harmony import */ var _style_tables__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/tables */ "./lib/style/tables.js");
/* harmony import */ var _widgets_ReadOnlyNotebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../widgets/ReadOnlyNotebook */ "./lib/widgets/ReadOnlyNotebook.js");
/* harmony import */ var _RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./RunDetailsDialog */ "./lib/components/RunDetailsDialog.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */








const basenamePattern = /([^/]*)$/;
function viewDetails(jobName, serverURL, accessKey) {
    return (0,_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.showRunDetails)(jobName, serverURL, accessKey);
}
function openResult(jobName, app, rendermime, serverURL, accessKey) {
    return async () => {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        // const response = await ServerConnection.makeRequest(
        //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'output', jobName),
        //   { method: 'GET' },
        //   settings,
        // );
        const request = {
            serverURL: serverURL,
            accessKey: accessKey,
        };
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'output', jobName), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: 'Error opening notebook',
                body: react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, errorMessage),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Close' })],
            });
            return;
        }
        const info = (await response.json());
        const match = basenamePattern.exec(info.output_object);
        const outputName = match[1];
        const document = {
            name: outputName,
            content: JSON.parse(info.data),
        };
        (0,_widgets_ReadOnlyNotebook__WEBPACK_IMPORTED_MODULE_5__.openReadonlyNotebook)(app, rendermime, document, outputName, jobName);
    };
}
function stopJob(jobName, serverURL, accessKey) {
    return async () => {
        console.log(`Stop job ${jobName}`);
        const request = {
            serverURL: serverURL,
            accessKey: accessKey,
        };
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        // const response = await ServerConnection.makeRequest(
        //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'run', jobName),
        //   { method: 'DELETE' },
        //   settings,
        // );
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'run', jobName), { method: 'DELETE', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: 'Error stopping execution',
                body: react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, errorMessage),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Close' })],
            });
            return;
        }
    };
}
const Headers = ['Rule', 'Notebook', 'Parameters', 'Status', 'Start', 'Elapsed', '', ''];
class RunList extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.extractRow = (run) => {
            const app = this._app;
            const rendermime = this._rendermime;
            const details = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { onClick: viewDetails(run.Job, this.props.model.serverURL, this.props.model.accessKey), className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableLinkClass }, "View Details"));
            let links = null;
            if (run.Status === 'Completed') {
                links = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { onClick: openResult(run.Job, app, rendermime, this.props.model.serverURL, this.props.model.accessKey), className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableLinkClass }, "View Output"));
            }
            else if (run.Status === 'InProgress') {
                links = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { onClick: stopJob(run.Job, this.props.model.serverURL, this.props.model.accessKey), className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableLinkClass }, "Stop Run"));
            }
            return [
                run.Rule,
                run.Notebook,
                this.formatParameters(run.Parameters),
                run.Status,
                (0,_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.processDate)(run.Start, run.Status),
                (0,_RunDetailsDialog__WEBPACK_IMPORTED_MODULE_4__.processRuntime)(run.Elapsed, run.Status),
                details,
                links,
            ];
        };
        this.state = { runs: props.model.runs, error: null };
        this._app = props.app;
        this._rendermime = props.rendermime;
        props.model.runsChanged.connect(this.onRunsChanged, this);
    }
    onRunsChanged(_, runInfo) {
        this.setState({ runs: runInfo.runs, error: runInfo.error });
    }
    componentWillUnmount() {
        this.props.model.runsChanged.disconnect(this.onRunsChanged, this);
    }
    formatParameters(params) {
        try {
            // eslint-disable-next-line  @typescript-eslint/no-explicit-any
            const parsed = JSON.parse(params);
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null, Object.entries(parsed).map(([k, v]) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { key: `param-${k}` }, `${k}: ${JSON.stringify(v)}`)))));
        }
        catch (SyntaxError) {
            return params;
        }
    }
    render() {
        let content;
        if (this.state.runs) {
            // sometimes it seems that render gets called before the constructor ???
            const rows = this.state.runs.map(this.extractRow);
            if (rows.length === 0) {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableEmptyClass }, "No notebooks have been run");
            }
            else {
                content = react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_7__.SimpleTable, { headings: Headers, rows: rows });
            }
        }
        else if (this.state.error) {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableEmptyClass },
                "Error retrieving execution history: ",
                this.state.error);
        }
        else {
            content = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_6__.tableEmptyClass }, "Loading execution history...");
        }
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_7__.SimpleTablePage, { title: "Notebook Execution History" }, content);
    }
}


/***/ }),

/***/ "./lib/components/SchedulePanel.js":
/*!*****************************************!*\
  !*** ./lib/components/SchedulePanel.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SchedulePanel": () => (/* binding */ SchedulePanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _InputColumn__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./InputColumn */ "./lib/components/InputColumn.js");
/* harmony import */ var _ParameterEditor__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ParameterEditor */ "./lib/components/ParameterEditor.js");
/* harmony import */ var _Alert__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./Alert */ "./lib/components/Alert.js");
/* harmony import */ var _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/SchedulePanel */ "./lib/style/SchedulePanel.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */








const KEY = 'dataplate-lab:schedule-sidebar:data';
// convertParameters turns the parameters we use here into a map that the server and containter expect.
// TODO: fix the container to take lists and delete this function so that parameters are always in the order specified
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function convertParameters(params) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const result = {};
    params.forEach((param) => {
        result[param.name] = param.value;
    });
    return result;
}
/** A React component for the schedule extension's main display */
class SchedulePanel extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        /**
         * Renders the component.
         *
         * @returns React element
         */
        this.render = () => {
            const notebookIndependent = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                this.renderConfigParams(),
                this.renderViewButtons(),
                this.renderRunsFilterParams(),
                this.renderCurrentNotebook()));
            const notebookDependent = this.currentNotebookPanel ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                this.renderRunParameters(),
                this.renderScheduleParameters(),
                this.renderExecuteButtons(),
                this.renderAlerts())) : (react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarNoNotebookClass }, "Select or create a notebook to enable execution and scheduling."));
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                notebookIndependent,
                notebookDependent));
        };
        this.onParametersChange = (editor) => {
            this.setState({ parameters: editor.value });
        };
        this.onServerUrlChange = (event) => {
            this.setState({ serverURL: event.target.value }, () => this.saveState());
        };
        this.onAccessKeyChange = (event) => {
            this.setState({ accessKey: event.target.value }, () => this.saveState());
        };
        this.onImageChange = (event) => {
            this.setState({ image: event.target.value }, () => this.saveState());
        };
        this.onRoleChange = (event) => {
            this.setState({ role: event.target.value }, () => this.saveState());
        };
        this.onInstanceTypeChange = (event) => {
            this.setState({ instanceType: event.target.value }, () => this.saveState());
        };
        this.onSecurityGroupsChange = (event) => {
            this.setState({ securityGroups: event.target.value }, () => this.saveState());
        };
        this.onSubnetsChange = (event) => {
            this.setState({ subnets: event.target.value }, () => this.saveState());
        };
        this.onMaxMinutesChange = (event) => {
            this.setState({ maxMinutes: event.target.value }, () => this.saveState());
        };
        this.onRuleNameChange = (event) => {
            this.setState({ ruleName: event.target.value }, () => this.saveState());
        };
        this.onScheduleChange = (event) => {
            this.setState({ schedule: event.target.value }, () => this.saveState());
        };
        this.onEventPatternChange = (event) => {
            this.setState({ eventPattern: event.target.value }, () => this.saveState());
        };
        this.onProjectChange = (event) => {
            this.setState({ project: event.target.value }, () => this.saveState());
        };
        this.onSubProjectChange = (event) => {
            this.setState({ subproject: event.target.value }, () => this.saveState());
        };
        this.onRunListClick = async () => {
            this.props.runsModel.setDataplateServerKey(this.state.serverURL, this.state.accessKey);
            this.props.runsModel.setProject(this.state.project, this.state.subproject);
            this.app.commands.execute('dataplate-lab:open_list_runs');
        };
        this.onScheduleListClick = async () => {
            this.props.rulesModel.setDataplateServerKey(this.state.serverURL, this.state.accessKey);
            this.app.commands.execute('dataplate-lab:open_list_schedules');
        };
        this.onDatasetListClick = async () => {
            this.props.datasetsModel.setDataplateServerKey(this.state.serverURL, this.state.accessKey);
            this.app.commands.execute('dataplate-lab:open_list_datasets');
        };
        this.onProjectListClick = async () => {
            this.props.projectsModel.setDataplateServerKey(this.state.serverURL, this.state.accessKey);
            this.app.commands.execute('dataplate-lab:open_list_projects');
        };
        this.onRunClick = async () => {
            console.log('Run Now');
            this.clearAlerts();
            try {
                this.addAlert({
                    type: 'notice',
                    message: `Starting notebook run for "${this.state.notebook}"`,
                });
                // const content = this.currentNotebookPanel.model.toJSON();
                // const s3Object = await this.uploadNotebook(content);
                // console.log(`notebook uploaded to ${s3Object}`);
                // TODO: clean up non-camel-case entries in the server requests
                /* eslint-disable @typescript-eslint/camelcase */
                const request = {
                    image: this.state.image,
                    input_path: this.currentNotebookPanel.context.contentsModel.path,
                    notebook: this.state.notebook,
                    parameters: convertParameters(this.state.parameters),
                    role: this.state.role,
                    instance_type: this.state.instanceType,
                    serverURL: this.state.serverURL,
                    accessKey: this.state.accessKey,
                    securityGroupIds: this.state.securityGroups,
                    subnets: this.state.subnets,
                    max_time_limit_minutes: parseInt(this.state.maxMinutes),
                };
                /* eslint-enable @typescript-eslint/camelcase */
                const jobName = await this.invokeNotebook(request);
                this.addAlert({ message: `Started notebook run "${jobName}"` });
                console.log(`started job ${jobName}`);
                this.props.runsModel.refresh();
            }
            catch (e) {
                this.addAlert({
                    type: 'error',
                    message: `Error starting run for "${this.state.notebook}": ${e.message}`,
                });
            }
        };
        this.onScheduleClick = async () => {
            console.log('Create schedule!!!');
            this.clearAlerts();
            try {
                this.addAlert({
                    type: 'notice',
                    message: `Creating rule "${this.state.ruleName}"`,
                });
                // const content = this.currentNotebookPanel.model.toJSON();
                // const s3Object = await this.uploadNotebook(content);
                // console.log(`notebook uploaded to ${s3Object}`);
                /* eslint-disable @typescript-eslint/camelcase */
                const request = {
                    image: this.state.image,
                    input_path: this.currentNotebookPanel.context.contentsModel.path,
                    notebook: this.state.notebook,
                    parameters: convertParameters(this.state.parameters),
                    role: this.state.role,
                    instance_type: this.state.instanceType,
                    serverURL: this.state.serverURL,
                    accessKey: this.state.accessKey,
                    securityGroupIds: this.state.securityGroups,
                    subnets: this.state.subnets,
                    max_time_limit_minutes: parseInt(this.state.maxMinutes),
                };
                const schedule = this.state.schedule;
                if (schedule !== '') {
                    request.schedule = schedule;
                }
                const eventPattern = this.state.eventPattern;
                if (eventPattern !== '') {
                    request.event_pattern = eventPattern;
                }
                /* eslint-enable @typescript-eslint/camelcase */
                const ruleName = await this.createRule(this.state.ruleName, request);
                this.addAlert({ message: `Created rule "${ruleName}"` });
                console.log(`created rule ${ruleName}`);
                this.props.rulesModel.refresh();
            }
            catch (e) {
                this.addAlert({
                    type: 'error',
                    message: `Error creating rule "${this.state.ruleName}": ${e.message}`,
                });
            }
        };
        ////////////////////////
        /* START SECURITY SCAN*/
        ////////////////////////
        this.onScanClick = async () => {
            console.log('Scan Notebook!!!');
            this.clearAlerts();
            try {
                this.addAlert({
                    type: 'notice',
                    message: `Scanning Notebook "${this.state.notebook}"`,
                });
                const request = {
                    notebook_file_path: this.currentNotebookPanel.context.contentsModel.path,
                    serverURL: this.state.serverURL,
                    accessKey: this.state.accessKey,
                };
                const report_name = await this.scanNotebook(this.state.notebook, request);
                this.addAlert({ message: `Scan finished successfully for notebook ${this.state.notebook}, open report file ${report_name} from your root folder` });
                console.log(`Scan finished successfully for notebook ${this.state.notebook}, open report file ${report_name}`);
            }
            catch (e) {
                this.addAlert({
                    type: 'error',
                    message: `Error scan notebook "${this.state.notebook}": ${e.message}`,
                });
            }
        };
        ///* END SECURITY SCAN *///
        ////////////////////////////
        /* START Statistics Report*/
        this.onStatisticsReportClick = async () => {
            console.log('Statistics Report for Notebook!!!');
            this.clearAlerts();
            try {
                this.addAlert({
                    type: 'notice',
                    message: `Generating statistics report (5 last runs) for Notebook "${this.state.notebook}"`,
                });
                const request = {
                    notebook_name: this.state.notebook,
                    serverURL: this.state.serverURL,
                    accessKey: this.state.accessKey,
                };
                const report_name = await this.statisticsReportNotebook(request);
                this.addAlert({ message: `Statistics report finished successfully for notebook ${this.state.notebook}, open report file ${report_name} from your root folder` });
                console.log(`Statistics report finished successfully for notebook ${this.state.notebook}, open report file ${report_name}`);
            }
            catch (e) {
                this.addAlert({
                    type: 'error',
                    message: `Error generating statistics report for notebook "${this.state.notebook}": ${e.message}`,
                });
            }
        };
        /* END Statistics Report*/
        //////////////////////////
        this.alertKey = 0;
        this.app = props.app;
        this.shell = props.shell;
        this.currentNotebookChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this.setCurrentWidget(this.shell.currentWidget);
        this.state = {
            notebook: this.notebook,
            notebookPanel: this.currentNotebookPanel,
            image: '',
            parameters: null,
            role: '',
            instanceType: '',
            ruleName: '',
            schedule: '',
            eventPattern: '',
            alerts: [],
            serverURL: '',
            accessKey: '',
            securityGroups: '',
            subnets: '',
            maxMinutes: '120',
            project: null,
            subproject: null,
        };
        this.loadState();
        this.shell.currentChanged.connect(this.onCurrentWidgetChanged, this);
    }
    //TODO: track notebook renames
    onCurrentWidgetChanged(sender, args) {
        const newWidget = args.newValue;
        const label = newWidget && newWidget.title.label;
        console.log(`current widget changed to ${label}`);
        this.setCurrentWidget(newWidget);
        this.setState({ notebook: this.notebook, notebookPanel: this.currentNotebookPanel });
    }
    setCurrentWidget(newWidget) {
        const context = newWidget && newWidget.context;
        const session = context && context.sessionContext && context.sessionContext.session;
        const isNotebook = session && session.type === 'notebook';
        if (isNotebook) {
            this.currentNotebookPanel = newWidget;
            this.notebook = session.name;
        }
        else {
            this.currentNotebookPanel = null;
            this.notebook = null;
        }
        this.currentNotebookChanged.emit(this.currentNotebookPanel);
    }
    renderViewButtons() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "View Notebook Operations & Datasets"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.flexButtonsClass },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "View notebook runs", value: "Runs", onClick: this.onRunListClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "View notebook scheduled workflows", value: "Workflow Jobs", onClick: this.onScheduleListClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "View datasets", value: "Datasets", onClick: this.onDatasetListClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "View projects", value: "Projects", onClick: this.onProjectListClick })))));
    }
    renderConfigParams() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "DataPlate Configuration"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.InputColumn, null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "DataPlate Server URL:", value: this.state.serverURL, title: "DataPlate Server URL to communicate with", placeholder: "", onChange: this.onServerUrlChange }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledPasswordInput, { label: "DataPlate Access Key:", value: this.state.accessKey, title: "DataPlate Access Key to use for specific user", placeholder: "", onChange: this.onAccessKeyChange })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { href: "https://api.dataplate.io/reference/api-reference", style: { 'color': 'blue' }, target: "_blank", rel: "noreferrer" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("i", { className: "fa fa-info-circle blueiconcolor" },
                        " ",
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("u", null, "Dataplate API"))))));
    }
    renderRunsFilterParams() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "Filter runs by project/sub-project"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.InputColumn, null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInputMaxWidth, { label: "", value: this.state.project, title: "Filter notebook runs by project", placeholder: "Filter by project name", onChange: this.onProjectChange }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInputMaxWidth, { label: "", value: this.state.subproject, title: "Filter notebook runs by sub-project", placeholder: "Filter by sub-project name", onChange: this.onSubProjectChange })))));
    }
    renderCurrentNotebook() {
        const notebook = this.state.notebook;
        let notebookDisplay;
        if (notebook != null) {
            notebookDisplay = react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, notebook);
        }
        else {
            notebookDisplay = react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, "No notebook selected");
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "Current Notebook"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarNotebookNameClass }, notebookDisplay)));
    }
    renderRunParameters() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "Notebook Execution"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_ParameterEditor__WEBPACK_IMPORTED_MODULE_6__.ParameterEditor, { onChange: this.onParametersChange, notebookPanel: this.currentNotebookPanel, notebookPanelChanged: this.currentNotebookChanged }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.InputColumn, null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Image:", value: this.state.image, title: "ECR image to use", placeholder: "", onChange: this.onImageChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Role:", value: this.state.role, title: "IAM role to use", placeholder: "", onChange: this.onRoleChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Instance:", value: this.state.instanceType, title: "Instance type to run on", placeholder: "", onChange: this.onInstanceTypeChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Security Group IDs:", value: this.state.securityGroups, title: "Security groups separated by comma", placeholder: "", onChange: this.onSecurityGroupsChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Subnets:", value: this.state.subnets, title: "Subnets separated by comma", placeholder: "", onChange: this.onSubnetsChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledNumberInput, { label: "Max run minutes:", value: this.state.maxMinutes, title: "Maximum minutes to run the job", placeholder: "", onChange: this.onMaxMinutesChange }))));
    }
    renderScheduleParameters() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("header", null, "Schedule Rule"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.InputColumn, null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Rule Name:", value: this.state.ruleName, title: "A name for this schedule", placeholder: "", onChange: this.onRuleNameChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Schedule:", value: this.state.schedule, title: "Schedule for the notebook run", placeholder: "", onChange: this.onScheduleChange }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_InputColumn__WEBPACK_IMPORTED_MODULE_5__.LabeledTextInput, { label: "Event Pattern:", value: this.state.eventPattern, title: "Events to trigger the notebook run", placeholder: "", onChange: this.onEventPatternChange }))));
    }
    renderExecuteButtons() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: `${_style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarSectionClass} ${_style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.runSidebarNoHeaderClass}` },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.flexButtonsClass },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "Run the notebook now", value: "Run Now", onClick: this.onRunClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "Create schedule", value: "Create Schedule", onClick: this.onScheduleClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "Statistics Report for the notebook saved statistics", value: "Statistics Report", onClick: this.onStatisticsReportClick }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.sidebarButtonClass, type: "button", title: "Scan the notebook", value: "Security Scan", onClick: this.onScanClick })))));
    }
    renderAlerts() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SchedulePanel__WEBPACK_IMPORTED_MODULE_4__.alertAreaClass }, this.state.alerts.map((alert) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_Alert__WEBPACK_IMPORTED_MODULE_7__.Alert, { key: `alert-${alert.key}`, type: alert.type, message: alert.message })))));
    }
    // private async uploadNotebook(notebook: JSONValue): Promise<string> {
    //   const settings = ServerConnection.makeSettings();
    //   const response = await ServerConnection.makeRequest(
    //     URLExt.join(settings.baseUrl, 'dataplate-lab', 'upload'),
    //     { method: 'PUT', body: JSON.stringify(notebook) },
    //     settings,
    //   );
    //
    //   if (!response.ok) {
    //     const error = (await response.json()) as ErrorResponse;
    //     let errorMessage: string;
    //     if (error.error) {
    //       errorMessage = error.error.message;
    //     } else {
    //       errorMessage = JSON.stringify(error);
    //     }
    //     throw Error('Uploading notebook to S3 failed: ' + errorMessage);
    //   }
    //
    //   const data = (await response.json()) as UploadNotebookResponse;
    //   return data.s3Object;
    // }
    // Figure out if the current notebook has a parameter cell marked
    hasParameterCell() {
        if (!this.currentNotebookPanel) {
            return false;
        }
        const cells = this.currentNotebookPanel.model.cells;
        for (let i = 0; i < cells.length; i++) {
            const tags = cells.get(i).metadata.get('tags');
            if (tags && tags.includes('parameters')) {
                return true;
            }
        }
        return false;
    }
    runReady() {
        const result = [];
        // if (!this.state.image) {
        //   result.push('missing container image');
        // }
        // if (!this.state.instanceType) {
        //   result.push('missing instance type');
        // }
        if (this.state.parameters.length > 0 && !this.hasParameterCell()) {
            result.push(`no parameter cell defined in ${this.notebook}`);
        }
        return result;
    }
    async invokeNotebook(request) {
        const errors = this.runReady();
        if (errors.length > 0) {
            throw new Error(errors.join(', '));
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'run'), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            throw Error(errorMessage);
        }
        const data = (await response.json());
        return data.job_name;
    }
    // Return an array of reasons that we can't create a schedule.
    scheduleReady() {
        const result = this.runReady();
        if (!this.state.ruleName) {
            result.push('missing schedule name');
        }
        if (!(this.state.schedule || this.state.eventPattern)) {
            result.push('must have either a schedule or an event pattern');
        }
        return result;
    }
    async createRule(ruleName, request) {
        const errors = this.scheduleReady();
        if (errors.length > 0) {
            throw new Error(errors.join(', '));
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'schedule', ruleName), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            throw Error(errorMessage);
        }
        const data = (await response.json());
        return data.rule_name;
    }
    // Return an array of reasons that we can't scan a notebook.
    scanReady() {
        const result = [];
        if (!this.state.notebook) {
            result.push('missing notebook name - did you save your notebook ?');
        }
        if (!this.currentNotebookPanel.context.contentsModel.path.endsWith('.ipynb')) {
            result.push('Youe `CURRENT NOTEBOOK` must be a proper notebook file with extension .ipynb');
        }
        return result;
    }
    async scanNotebook(notebookName, request) {
        const errors = this.scanReady();
        if (errors.length > 0) {
            throw new Error(errors.join(', '));
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'scan', notebookName), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            throw Error(errorMessage);
        }
        const data = (await response.json());
        return data.report_name;
    }
    // Return an array of reasons that we can't scan a notebook.
    statisticsReportReady() {
        const result = [];
        if (!this.state.notebook) {
            result.push('missing notebook name - did you save your notebook ?');
        }
        return result;
    }
    async statisticsReportNotebook(request) {
        const errors = this.statisticsReportReady();
        if (errors.length > 0) {
            throw new Error(errors.join(', '));
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'reportstatistics'), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            let errorMessage;
            if (error.error) {
                errorMessage = error.error.message;
            }
            else {
                errorMessage = JSON.stringify(error);
            }
            throw Error(errorMessage);
        }
        const data = (await response.json());
        return data.report_name;
    }
    addAlert(alert) {
        const key = this.alertKey++;
        const keyedAlert = Object.assign(Object.assign({}, alert), { key: `alert-${key}` });
        this.setState({ alerts: [keyedAlert] });
    }
    clearAlerts() {
        this.setState({ alerts: [] });
    }
    saveState() {
        const state = {
            image: this.state.image,
            role: this.state.role,
            instanceType: this.state.instanceType,
            ruleName: this.state.ruleName,
            schedule: this.state.schedule,
            eventPattern: this.state.eventPattern,
            serverURL: this.state.serverURL,
            accessKey: this.state.accessKey,
            securityGroups: this.state.securityGroups,
            subnets: this.state.subnets,
            maxMinutes: this.state.maxMinutes,
            project: this.state.project,
            subproject: this.state.subproject,
        };
        this.props.stateDB.save(KEY, state);
    }
    loadState() {
        this.props.stateDB.fetch(KEY).then((s) => {
            const state = s;
            if (state) {
                this.setState({
                    image: state['image'],
                    role: state['role'],
                    instanceType: state['instanceType'],
                    ruleName: state['ruleName'],
                    schedule: state['schedule'],
                    eventPattern: state['eventPattern'],
                    serverURL: state['serverURL'],
                    accessKey: state['accessKey'],
                    securityGroups: state['securityGroups'],
                    subnets: state['subnets'],
                    maxMinutes: state['maxMinutes'],
                    project: state['project'],
                    subproject: state['subproject'],
                });
            }
        });
    }
}


/***/ }),

/***/ "./lib/components/SimpleTable.js":
/*!***************************************!*\
  !*** ./lib/components/SimpleTable.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SimpleTable": () => (/* binding */ SimpleTable),
/* harmony export */   "SimpleTablePage": () => (/* binding */ SimpleTablePage),
/* harmony export */   "SimpleTableProps": () => (/* binding */ SimpleTableProps)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/SimpleTable */ "./lib/style/SimpleTable.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */


class SimpleTableProps {
}
function SimpleTablePage(data) {
    let title = null;
    if (data.title) {
        title = react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__.tablePageTitleClass }, data.title);
    }
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__.tablePageClass },
        title,
        data.children));
}
class SimpleTable extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor() {
        super(...arguments);
        this.renderHeadingRow = (_cell, cellIndex) => {
            const { headings } = this.props;
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(Cell, { key: `heading-${cellIndex}`, content: headings[cellIndex], header: true });
        };
        this.renderRow = (row, rowIndex) => {
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("tr", { key: `row-${rowIndex}` }, row.map((cell, cellIndex) => {
                return react__WEBPACK_IMPORTED_MODULE_0__.createElement(Cell, { key: `${rowIndex}-${cellIndex}`, content: cell });
            })));
        };
    }
    render() {
        const { headings, rows } = this.props;
        this.renderHeadingRow = this.renderHeadingRow.bind(this);
        this.renderRow = this.renderRow.bind(this);
        const theadMarkup = react__WEBPACK_IMPORTED_MODULE_0__.createElement("tr", { key: "heading" }, headings.map(this.renderHeadingRow));
        const tbodyMarkup = rows.map(this.renderRow);
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__.tableWrapperClass },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("table", { className: _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__.tableClass },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("thead", null, theadMarkup),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("tbody", null, tbodyMarkup))));
    }
}
function Cell(data) {
    const cellMarkup = data.header ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement("th", { className: "${cellClass} Cell-header" }, data.content)) : (react__WEBPACK_IMPORTED_MODULE_0__.createElement("td", { className: _style_SimpleTable__WEBPACK_IMPORTED_MODULE_1__.cellClass }, data.content));
    return cellMarkup;
}


/***/ }),

/***/ "./lib/components/SubProjectsDialog.js":
/*!*********************************************!*\
  !*** ./lib/components/SubProjectsDialog.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SubProjectsDialogBody": () => (/* binding */ SubProjectsDialogBody),
/* harmony export */   "showSubProjects": () => (/* binding */ showSubProjects)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_tables__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/tables */ "./lib/style/tables.js");
/* harmony import */ var _SimpleTable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./SimpleTable */ "./lib/components/SimpleTable.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




// import { sectionClass, labeledRowClass, kvContainer } from '../style/RunDetailsDialog';
 //, tableLinkClass

async function loadSubProjects(projectName, serverURL, accessKey) {
    try {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const request = {
            serverURL: serverURL,
            accessKey: accessKey,
        };
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'subprojects', projectName), { method: 'POST', body: JSON.stringify(request) }, settings);
        if (!response.ok) {
            const error = (await response.json());
            if (error.error) {
                return { projects: null, error: error.error.message };
            }
            else {
                return { projects: null, error: JSON.stringify(error) };
            }
        }
        const data = (await response.json());
        return { projects: data.projects, error: null };
    }
    catch (e) {
        return { projects: null, error: e.message };
    }
}
function showSubProjects(projectName, serverURL, accessKey) {
    return async () => {
        let subprojects;
        let error;
        try {
            subprojects = await loadSubProjects(projectName, serverURL, accessKey);
        }
        catch (e) {
            error = e.message;
        }
        let title;
        if (subprojects.projects) {
            if (projectName) {
                title = `Sub-Projects list for Project: "${projectName}"`;
            }
            else {
                title = `Sub-Projects list`;
            }
        }
        else {
            title = 'Error retrieving Sub-Projects';
        }
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
            title: title,
            body: react__WEBPACK_IMPORTED_MODULE_2___default().createElement(SubProjectsDialogBody, { projectName: projectName, subprojects: subprojects.projects, error: error }),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: 'Close' })],
        });
    };
}
const Headers = ['Name', 'Created', 'LastModified'];
class SubProjectsDialogBody extends (react__WEBPACK_IMPORTED_MODULE_2___default().Component) {
    constructor(props) {
        super(props);
        this.extractRow = (project) => {
            return [
                project.Name,
                project.Created,
                project.LastModified
            ];
        };
        this.state = { subprojects: props.subprojects, error: props.error };
    }
    render() {
        let content;
        if (this.state.subprojects) {
            // sometimes it seems that render gets called before the constructor ???
            const rows = this.state.subprojects.map(this.extractRow);
            if (rows.length === 0) {
                content = react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass }, "No Sub-Projects are available");
            }
            else {
                content = react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_5__.SimpleTable, { headings: Headers, rows: rows });
            }
        }
        else if (this.state.error) {
            content = react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass },
                "Error retrieving sub-projects: ",
                this.state.error);
        }
        else {
            content = react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: _style_tables__WEBPACK_IMPORTED_MODULE_4__.tableEmptyClass }, "Loading sub-projects...");
        }
        return react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_SimpleTable__WEBPACK_IMPORTED_MODULE_5__.SimpleTablePage, { title: "Sub-Projects List" }, content);
    }
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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _widgets_RunsWidget__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./widgets/RunsWidget */ "./lib/widgets/RunsWidget.js");
/* harmony import */ var _widgets_RulesWidget__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./widgets/RulesWidget */ "./lib/widgets/RulesWidget.js");
/* harmony import */ var _widgets_ScheduleWidget__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./widgets/ScheduleWidget */ "./lib/widgets/ScheduleWidget.js");
/* harmony import */ var _widgets_DatasetsWidget__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./widgets/DatasetsWidget */ "./lib/widgets/DatasetsWidget.js");
/* harmony import */ var _widgets_ProjectsWidget__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./widgets/ProjectsWidget */ "./lib/widgets/ProjectsWidget.js");
/* harmony import */ var _models_RunsModel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./models/RunsModel */ "./lib/models/RunsModel.js");
/* harmony import */ var _style_icons__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./style/icons */ "./lib/style/icons.js");
/* harmony import */ var _models_RulesModel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./models/RulesModel */ "./lib/models/RulesModel.js");
/* harmony import */ var _models_DatasetsModel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./models/DatasetsModel */ "./lib/models/DatasetsModel.js");
/* harmony import */ var _models_ProjectsModel__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./models/ProjectsModel */ "./lib/models/ProjectsModel.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */














function activate(app, shell, palette, restorer, rendermime, stateDB) {
    console.log('JupyterLab extension dataplate-lab is activated!');
    let runsWidget;
    let rulesWidget;
    let datasetsWidget;
    let projectsWidget;
    const runsModel = new _models_RunsModel__WEBPACK_IMPORTED_MODULE_4__.RunsModel();
    const rulesModel = new _models_RulesModel__WEBPACK_IMPORTED_MODULE_5__.RulesModel();
    const datasetsModel = new _models_DatasetsModel__WEBPACK_IMPORTED_MODULE_6__.DatasetsModel();
    const projectsModel = new _models_ProjectsModel__WEBPACK_IMPORTED_MODULE_7__.ProjectsModel();
    (0,_style_icons__WEBPACK_IMPORTED_MODULE_8__["default"])();
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'dataplate-labs',
    });
    // Track and restore the widget state
    const tracker1 = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'dataplate-lab_schedules',
    });
    const tracker2 = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'dataplate-lab_datasets',
    });
    const tracker3 = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'dataplate-lab_projects',
    });
    // Add the list runs command
    const command = 'dataplate-lab:open_list_runs';
    app.commands.addCommand(command, {
        label: 'List Notebook Runs',
        execute: () => {
            if (!runsWidget) {
                const content = new _widgets_RunsWidget__WEBPACK_IMPORTED_MODULE_9__.RunsWidget(app, rendermime, runsModel);
                runsWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                runsWidget.id = 'dataplate-lab_list_runs';
                runsWidget.title.iconClass = 'scheduler-tab-icon fa fa-clock-o';
                runsWidget.title.label = 'Notebook Runs';
                runsWidget.title.closable = true;
                runsWidget.disposed.connect(() => {
                    runsWidget = undefined;
                });
            }
            if (!tracker.has(runsWidget)) {
                // Track the state of the widget for later restoration
                tracker.add(runsWidget);
            }
            if (!runsWidget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(runsWidget, 'main');
            }
            // refresh the list on the widget
            runsWidget.content.update();
            // Activate the widget
            app.shell.activateById(runsWidget.id);
        },
    });
    // Add the command to the palette.
    palette.addItem({ command, category: 'DataPlate Notebook Commands' });
    const command1 = 'dataplate-lab:open_list_schedules';
    app.commands.addCommand(command1, {
        label: 'List Notebook Schedules',
        execute: () => {
            if (!rulesWidget) {
                const content = new _widgets_RulesWidget__WEBPACK_IMPORTED_MODULE_10__.RulesWidget(rulesModel);
                rulesWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                rulesWidget.id = 'dataplate-lab_list_schedules';
                rulesWidget.title.iconClass = 'scheduler-tab-icon fa fa-clock-o';
                rulesWidget.title.label = 'Notebook Schedules';
                rulesWidget.title.closable = true;
                rulesWidget.disposed.connect(() => {
                    rulesWidget = undefined;
                });
            }
            if (!tracker1.has(rulesWidget)) {
                // Track the state of the widget for later restoration
                tracker1.add(rulesWidget);
            }
            if (!rulesWidget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(rulesWidget, 'main');
            }
            // refresh the list on the widget
            rulesWidget.content.update();
            // Activate the widget
            app.shell.activateById(rulesWidget.id);
        },
    });
    // Add the command to the palette.
    palette.addItem({ command: command1, category: 'DataPlate Notebook Commands' });
    const command2 = 'dataplate-lab:open_list_datasets';
    app.commands.addCommand(command2, {
        label: 'List My Allowed Datasets',
        execute: () => {
            if (!datasetsWidget) {
                const content = new _widgets_DatasetsWidget__WEBPACK_IMPORTED_MODULE_11__.DatasetsWidget(datasetsModel);
                datasetsWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                datasetsWidget.id = 'dataplate-lab_list_datasets';
                datasetsWidget.title.iconClass = 'scheduler-tab-icon fa fa-database';
                datasetsWidget.title.label = 'Allowed Datasets';
                datasetsWidget.title.closable = true;
                datasetsWidget.disposed.connect(() => {
                    datasetsWidget = undefined;
                });
            }
            if (!tracker2.has(datasetsWidget)) {
                // Track the state of the widget for later restoration
                tracker2.add(datasetsWidget);
            }
            if (!datasetsWidget.isAttached) {
                // Attach the datasetsWidget to the main work area if it's not there
                app.shell.add(datasetsWidget, 'main');
            }
            // refresh the list on the widget
            datasetsWidget.content.update();
            // Activate the widget
            app.shell.activateById(datasetsWidget.id);
        },
    });
    // Add the command to the palette.
    palette.addItem({ command: command2, category: 'DataPlate Datasets Commands' });
    const command3 = 'dataplate-lab:open_list_projects';
    app.commands.addCommand(command3, {
        label: 'List Projects',
        execute: () => {
            if (!projectsWidget) {
                const content = new _widgets_ProjectsWidget__WEBPACK_IMPORTED_MODULE_12__.ProjectsWidget(projectsModel);
                projectsWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                projectsWidget.id = 'dataplate-lab_list_projects';
                projectsWidget.title.iconClass = 'scheduler-tab-icon fa fa-list';
                projectsWidget.title.label = 'Projects';
                projectsWidget.title.closable = true;
                projectsWidget.disposed.connect(() => {
                    projectsWidget = undefined;
                });
            }
            if (!tracker3.has(projectsWidget)) {
                // Track the state of the widget for later restoration
                tracker3.add(projectsWidget);
            }
            if (!projectsWidget.isAttached) {
                // Attach the datasetsWidget to the main work area if it's not there
                app.shell.add(projectsWidget, 'main');
            }
            // refresh the list on the widget
            projectsWidget.content.update();
            // Activate the widget
            app.shell.activateById(projectsWidget.id);
        },
    });
    // Add the command to the palette.
    palette.addItem({ command: command3, category: 'DataPlate Projects Commands' });
    // Create the schedule widget sidebar
    const scheduleWidget = new _widgets_ScheduleWidget__WEBPACK_IMPORTED_MODULE_13__.ScheduleWidget(app, shell, runsModel, rulesModel, datasetsModel, projectsModel, stateDB);
    scheduleWidget.id = 'jp-schedule';
    scheduleWidget.title.iconClass = 'jp-SideBar-tabIcon fa fa-dot-circle-o fa-2x scheduler-sidebar-icon';
    scheduleWidget.title.caption = 'Schedule';
    // Let the application restorer track the running panel for restoration of
    // application state (e.g. setting the running panel as the current side bar
    // widget).
    restorer.add(scheduleWidget, 'schedule-sidebar');
    // Rank has been chosen somewhat arbitrarily to give priority to the running
    // sessions widget in the sidebar.
    app.shell.add(scheduleWidget, 'left', { rank: 200 });
    // Track and restore the widget states
    restorer.restore(tracker, {
        command,
        name: () => 'dataplate-lab',
    });
    restorer.restore(tracker1, {
        command: command1,
        name: () => 'dataplate-lab_schedules',
    });
    restorer.restore(tracker2, {
        command: command2,
        name: () => 'dataplate-lab_datasets',
    });
    restorer.restore(tracker3, {
        command: command3,
        name: () => 'dataplate-lab_projects',
    });
}
/**
 * Initialization data for the dataplate-lab extension.
 */
const extension = {
    id: 'dataplate-lab:plugin',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.IStateDB],
    activate: activate,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/models/DatasetsModel.js":
/*!*************************************!*\
  !*** ./lib/models/DatasetsModel.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatasetsModel": () => (/* binding */ DatasetsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */



class DatasetsModel {
    constructor() {
        this._isDisposed = false;
        this._datasetsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._active = false;
        this._refreshing = false;
        this._serverURL = "";
        this._accessKey = "";
        // const interval = 30 * 1000; // TODO: make this a setting
        // const poll = new Poll({
        //   factory: () => this.refresh(),
        //   frequency: {
        //     interval: interval,
        //     backoff: true,
        //     max: 300 * 1000,
        //   },
        //   standby: 'when-hidden',
        // });
        // this._poll = poll;
    }
    get serverURL() {
        return this._serverURL;
    }
    get accessKey() {
        return this._accessKey;
    }
    setDataplateServerKey(serverUrl, accessKey) {
        this._serverURL = serverUrl;
        this._accessKey = accessKey;
    }
    setActive(active) {
        this._active = active;
        if (active) {
            this.refresh();
        }
    }
    async refresh() {
        this.getDatasets().then((result) => {
            if (result) {
                this._datasets = result.datasets;
                this._datasetsChanged.emit(result);
            }
        });
    }
    async getDatasets() {
        if (this._active && !this._refreshing) {
            this._refreshing = true;
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
                const request = {
                    serverURL: this.serverURL,
                    accessKey: this.accessKey,
                };
                // const response = await ServerConnection.makeRequest(
                //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'runs'),
                //   { method: 'GET' },
                //   settings,
                // );
                // console.log(`sending request with ${JSON.stringify(request)}`);
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'datasets'), { method: 'POST', body: JSON.stringify(request) }, settings);
                if (!response.ok) {
                    const error = (await response.json());
                    if (error.error) {
                        return { datasets: null, error: error.error.message };
                    }
                    else {
                        return { datasets: null, error: JSON.stringify(error) };
                    }
                }
                const data = (await response.json());
                return { datasets: data.datasets, error: null };
            }
            finally {
                this._refreshing = false;
            }
        }
    }
    get datasets() {
        return this._datasets;
    }
    /**
     * A signal emitted when the current list of runs changes.
     */
    get datasetsChanged() {
        return this._datasetsChanged;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._poll) {
            this._poll.dispose();
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/models/ProjectsModel.js":
/*!*************************************!*\
  !*** ./lib/models/ProjectsModel.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProjectsModel": () => (/* binding */ ProjectsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */



class ProjectsModel {
    constructor() {
        this._isDisposed = false;
        this._projectsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._active = false;
        this._refreshing = false;
        this._serverURL = "";
        this._accessKey = "";
        // const interval = 30 * 1000; // TODO: make this a setting
        // const poll = new Poll({
        //   factory: () => this.refresh(),
        //   frequency: {
        //     interval: interval,
        //     backoff: true,
        //     max: 300 * 1000,
        //   },
        //   standby: 'when-hidden',
        // });
        // this._poll = poll;
    }
    get serverURL() {
        return this._serverURL;
    }
    get accessKey() {
        return this._accessKey;
    }
    setDataplateServerKey(serverUrl, accessKey) {
        this._serverURL = serverUrl;
        this._accessKey = accessKey;
    }
    setActive(active) {
        this._active = active;
        if (active) {
            this.refresh();
        }
    }
    async refresh() {
        this.getProjects().then((result) => {
            if (result) {
                this._projects = result.projects;
                this._projectsChanged.emit(result);
            }
        });
    }
    async getProjects() {
        if (this._active && !this._refreshing) {
            this._refreshing = true;
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
                const request = {
                    serverURL: this.serverURL,
                    accessKey: this.accessKey,
                };
                // const response = await ServerConnection.makeRequest(
                //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'runs'),
                //   { method: 'GET' },
                //   settings,
                // );
                // console.log(`sending request with ${JSON.stringify(request)}`);
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'projects'), { method: 'POST', body: JSON.stringify(request) }, settings);
                if (!response.ok) {
                    const error = (await response.json());
                    if (error.error) {
                        return { projects: null, error: error.error.message };
                    }
                    else {
                        return { projects: null, error: JSON.stringify(error) };
                    }
                }
                const data = (await response.json());
                return { projects: data.projects, error: null };
            }
            finally {
                this._refreshing = false;
            }
        }
    }
    get projects() {
        return this._projects;
    }
    /**
     * A signal emitted when the current list of runs changes.
     */
    get projectsChanged() {
        return this._projectsChanged;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._poll) {
            this._poll.dispose();
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/models/RulesModel.js":
/*!**********************************!*\
  !*** ./lib/models/RulesModel.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RulesModel": () => (/* binding */ RulesModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/polling */ "./node_modules/@lumino/polling/dist/index.es6.js");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class RulesModel {
    constructor() {
        this._isDisposed = false;
        this._rulesChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._refreshing = false;
        this._active = false;
        this._serverURL = "";
        this._accessKey = "";
        const interval = 30 * 1000; // TODO: make this a setting
        const poll = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Poll({
            factory: () => this.refresh(),
            frequency: {
                interval: interval,
                backoff: true,
                max: 300 * 1000,
            },
            standby: 'when-hidden',
        });
        this._poll = poll;
    }
    get serverURL() {
        return this._serverURL;
    }
    get accessKey() {
        return this._accessKey;
    }
    setDataplateServerKey(serverUrl, accessKey) {
        this._serverURL = serverUrl;
        this._accessKey = accessKey;
    }
    setActive(active) {
        this._active = active;
        if (active) {
            this.refresh();
        }
    }
    async refresh() {
        this.getRules().then((result) => {
            if (result) {
                this._rules = result.rules;
                this._rulesChanged.emit(result);
            }
        });
    }
    async getRules() {
        if (this._active && !this._refreshing) {
            this._refreshing = true;
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
                // const response = await ServerConnection.makeRequest(
                //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'schedules'),
                //   { method: 'GET' },
                //   settings,
                // );
                const request = {
                    serverURL: this.serverURL,
                    accessKey: this.accessKey,
                };
                // console.log(`sending request with ${JSON.stringify(request)}`);
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'schedules'), { method: 'POST', body: JSON.stringify(request) }, settings);
                if (!response.ok) {
                    const error = (await response.json());
                    return { rules: null, error: error.error.message };
                }
                const data = (await response.json());
                return { rules: data.schedules, error: null };
            }
            finally {
                this._refreshing = false;
            }
        }
    }
    get rules() {
        return this._rules;
    }
    /**
     * A signal emitted when the current list of runs changes.
     */
    get rulesChanged() {
        return this._rulesChanged;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._poll) {
            this._poll.dispose();
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/models/RunsModel.js":
/*!*********************************!*\
  !*** ./lib/models/RunsModel.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunsModel": () => (/* binding */ RunsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/polling */ "./node_modules/@lumino/polling/dist/index.es6.js");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class RunsModel {
    constructor() {
        this._isDisposed = false;
        this._runsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._active = false;
        this._refreshing = false;
        this._serverURL = "";
        this._accessKey = "";
        this._project = "";
        this._subproject = "";
        const interval = 30 * 1000; // TODO: make this a setting
        const poll = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Poll({
            factory: () => this.refresh(),
            frequency: {
                interval: interval,
                backoff: true,
                max: 300 * 1000,
            },
            standby: 'when-hidden',
        });
        this._poll = poll;
    }
    get serverURL() {
        return this._serverURL;
    }
    get accessKey() {
        return this._accessKey;
    }
    get project() {
        return this._project;
    }
    get subproject() {
        return this._subproject;
    }
    setDataplateServerKey(serverUrl, accessKey) {
        this._serverURL = serverUrl;
        this._accessKey = accessKey;
    }
    setProject(project, subproject) {
        this._project = project;
        this._subproject = subproject;
    }
    setActive(active) {
        this._active = active;
        if (active) {
            this.refresh();
        }
    }
    async refresh() {
        this.getRuns().then((result) => {
            if (result) {
                this._runs = result.runs;
                this._runsChanged.emit(result);
            }
        });
    }
    async getRuns() {
        if (this._active && !this._refreshing) {
            this._refreshing = true;
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
                const request = {
                    serverURL: this.serverURL,
                    accessKey: this.accessKey,
                    project: this.project,
                    subproject: this.subproject
                };
                // const response = await ServerConnection.makeRequest(
                //   URLExt.join(settings.baseUrl, 'dataplate-lab', 'runs'),
                //   { method: 'GET' },
                //   settings,
                // );
                // console.log(`sending request with ${JSON.stringify(request)}`);
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'dataplate-lab', 'runs'), { method: 'POST', body: JSON.stringify(request) }, settings);
                if (!response.ok) {
                    const error = (await response.json());
                    if (error.error) {
                        return { runs: null, error: error.error.message };
                    }
                    else {
                        return { runs: null, error: JSON.stringify(error) };
                    }
                }
                const data = (await response.json());
                return { runs: data.runs, error: null };
            }
            finally {
                this._refreshing = false;
            }
        }
    }
    get runs() {
        return this._runs;
    }
    /**
     * A signal emitted when the current list of runs changes.
     */
    get runsChanged() {
        return this._runsChanged;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._poll) {
            this._poll.dispose();
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/style/Alert.js":
/*!****************************!*\
  !*** ./lib/style/Alert.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "alert": () => (/* binding */ alert),
/* harmony export */   "alertDanger": () => (/* binding */ alertDanger),
/* harmony export */   "alertInfo": () => (/* binding */ alertInfo),
/* harmony export */   "alertSuccess": () => (/* binding */ alertSuccess),
/* harmony export */   "alertWarning": () => (/* binding */ alertWarning)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

// Alert styles are cloned from Bootstrap 3
const alert = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    padding: '15px',
    marginBottom: '20px',
    border: '1px solid transparent',
    borderRadius: '4px',
});
const alertDanger = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    color: '#a94442',
    backgroundColor: '#f2dede',
    borderColor: '#ebccd1',
});
const alertWarning = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    color: '#8a6d3b',
    backgroundColor: '#fcf8e3',
    borderColor: '#faebcc',
});
const alertInfo = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    color: '#31708f',
    backgroundColor: '#d9edf7',
    borderColor: '#bce8f1',
});
const alertSuccess = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    color: '#3c763d',
    backgroundColor: '#dff0d8',
    borderColor: '#d6e9c6',
});


/***/ }),

/***/ "./lib/style/InputColumn.js":
/*!**********************************!*\
  !*** ./lib/style/InputColumn.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "inputColumnClass": () => (/* binding */ inputColumnClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const inputColumnClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    $nest: {
        '& td:first-child': {
            paddingLeft: '0px',
        },
    },
});


/***/ }),

/***/ "./lib/style/ParameterEditor.js":
/*!**************************************!*\
  !*** ./lib/style/ParameterEditor.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "closeIcon": () => (/* binding */ closeIcon),
/* harmony export */   "parameterEditorAddItemClass": () => (/* binding */ parameterEditorAddItemClass),
/* harmony export */   "parameterEditorNoParametersClass": () => (/* binding */ parameterEditorNoParametersClass),
/* harmony export */   "parameterEditorTableClass": () => (/* binding */ parameterEditorTableClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const parameterEditorTableClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    textAlign: 'left',
    marginLeft: '8px',
    $nest: {
        '& th': {
            fontWeight: 400,
        },
    },
});
const parameterEditorNoParametersClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    fontStyle: 'italic',
    padding: '4px 0px 6px 0px',
});
const parameterEditorAddItemClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    marginLeft: '4px',
    color: 'var(--jp-ui-font-color0)',
    backgroundColor: 'var(--jp-layout-color0)',
    $nest: {
        '&:hover': {
            backgroundColor: 'var(--jp-layout-color3)',
        },
        '&:active': {
            color: 'var(--jp-ui-inverse-font-color0)',
            backgroundColor: 'var(--jp-inverse-layout-color3)',
        },
    },
});
const closeIcon = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    backgroundSize: '16px',
    backgroundImage: 'var(--jp-icon-close)',
    height: '16px',
    width: '16px',
    padding: '4px 0px 4px 4px',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    $nest: {
        '&:hover': {
            backgroundImage: 'var(--jp-icon-close-circle)',
        },
    },
});


/***/ }),

/***/ "./lib/style/RunDetailsDialog.js":
/*!***************************************!*\
  !*** ./lib/style/RunDetailsDialog.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "kvContainer": () => (/* binding */ kvContainer),
/* harmony export */   "labeledRowClass": () => (/* binding */ labeledRowClass),
/* harmony export */   "sectionClass": () => (/* binding */ sectionClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const sectionClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    marginTop: '8px',
    $nest: {
        '& header': {
            borderBottom: 'var(--jp-border-width) solid var(--jp-border-color2)',
            flex: '0 0 auto',
            fontSize: 'var(--jp-ui-font-size1)',
            fontWeight: 600,
            letterSpacing: '1px',
            margin: '0px 0px 8px 0px',
            padding: '8px 0px',
        },
    },
});
const labeledRowClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    verticalAlign: 'top',
    $nest: {
        '&>*:last-child': {
            paddingLeft: '.6em',
        },
    },
});
const kvContainer = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    display: 'grid',
    gridTemplateColumns: 'auto auto',
    gridGap: '.2em .6em',
});


/***/ }),

/***/ "./lib/style/SchedulePanel.js":
/*!************************************!*\
  !*** ./lib/style/SchedulePanel.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "alertAreaClass": () => (/* binding */ alertAreaClass),
/* harmony export */   "flexButtonsClass": () => (/* binding */ flexButtonsClass),
/* harmony export */   "runSidebarNoHeaderClass": () => (/* binding */ runSidebarNoHeaderClass),
/* harmony export */   "runSidebarNoNotebookClass": () => (/* binding */ runSidebarNoNotebookClass),
/* harmony export */   "runSidebarNotebookNameClass": () => (/* binding */ runSidebarNotebookNameClass),
/* harmony export */   "runSidebarSectionClass": () => (/* binding */ runSidebarSectionClass),
/* harmony export */   "sidebarButtonClass": () => (/* binding */ sidebarButtonClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const runSidebarSectionClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: 'var(--jp-layout-color1)',
    overflow: 'visible',
    color: 'var(--jp-ui-font-color1)',
    /* This is needed so that all font sizing of children done in ems is
     * relative to this base size */
    fontSize: 'var(--jp-ui-font-size1)',
    marginBottom: '12px',
    $nest: {
        '& header': {
            borderBottom: 'var(--jp-border-width) solid var(--jp-border-color2)',
            flex: '0 0 auto',
            fontSize: 'var(--jp-ui-font-size0)',
            fontWeight: 600,
            letterSpacing: '1px',
            margin: '0px 0px 8px 0px',
            padding: '8px 12px',
            textTransform: 'uppercase',
        },
        '&>*': {
            marginLeft: '12px',
        },
        '&>.inputColumnMarker': {
            marginLeft: '10px',
        },
    },
});
const runSidebarNoHeaderClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    borderTop: 'var(--jp-border-width) solid var(--jp-border-color2)',
    paddingTop: '8px',
});
const runSidebarNotebookNameClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    marginBottom: 'auto',
    fontWeight: 700,
});
const runSidebarNoNotebookClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    fontStyle: 'italic',
    padding: '0px 12px',
});
const sidebarButtonClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    boxSizing: 'border-box',
    width: '9.7em',
    height: '2em',
    color: 'white',
    fontSize: 'var(--jp-ui-font-size1)',
    backgroundColor: 'var(--jp-accent-color0)',
    border: '0',
    borderRadius: '3px',
    $nest: {
        '&:hover': {
            backgroundColor: 'var(--jp-accent-color1)',
        },
        '&:active': {
            color: 'var(--md-grey-200)',
            fontWeight: 600,
        },
    },
});
// Emulate flexbox gaps even in browsers that don't support it yet, per https://coryrylan.com/blog/css-gap-space-with-flexbox
const buttonGapX = '20px';
const buttonGapY = '8px';
const flexButtonsClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    display: 'inline-flex',
    flexWrap: 'wrap',
    margin: `-${buttonGapY} 0 0 -${buttonGapX}`,
    width: `calc(100% + ${buttonGapX})`,
    $nest: {
        '> *': {
            margin: `${buttonGapY} 0 0 ${buttonGapX}`,
        },
    },
});
const alertAreaClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    marginLeft: '12px',
    marginRight: '12px',
});


/***/ }),

/***/ "./lib/style/ScheduleWidgetStyle.js":
/*!******************************************!*\
  !*** ./lib/style/ScheduleWidgetStyle.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "scheduleWidgetStyle": () => (/* binding */ scheduleWidgetStyle)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const scheduleWidgetStyle = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    display: 'flex',
    flexDirection: 'column',
    minWidth: '300px',
    color: 'var(--jp-ui-font-color1)',
    background: 'var(--jp-layout-color1)',
    fontSize: 'var(--jp-ui-font-size1)',
    overflow: 'auto',
});


/***/ }),

/***/ "./lib/style/SimpleTable.js":
/*!**********************************!*\
  !*** ./lib/style/SimpleTable.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cellClass": () => (/* binding */ cellClass),
/* harmony export */   "tableClass": () => (/* binding */ tableClass),
/* harmony export */   "tablePageClass": () => (/* binding */ tablePageClass),
/* harmony export */   "tablePageTitleClass": () => (/* binding */ tablePageTitleClass),
/* harmony export */   "tableWrapperClass": () => (/* binding */ tableWrapperClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const tablePageClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    background: 'var(--jp-layout-color1)',
    padding: '1rem 3.2rem',
    color: 'var(--jp-content-font-color1)',
});
const tablePageTitleClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    fontSize: '1.5em',
    fontWeight: 'bold',
    marginBottom: '0.5em',
});
const tableWrapperClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    maxWidth: '100vw',
});
const tableClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    borderSpacing: '0px',
    background: 'var(--jp-layout-color1)',
    color: 'var(--jp-content-font-color1)',
    boxShadow: '0 1px 0 0 rgba(22, 29, 37, 0.05)',
    width: '100%',
    $nest: {
        '& th': {
            textAlign: 'left',
        },
    },
});
const cellClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    border: '1px solid var(--jp-border-color1)',
    padding: '4px',
    textAlign: 'left',
});


/***/ }),

/***/ "./lib/style/Widget.js":
/*!*****************************!*\
  !*** ./lib/style/Widget.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "scrollableWidgetClass": () => (/* binding */ scrollableWidgetClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const scrollableWidgetClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    overflow: 'auto',
});


/***/ }),

/***/ "./lib/style/icons.js":
/*!****************************!*\
  !*** ./lib/style/icons.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ICON_INFO_CIRCLE": () => (/* binding */ ICON_INFO_CIRCLE),
/* harmony export */   "default": () => (/* binding */ registerSharingIcons)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_info_circle_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/icons/info_circle.svg */ "./style/icons/info_circle.svg");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */


const ICON_INFO_CIRCLE = 'sm-sharing-info-circle';
function registerSharingIcons() {
    new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: ICON_INFO_CIRCLE, svgstr: _style_icons_info_circle_svg__WEBPACK_IMPORTED_MODULE_1__["default"] });
}


/***/ }),

/***/ "./lib/style/tables.js":
/*!*****************************!*\
  !*** ./lib/style/tables.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tableEmptyClass": () => (/* binding */ tableEmptyClass),
/* harmony export */   "tableLinkClass": () => (/* binding */ tableLinkClass)
/* harmony export */ });
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

const tableLinkClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    color: 'var(--jp-content-link-color)',
    $nest: {
        '&:hover': {
            color: '#0366d6',
            textDecoration: 'underline',
        },
    },
});
const tableEmptyClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_0__.style)({
    fontStyle: 'italic',
});


/***/ }),

/***/ "./lib/util/files.js":
/*!***************************!*\
  !*** ./lib/util/files.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getUniqueFilename": () => (/* binding */ getUniqueFilename)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

/**
 * Given a desired filename, this returns it if it does not conflict with any existing files. If
 * there is a conflict, this returns an incremented filename like Test_1.ipynb or Test_2.ipynb.
 */
async function getUniqueFilename(app, filename) {
    const basename = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(filename);
    const components = basename.split('.');
    const extension = components.pop();
    const stem = components.join('.');
    const fileExists = async (name) => {
        try {
            await app.serviceManager.contents.get(name);
            return true;
        }
        catch (e) {
            if (e.response && e.response.status === 404) {
                return false;
            }
            throw e;
        }
    };
    let count = 1;
    let newName = filename;
    while (await fileExists(newName)) {
        newName = `${stem}_${count++}${extension}`;
    }
    return newName;
}


/***/ }),

/***/ "./lib/util/testId.js":
/*!****************************!*\
  !*** ./lib/util/testId.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "testId": () => (/* binding */ testId)
/* harmony export */ });
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */
/**
 * Returns an object with a data-testid attribute equal to the provided value, for spreading over a
 * React element.
 *
 * @example
 * const MyComponent = () => <div {...testId("foo")}></div> // becomes <div data-testid="foo"></div>
 */
const testId = (id) => ({ 'data-testid': `${id}` });


/***/ }),

/***/ "./lib/widgets/DatasetsWidget.js":
/*!***************************************!*\
  !*** ./lib/widgets/DatasetsWidget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatasetsWidget": () => (/* binding */ DatasetsWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_DatasetList__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/DatasetList */ "./lib/components/DatasetList.js");
/* harmony import */ var _style_Widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/Widget */ "./lib/style/Widget.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class DatasetsWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new widget for listing notebook runs
     */
    constructor(model) {
        super();
        this._model = model;
        this.addClass(_style_Widget__WEBPACK_IMPORTED_MODULE_2__.scrollableWidgetClass);
    }
    processMessage(msg) {
        switch (msg.type) {
            case 'before-show':
                this._model.setActive(true);
                break;
            case 'before-hide':
                this._model.setActive(false);
                break;
        }
        super.processMessage(msg);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_DatasetList__WEBPACK_IMPORTED_MODULE_3__.DatasetList, { model: this._model });
    }
}


/***/ }),

/***/ "./lib/widgets/ProjectsWidget.js":
/*!***************************************!*\
  !*** ./lib/widgets/ProjectsWidget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProjectsWidget": () => (/* binding */ ProjectsWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_ProjectList__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/ProjectList */ "./lib/components/ProjectList.js");
/* harmony import */ var _style_Widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/Widget */ "./lib/style/Widget.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class ProjectsWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new widget for listing notebook runs
     */
    constructor(model) {
        super();
        this._model = model;
        this.addClass(_style_Widget__WEBPACK_IMPORTED_MODULE_2__.scrollableWidgetClass);
    }
    processMessage(msg) {
        switch (msg.type) {
            case 'before-show':
                this._model.setActive(true);
                break;
            case 'before-hide':
                this._model.setActive(false);
                break;
        }
        super.processMessage(msg);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_ProjectList__WEBPACK_IMPORTED_MODULE_3__.ProjectList, { model: this._model });
    }
}


/***/ }),

/***/ "./lib/widgets/ReadOnlyNotebook.js":
/*!*****************************************!*\
  !*** ./lib/widgets/ReadOnlyNotebook.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "openReadonlyNotebook": () => (/* binding */ openReadonlyNotebook)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _components_ReadonlyNotebookHeader__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/ReadonlyNotebookHeader */ "./lib/components/ReadonlyNotebookHeader.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */






const toolbarClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    minHeight: '88px !important',
    display: 'flex',
    padding: '20px',
    paddingRight: '28px',
    background: 'var(--jp-info-color3)',
    borderBottomColor: 'var(--jp-info-color2)',
    color: 'var(--ui-font-color1)',
    fontSize: 'var(--jp-ui-font-size1)',
    fontFamily: 'var(--jp-ui-font-family)',
});
// Override toolbar item style
const headerClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_1__.style)({
    flex: '1 !important',
    alignItems: 'center',
    padding: 0,
    lineHeight: 'unset !important',
    fontSize: 'var(--jp-ui-font-size2) !important',
});
function openReadonlyNotebook(app, rendermime, document, notebookName, jobName) {
    const { name, content: nbContent } = document;
    const contentWidget = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.StaticNotebook({
        rendermime,
        mimeTypeService: _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__.editorServices.mimeTypeService,
    });
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.MainAreaWidget({ content: contentWidget });
    widget.id = 'shared_notebook';
    widget.title.label = `[Read-only] ${name}`;
    widget.title.iconClass = 'notebook';
    widget.toolbar.addClass(toolbarClass);
    app.shell.add(widget, 'main');
    // Model must be populated after the widget is added.
    const nbModel = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookModel();
    // nbModel.mimeType = 'text/x-python';
    nbModel.metadata.set('language_info', { name: 'python' });
    // nbModel.metadata.set('kernelspec', { name: 'python3' });
    contentWidget.model = nbModel;
    nbModel.fromJSON(nbContent);
    contentWidget.widgets.forEach((cell) => {
        cell.readOnly = true;
    });
    const headerWidget = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_ReadonlyNotebookHeader__WEBPACK_IMPORTED_MODULE_5__.ReadonlyNotebookHeader, { app: app, document: document, notebookName: notebookName, jobName: jobName }));
    headerWidget.addClass(headerClass);
    widget.toolbar.addItem('header', headerWidget);
    return widget;
}


/***/ }),

/***/ "./lib/widgets/RulesWidget.js":
/*!************************************!*\
  !*** ./lib/widgets/RulesWidget.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RulesWidget": () => (/* binding */ RulesWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_RuleList__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/RuleList */ "./lib/components/RuleList.js");
/* harmony import */ var _style_Widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/Widget */ "./lib/style/Widget.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class RulesWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new widget for listing notebook schedules
     */
    constructor(model) {
        super();
        this._model = model;
        this.addClass(_style_Widget__WEBPACK_IMPORTED_MODULE_2__.scrollableWidgetClass);
    }
    processMessage(msg) {
        switch (msg.type) {
            case 'before-show':
                this._model.setActive(true);
                break;
            case 'before-hide':
                this._model.setActive(false);
                break;
        }
        super.processMessage(msg);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_RuleList__WEBPACK_IMPORTED_MODULE_3__.RulesList, { model: this._model });
    }
}


/***/ }),

/***/ "./lib/widgets/RunsWidget.js":
/*!***********************************!*\
  !*** ./lib/widgets/RunsWidget.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunsWidget": () => (/* binding */ RunsWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_RunList__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/RunList */ "./lib/components/RunList.js");
/* harmony import */ var _style_Widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/Widget */ "./lib/style/Widget.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




class RunsWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Construct a new widget for listing notebook runs
     */
    constructor(app, rendermime, model) {
        super();
        this._app = app;
        this._rendermime = rendermime;
        this._model = model;
        this.addClass(_style_Widget__WEBPACK_IMPORTED_MODULE_2__.scrollableWidgetClass);
    }
    processMessage(msg) {
        switch (msg.type) {
            case 'before-show':
                this._model.setActive(true);
                break;
            case 'before-hide':
                this._model.setActive(false);
                break;
        }
        super.processMessage(msg);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_RunList__WEBPACK_IMPORTED_MODULE_3__.RunList, { app: this._app, rendermime: this._rendermime, model: this._model });
    }
}


/***/ }),

/***/ "./lib/widgets/ScheduleWidget.js":
/*!***************************************!*\
  !*** ./lib/widgets/ScheduleWidget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScheduleWidget": () => (/* binding */ ScheduleWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_SchedulePanel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/SchedulePanel */ "./lib/components/SchedulePanel.js");
/* harmony import */ var _style_ScheduleWidgetStyle__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/ScheduleWidgetStyle */ "./lib/style/ScheduleWidgetStyle.js");
/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You
 * may not use this file except in compliance with the License. A copy of
 * the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
 * ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */




/**
 * A class that exposes the Schedule plugin Widget.
 */
class ScheduleWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(app, shell, runsModel, rulesModel, datasetsModel, projectsModel, stateDB, options) {
        super(options);
        this.node.id = 'ScheduleSession-root';
        this.addClass(_style_ScheduleWidgetStyle__WEBPACK_IMPORTED_MODULE_2__.scheduleWidgetStyle);
        this.app = app;
        this.shell = shell;
        this.runsModel = runsModel;
        this.rulesModel = rulesModel;
        this.datasetsModel = datasetsModel;
        this.projectsModel = projectsModel;
        this.stateDB = stateDB;
        console.log('Schedule widget created');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_components_SchedulePanel__WEBPACK_IMPORTED_MODULE_3__.SchedulePanel, { app: this.app, shell: this.shell, runsModel: this.runsModel, rulesModel: this.rulesModel, datasetsModel: this.datasetsModel, projectsModel: this.projectsModel, stateDB: this.stateDB }));
    }
}


/***/ }),

/***/ "./style/icons/info_circle.svg":
/*!*************************************!*\
  !*** ./style/icons/info_circle.svg ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" aria-hidden=\"true\" focusable=\"false\" width=\"1em\" height=\"1em\" style=\"-ms-transform: rotate(360deg); -webkit-transform: rotate(360deg); transform: rotate(360deg);\" preserveAspectRatio=\"xMidYMid meet\" viewBox=\"0 0 24 24\"><path d=\"M12 11a1 1 0 0 0-1 1v4a1 1 0 0 0 2 0v-4a1 1 0 0 0-1-1zm.38-3.92a1 1 0 0 0-.76 0a1 1 0 0 0-.33.21a1.15 1.15 0 0 0-.21.33A.84.84 0 0 0 11 8a1 1 0 0 0 .29.71a1.15 1.15 0 0 0 .33.21A1 1 0 0 0 13 8a1.05 1.05 0 0 0-.29-.71a1 1 0 0 0-.33-.21zM12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8a8 8 0 0 1-8 8z\" fill=\"#626262\"/></svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils.c70a3f0ecb9d83d34dad.js.map