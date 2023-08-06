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

import * as React from 'react';

import { RunsModel } from '../models/RunsModel';
import { NotebookPanel } from '@jupyterlab/notebook';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { IStateDB } from '@jupyterlab/statedb';
import { ReadonlyJSONObject, JSONArray } from '@lumino/coreutils';//JSONValue
import { Signal } from '@lumino/signaling';
import { Widget } from '@lumino/widgets';

import {
  // UploadNotebookResponse,
  InvokeRequest,
  InvokeResponse,
  CreateRuleRequest,
  CreateRuleResponse,
  ErrorResponse,
  ScanRequest,
  ScanResponse,
  StatisticsReportRequest,
  StatisticsReportResponse,
} from '../server';
import { InputColumn, LabeledTextInput, LabeledPasswordInput, LabeledNumberInput, LabeledTextInputMaxWidth } from './InputColumn';
import { ParameterEditor, ParameterKV } from './ParameterEditor';
import { Alert, AlertProps } from './Alert';

import {
  runSidebarSectionClass,
  runSidebarNotebookNameClass,
  runSidebarNoHeaderClass,
  sidebarButtonClass,
  alertAreaClass,
  runSidebarNoNotebookClass,
  flexButtonsClass,
} from '../style/SchedulePanel';
import { JupyterFrontEnd, ILabShell } from '@jupyterlab/application';
import { RulesModel } from '../models/RulesModel';
import {DatasetsModel} from "../models/DatasetsModel";
import {ProjectsModel} from "../models/ProjectsModel";
import {ContainersModel} from "../models/ContainersModel";

const KEY = 'dataplate-lab:schedule-sidebar:data';

/** Interface for SchedulePanel component props */
export interface ISchedulePanelProps {
  app: JupyterFrontEnd;
  shell: ILabShell;
  runsModel: RunsModel;
  rulesModel: RulesModel;
  datasetsModel: DatasetsModel;
  projectsModel: ProjectsModel;
  containersModel: ContainersModel;
  stateDB: IStateDB;
}

interface PersistentState {
  image: string;
  role: string;
  instanceType: string;
  ruleName: string;
  schedule: string;
  eventPattern: string;
  serverURL: string;
  accessKey: string;
  securityGroups: string;
  subnets: string;
  maxMinutes: string;
  project: string;
  subproject: string;
}
interface ISchedulePanelState extends PersistentState {
  notebook: string;
  notebookPanel: NotebookPanel;
  parameters: ParameterKV[];
  alerts: (AlertProps & { key: string })[];
}

// convertParameters turns the parameters we use here into a map that the server and containter expect.
// TODO: fix the container to take lists and delete this function so that parameters are always in the order specified
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function convertParameters(params: ParameterKV[]): Record<string, any> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const result: Record<string, any> = {};
  params.forEach((param) => {
    result[param.name] = param.value;
  });
  return result;
}

