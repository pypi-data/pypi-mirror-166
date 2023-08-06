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

import { ProjectsModel, ProjectsUpdate } from '../models/ProjectsModel';
import {Project} from '../server';
import { SimpleTable, SimpleTablePage } from './SimpleTable';
import {tableEmptyClass, tableLinkClass} from '../style/tables';
import {showSubProjects} from "./SubProjectsDialog";


function viewSubProjects(projectName: string, serverURL: string, accessKey: string): () => Promise<void> {
  return showSubProjects(projectName,serverURL,accessKey);
}

export interface ProjectListProps {
  model: ProjectsModel;
}

interface ProjectListState {
  projects: Project[];
  error: string;
}

const Headers = ['Name', 'Created', 'LastModified', ''];

export class ProjectList extends React.Component<ProjectListProps, ProjectListState> {
  constructor(props: ProjectListProps) {
    super(props);
    this.state = { projects: props.model.projects, error: null };

    props.model.projectsChanged.connect(this.onProjectsChanged, this);
  }

  private onProjectsChanged(_: ProjectsModel, projectInfo: ProjectsUpdate): void {
    this.setState({ projects: projectInfo.projects, error: projectInfo.error });
  }

  componentWillUnmount(): void {
    this.props.model.projectsChanged.disconnect(this.onProjectsChanged, this);
  }

  private extractRow = (project: Project): (string | JSX.Element)[] => {

    return [
      project.Name,
      project.Created,
      project.LastModified,
      <a key={project.Name} onClick={viewSubProjects(project.Name,this.props.model.serverURL,this.props.model.accessKey)} className={tableLinkClass}>
        Sub-Projects
      </a>
    ];
  };

  render(): JSX.Element {
    let content: JSX.Element;
    if (this.state.projects) {
      // sometimes it seems that render gets called before the constructor ???
      const rows = this.state.projects.map(this.extractRow);
      if (rows.length === 0) {
        content = <div className={tableEmptyClass}>No Projects are available - or no proper permission</div>;
      } else {
        content = <SimpleTable headings={Headers} rows={rows} />;
      }
    } else if (this.state.error) {
      content = <div className={tableEmptyClass}>Error retrieving projects: {this.state.error}</div>;
    } else {
      content = <div className={tableEmptyClass}>Loading projects...</div>;
    }
    return <SimpleTablePage title="Projects List">{content}</SimpleTablePage>;
  }

}
