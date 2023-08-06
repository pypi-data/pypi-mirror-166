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

import { ReactWidget } from '@jupyterlab/apputils';
import { IStateDB } from '@jupyterlab/statedb';
import { Widget } from '@lumino/widgets';
import * as React from 'react';
import { SchedulePanel } from '../components/SchedulePanel';
import { RunsModel } from '../models/RunsModel';
import { scheduleWidgetStyle } from '../style/ScheduleWidgetStyle';
import { JupyterFrontEnd, ILabShell } from '@jupyterlab/application';
import { RulesModel } from '../models/RulesModel';
import {DatasetsModel} from "../models/DatasetsModel";
import {ProjectsModel} from "../models/ProjectsModel";
import {ContainersModel} from "../models/ContainersModel";

/**
 * A class that exposes the Schedule plugin Widget.
 */
export class ScheduleWidget extends ReactWidget {
  constructor(
    app: JupyterFrontEnd,
    shell: ILabShell,
    runsModel: RunsModel,
    rulesModel: RulesModel,
    datasetsModel: DatasetsModel,
    projectsModel: ProjectsModel,
    containersModel: ContainersModel,
    stateDB: IStateDB,
    options?: Widget.IOptions,
  ) {
    super(options);
    this.node.id = 'ScheduleSession-root';
    this.addClass(scheduleWidgetStyle);

    this.app = app;
    this.shell = shell;
    this.runsModel = runsModel;
    this.rulesModel = rulesModel;
    this.datasetsModel = datasetsModel;
    this.projectsModel = projectsModel;
    this.containersModel = containersModel;
    this.stateDB = stateDB;
    console.log('Schedule widget created');
  }

  render() {
    return (
      <SchedulePanel
        app={this.app}
        shell={this.shell}
        runsModel={this.runsModel}
        rulesModel={this.rulesModel}
        datasetsModel={this.datasetsModel}
        projectsModel={this.projectsModel}
        containersModel={this.containersModel}
        stateDB={this.stateDB}
      />
    );
  }

  private app: JupyterFrontEnd;
  private shell: ILabShell;
  private runsModel: RunsModel;
  private rulesModel: RulesModel;
  private datasetsModel: DatasetsModel;
  private projectsModel: ProjectsModel;
  private containersModel: ContainersModel;
  private stateDB: IStateDB;
}