/** A React component for the schedule extension's main display */
export class SchedulePanel extends React.Component<ISchedulePanelProps, ISchedulePanelState> {
  constructor(props: ISchedulePanelProps) {
    super(props);
    this.app = props.app;
    this.shell = props.shell;
    this.currentNotebookChanged = new Signal<SchedulePanel, NotebookPanel>(this);
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
  private onCurrentWidgetChanged(sender: ILabShell, args: ILabShell.IChangedArgs) {
    const newWidget = args.newValue;
    const label = newWidget && newWidget.title.label;
    console.log(`current widget changed to ${label}`);
    this.setCurrentWidget(newWidget);
    this.setState({ notebook: this.notebook, notebookPanel: this.currentNotebookPanel });
  }

  private setCurrentWidget(newWidget: Widget): void {
    const context = newWidget && (newWidget as NotebookPanel).context;
    const session = context && context.sessionContext && context.sessionContext.session;
    const isNotebook = session && session.type === 'notebook';
    if (isNotebook) {
      this.currentNotebookPanel = newWidget as NotebookPanel;
      this.notebook = session.name;
    } else {
      this.currentNotebookPanel = null;
      this.notebook = null;
    }
    this.currentNotebookChanged.emit(this.currentNotebookPanel);
  }

  /**
   * Renders the component.
   *
   * @returns React element
   */
  render = (): React.ReactElement => {
    const notebookIndependent = (
      <div>
        {this.renderConfigParams()}
        {this.renderViewButtons()}
        {this.renderRunsFilterParams()}
        {this.renderCurrentNotebook()}
      </div>
    );
    const notebookDependent = this.currentNotebookPanel ? (
      <div>
        {this.renderRunParameters()}
        {this.renderScheduleParameters()}
        {this.renderExecuteButtons()}
        {this.renderAlerts()}
      </div>
    ) : (
      <p className={runSidebarNoNotebookClass}>Select or create a notebook to enable execution and scheduling.</p>
    );
    return (
      <div>
        {notebookIndependent}
        {notebookDependent}
      </div>
    );
  };

  private renderViewButtons() {
    return (
      <div className={runSidebarSectionClass}>
        <header>View Notebook Operations & Datasets</header>
        <div>
          <div className={flexButtonsClass}>
            <input
              className={sidebarButtonClass}
              type="button"
              title="View notebook runs"
              value="Runs"
              onClick={this.onRunListClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="View notebook scheduled workflows"
              value="Workflow Jobs"
              onClick={this.onScheduleListClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="View datasets"
              value="Datasets"
              onClick={this.onDatasetListClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="View projects"
              value="Projects"
              onClick={this.onProjectListClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="View containers"
              value="Containers"
              onClick={this.onContainerListClick}
            />
            {/*<input*/}
            {/*  className={sidebarButtonClass}*/}
            {/*  type="button"*/}
            {/*  title="View notebook scans"*/}
            {/*  value="Scans"*/}
            {/*  onClick={this.onScheduleListClick}*/}
            {/*/>*/}
          </div>
        </div>
      </div>
    );
  }

  private renderConfigParams() {
    return (
        <div className={runSidebarSectionClass}>
        <header>DataPlate Configuration</header>
        <div>
          <InputColumn>
            <LabeledTextInput
              label="DataPlate Server URL:"
              value={this.state.serverURL}
              title="DataPlate Server URL to communicate with"
              placeholder=""
              onChange={this.onServerUrlChange}
            />
            <LabeledPasswordInput
              label="DataPlate Access Key:"
              value={this.state.accessKey}
              title="DataPlate Access Key to use for specific user"
              placeholder=""
              onChange={this.onAccessKeyChange}
            />
          </InputColumn>
          <a href="https://api.dataplate.io/reference/api-reference" style={{'color': 'blue'}} target="_blank" rel="noreferrer">
            <i className="fa fa-info-circle blueiconcolor"> <u>Dataplate API</u></i>
          </a>
        </div>
      </div>
    );
  }


  private renderRunsFilterParams() {
    return (
        <div className={runSidebarSectionClass}>
        <header>Filter runs by project/sub-project</header>
        <div>
          <InputColumn>
            <LabeledTextInputMaxWidth
              label=""
              value={this.state.project}
              title="Filter notebook runs by project"
              placeholder="Filter by project name"
              onChange={this.onProjectChange}
            />
            <LabeledTextInputMaxWidth
              label=""
              value={this.state.subproject}
              title="Filter notebook runs by sub-project"
              placeholder="Filter by sub-project name"
              onChange={this.onSubProjectChange}
            />
          </InputColumn>
        </div>
      </div>
    );
  }

  private renderCurrentNotebook() {
    const notebook = this.state.notebook;
    let notebookDisplay: React.ReactElement;
    if (notebook != null) {
      notebookDisplay = <span>{notebook}</span>;
    } else {
      notebookDisplay = <span>No notebook selected</span>;
    }

    return (
      <div className={runSidebarSectionClass}>
        <header>Current Notebook</header>
        <p className={runSidebarNotebookNameClass}>{notebookDisplay}</p>
      </div>
    );
  }


  private renderRunParameters() {
    return (
      <div className={runSidebarSectionClass}>
        <header>Notebook Execution</header>
        <ParameterEditor
          onChange={this.onParametersChange}
          notebookPanel={this.currentNotebookPanel}
          notebookPanelChanged={this.currentNotebookChanged}
        />
        <InputColumn>
          <LabeledTextInput
            label="Image:"
            value={this.state.image}
            title="ECR image to use"
            placeholder=""
            onChange={this.onImageChange}
          />
          <LabeledTextInput
            label="Role:"
            value={this.state.role}
            title="IAM role to use"
            placeholder=""
            onChange={this.onRoleChange}
          />
          <LabeledTextInput
            label="Instance:"
            value={this.state.instanceType}
            title="Instance type to run on"
            placeholder=""
            onChange={this.onInstanceTypeChange}
          />
          <LabeledTextInput
            label="Security Group IDs:"
            value={this.state.securityGroups}
            title="Security groups separated by comma"
            placeholder=""
            onChange={this.onSecurityGroupsChange}
          />
          <LabeledTextInput
            label="Subnets:"
            value={this.state.subnets}
            title="Subnets separated by comma"
            placeholder=""
            onChange={this.onSubnetsChange}
          />
          <LabeledNumberInput
            label="Max run minutes:"
            value={this.state.maxMinutes}
            title="Maximum minutes to run the job"
            placeholder=""
            onChange={this.onMaxMinutesChange}
          />
        </InputColumn>
      </div>
    );
  }

  private renderScheduleParameters() {
    return (
      <div className={runSidebarSectionClass}>
        <header>Schedule Rule</header>
        <InputColumn>
          <LabeledTextInput
            label="Rule Name:"
            value={this.state.ruleName}
            title="A name for this schedule"
            placeholder=""
            onChange={this.onRuleNameChange}
          />
          <LabeledTextInput
            label="Schedule:"
            value={this.state.schedule}
            title="Schedule for the notebook run"
            placeholder=""
            onChange={this.onScheduleChange}
          />
          <LabeledTextInput
            label="Event Pattern:"
            value={this.state.eventPattern}
            title="Events to trigger the notebook run"
            placeholder=""
            onChange={this.onEventPatternChange}
          />
        </InputColumn>
      </div>
    );
  }

  private renderExecuteButtons() {
    return (
      <div className={`${runSidebarSectionClass} ${runSidebarNoHeaderClass}`}>
        <div>
          <div className={flexButtonsClass}>
            <input
              className={sidebarButtonClass}
              type="button"
              title="Run the notebook now"
              value="Run Now"
              onClick={this.onRunClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="Create schedule"
              value="Create Schedule"
              onClick={this.onScheduleClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="Statistics Report for the notebook saved statistics"
              value="Statistics Report"
              onClick={this.onStatisticsReportClick}
            />
            <input
              className={sidebarButtonClass}
              type="button"
              title="Scan the notebook"
              value="Security Scan"
              onClick={this.onScanClick}
            />
          </div>
        </div>
      </div>
    );
  }

  private renderAlerts() {
    return (
      <div className={alertAreaClass}>
        {this.state.alerts.map((alert) => (
          <Alert key={`alert-${alert.key}`} type={alert.type} message={alert.message} />
        ))}
      </div>
    );
  }

  private onParametersChange = (editor: ParameterEditor): void => {
    this.setState({ parameters: editor.value });
  };

  private onServerUrlChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ serverURL: event.target.value }, () => this.saveState());
  };

  private onAccessKeyChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ accessKey: event.target.value }, () => this.saveState());
  };

  private onImageChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ image: event.target.value }, () => this.saveState());
  };

  private onRoleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ role: event.target.value }, () => this.saveState());
  };

  private onInstanceTypeChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ instanceType: event.target.value }, () => this.saveState());
  };

  private onSecurityGroupsChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ securityGroups: event.target.value }, () => this.saveState());
  };

  private onSubnetsChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ subnets: event.target.value }, () => this.saveState());
  };

  private onMaxMinutesChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ maxMinutes: event.target.value }, () => this.saveState());
  };

  private onRuleNameChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ ruleName: event.target.value }, () => this.saveState());
  };

  private onScheduleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ schedule: event.target.value }, () => this.saveState());
  };

  private onEventPatternChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ eventPattern: event.target.value }, () => this.saveState());
  };

  private onProjectChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ project: event.target.value }, () => this.saveState());
  };

  private onSubProjectChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    this.setState({ subproject: event.target.value }, () => this.saveState());
  };

  private onRunListClick = async (): Promise<void> => {
    this.props.runsModel.setDataplateServerKey(this.state.serverURL,this.state.accessKey)
    this.props.runsModel.setProject(this.state.project,this.state.subproject)
    this.app.commands.execute('dataplate-lab:open_list_runs');
  };

  private onScheduleListClick = async (): Promise<void> => {
      this.props.rulesModel.setDataplateServerKey(this.state.serverURL,this.state.accessKey)
      this.app.commands.execute('dataplate-lab:open_list_schedules');
  };

  private onDatasetListClick = async (): Promise<void> => {
      this.props.datasetsModel.setDataplateServerKey(this.state.serverURL,this.state.accessKey)
      this.app.commands.execute('dataplate-lab:open_list_datasets');
  };

  private onProjectListClick = async (): Promise<void> => {
      this.props.projectsModel.setDataplateServerKey(this.state.serverURL,this.state.accessKey)
      this.app.commands.execute('dataplate-lab:open_list_projects');
  };

  private onContainerListClick = async (): Promise<void> => {
      this.props.containersModel.setDataplateServerKey(this.state.serverURL,this.state.accessKey)
      this.app.commands.execute('dataplate-lab:open_list_containers');
  };


  private onRunClick = async (): Promise<void> => {
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
      const request: InvokeRequest = {
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
    } catch (e) {
      this.addAlert({
        type: 'error',
        message: `Error starting run for "${this.state.notebook}": ${e.message}`,
      });
    }
  };

  private onScheduleClick = async (): Promise<void> => {
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
      const request: CreateRuleRequest = {
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
    } catch (e) {
      this.addAlert({
        type: 'error',
        message: `Error creating rule "${this.state.ruleName}": ${e.message}`,
      });
    }
  };

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
  private hasParameterCell(): boolean {
    if (!this.currentNotebookPanel) {
      return false;
    }
    const cells = this.currentNotebookPanel.model.cells;
    for (let i = 0; i < cells.length; i++) {
      const tags = cells.get(i).metadata.get('tags') as JSONArray;
      if (tags && tags.includes('parameters')) {
        return true;
      }
    }
    return false;
  }

  private runReady(): string[] {
    const result: string[] = [];
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

  private async invokeNotebook(request: InvokeRequest): Promise<string> {
    const errors = this.runReady();
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }
    const settings = ServerConnection.makeSettings();
    const response = await ServerConnection.makeRequest(
      URLExt.join(settings.baseUrl, 'dataplate-lab', 'run'),
      { method: 'POST', body: JSON.stringify(request) },
      settings,
    );

    if (!response.ok) {
      const error = (await response.json()) as ErrorResponse;
      let errorMessage: string;
      if (error.error) {
        errorMessage = error.error.message;
      } else {
        errorMessage = JSON.stringify(error);
      }
      throw Error(errorMessage);
    }

    const data = (await response.json()) as InvokeResponse;
    return data.job_name;
  }

  // Return an array of reasons that we can't create a schedule.
  private scheduleReady(): string[] {
    const result = this.runReady();
    if (!this.state.ruleName) {
      result.push('missing schedule name');
    }
    if (!(this.state.schedule || this.state.eventPattern)) {
      result.push('must have either a schedule or an event pattern');
    }
    return result;
  }

  private async createRule(ruleName: string, request: CreateRuleRequest): Promise<string> {
    const errors = this.scheduleReady();
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }
    const settings = ServerConnection.makeSettings();
    const response = await ServerConnection.makeRequest(
      URLExt.join(settings.baseUrl, 'dataplate-lab', 'schedule', ruleName),
      { method: 'POST', body: JSON.stringify(request) },
      settings,
    );

    if (!response.ok) {
      const error = (await response.json()) as ErrorResponse;
      let errorMessage: string;
      if (error.error) {
        errorMessage = error.error.message;
      } else {
        errorMessage = JSON.stringify(error);
      }
      throw Error(errorMessage);
    }

    const data = (await response.json()) as CreateRuleResponse;
    return data.rule_name;
  }

  ////////////////////////
  /* START SECURITY SCAN*/
  ////////////////////////

  private onScanClick = async (): Promise<void> => {
    console.log('Scan Notebook!!!');
    this.clearAlerts();
    try {
      this.addAlert({
        type: 'notice',
        message: `Scanning Notebook "${this.state.notebook}"`,
      });

      const request: ScanRequest = {
        notebook_file_path: this.currentNotebookPanel.context.contentsModel.path,
        serverURL: this.state.serverURL,
        accessKey: this.state.accessKey,
      };

      const report_name = await this.scanNotebook(this.state.notebook, request);
      this.addAlert({ message: `Scan finished successfully for notebook ${this.state.notebook}, open report file ${report_name} from your root folder`});
      console.log(`Scan finished successfully for notebook ${this.state.notebook}, open report file ${report_name}`);
    } catch (e) {
      this.addAlert({
        type: 'error',
        message: `Error scan notebook "${this.state.notebook}": ${e.message}`,
      });
    }
  };

  // Return an array of reasons that we can't scan a notebook.
  private scanReady(): string[] {
    const result: string[] = [];
    if (!this.state.notebook) {
      result.push('missing notebook name - did you save your notebook ?');
    }
    if (!this.currentNotebookPanel.context.contentsModel.path.endsWith('.ipynb')) {
      result.push('Youe `CURRENT NOTEBOOK` must be a proper notebook file with extension .ipynb');
    }
    return result;
  }

  private async scanNotebook(notebookName: string, request: ScanRequest): Promise<string> {
    const errors = this.scanReady();
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }
    const settings = ServerConnection.makeSettings();

    const response = await ServerConnection.makeRequest(
      URLExt.join(settings.baseUrl, 'dataplate-lab', 'scan', notebookName),
      { method: 'POST', body: JSON.stringify(request) },
      settings,
    );

    if (!response.ok) {
      const error = (await response.json()) as ErrorResponse;
      let errorMessage: string;
      if (error.error) {
        errorMessage = error.error.message;
      } else {
        errorMessage = JSON.stringify(error);
      }
      throw Error(errorMessage);
    }

    const data = (await response.json()) as ScanResponse;
    return data.report_name;
  }

  ///* END SECURITY SCAN *///


  ////////////////////////////
  /* START Statistics Report*/

  private onStatisticsReportClick = async (): Promise<void> => {
    console.log('Statistics Report for Notebook!!!');
    this.clearAlerts();
    try {
      this.addAlert({
        type: 'notice',
        message: `Generating statistics report (5 last runs) for Notebook "${this.state.notebook}"`,
      });

      const request: StatisticsReportRequest = {
        notebook_name: this.state.notebook,
        serverURL: this.state.serverURL,
        accessKey: this.state.accessKey,
      };

      const report_name = await this.statisticsReportNotebook(request);
      this.addAlert({ message: `Statistics report finished successfully for notebook ${this.state.notebook}, open report file ${report_name} from your root folder`});
      console.log(`Statistics report finished successfully for notebook ${this.state.notebook}, open report file ${report_name}`);
    } catch (e) {
      this.addAlert({
        type: 'error',
        message: `Error generating statistics report for notebook "${this.state.notebook}": ${e.message}`,
      });
    }
  };

  // Return an array of reasons that we can't scan a notebook.
  private statisticsReportReady(): string[] {
    const result: string[] = [];
    if (!this.state.notebook) {
      result.push('missing notebook name - did you save your notebook ?');
    }
    return result;
  }

  private async statisticsReportNotebook(request: StatisticsReportRequest): Promise<string> {
    const errors = this.statisticsReportReady();
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }
    const settings = ServerConnection.makeSettings();

    const response = await ServerConnection.makeRequest(
      URLExt.join(settings.baseUrl, 'dataplate-lab', 'reportstatistics'),
      { method: 'POST', body: JSON.stringify(request) },
      settings,
    );

    if (!response.ok) {
      const error = (await response.json()) as ErrorResponse;
      let errorMessage: string;
      if (error.error) {
        errorMessage = error.error.message;
      } else {
        errorMessage = JSON.stringify(error);
      }
      throw Error(errorMessage);
    }

    const data = (await response.json()) as StatisticsReportResponse;
    return data.report_name;
  }


  /* END Statistics Report*/
  //////////////////////////

  private alertKey = 0;
  private addAlert(alert: AlertProps) {
    const key = this.alertKey++;

    const keyedAlert: AlertProps & { key: string } = { ...alert, key: `alert-${key}` };
    this.setState({ alerts: [keyedAlert] });
  }

  private clearAlerts() {
    this.setState({ alerts: [] });
  }

  private saveState() {
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

  private loadState() {
    this.props.stateDB.fetch(KEY).then((s) => {
      const state = s as ReadonlyJSONObject;
      if (state) {
        this.setState({
          image: state['image'] as string,
          role: state['role'] as string,
          instanceType: state['instanceType'] as string,
          ruleName: state['ruleName'] as string,
          schedule: state['schedule'] as string,
          eventPattern: state['eventPattern'] as string,
          serverURL: state['serverURL'] as string,
          accessKey: state['accessKey'] as string,
          securityGroups: state['securityGroups'] as string,
          subnets: state['subnets'] as string,
          maxMinutes: state['maxMinutes'] as string,
          project: state['project'] as string,
          subproject: state['subproject'] as string,
        });
      }
    });
  }

  private app: JupyterFrontEnd;
  private shell: ILabShell;

  private currentNotebookPanel: NotebookPanel;
  private notebook: string;
  private currentNotebookChanged: Signal<SchedulePanel, NotebookPanel>;
}
