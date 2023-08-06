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

import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';

import React from 'react';
import { Project, ListProjectsResponse, ErrorResponse, DataPlateConfig } from '../server';
import { showDialog, Dialog } from '@jupyterlab/apputils';

// import { sectionClass, labeledRowClass, kvContainer } from '../style/RunDetailsDialog';
import {tableEmptyClass} from "../style/tables"; //, tableLinkClass
import { SimpleTable, SimpleTablePage } from './SimpleTable';
// import {ProjectsModel} from "../models/ProjectsModel";

export interface ProjectsUpdate {
  projects: Project[] | null;
  error: string;
}

async function loadSubProjects(projectName: string, serverURL: string, accessKey: string): Promise<ProjectsUpdate> {
  try{
    const settings = ServerConnection.makeSettings();

    const request: DataPlateConfig = {
        serverURL: serverURL,
        accessKey: accessKey,
      };

    const response = await ServerConnection.makeRequest(
          URLExt.join(settings.baseUrl, 'dataplate-lab', 'subprojects', projectName),
          { method: 'POST' , body: JSON.stringify(request)},
          settings,
        );


    if (!response.ok) {
      const error = (await response.json()) as ErrorResponse;
      if (error.error) {
        return { projects: null, error: error.error.message };
      } else {
        return { projects: null, error: JSON.stringify(error) };
      }
    }

    const data = (await response.json()) as ListProjectsResponse;
    return { projects: data.projects, error: null };
  } catch (e) {
    return { projects: null, error : e.message};
  }
}


export function showSubProjects(projectName: string, serverURL: string, accessKey: string): () => Promise<void> {
  return async () => {
    let subprojects: ProjectsUpdate;
    let error: string;

    try {
      subprojects = await loadSubProjects(projectName,serverURL,accessKey);
    } catch (e) {
      error = e.message;
    }

    let title: string;
    if (subprojects.projects) {
      if (projectName) {
        title = `Sub-Projects list for Project: "${projectName}"`;
      } else {
        title = `Sub-Projects list`;
      }
    } else {
      title = 'Error retrieving Sub-Projects';
    }
    showDialog({
      title: title,
      body: <SubProjectsDialogBody projectName={projectName} subprojects={subprojects.projects} error={error} />,
      buttons: [Dialog.okButton({ label: 'Close' })],
    });
  };
}

// interface LabeledRowProps {
//   label: string;
//   content: string | JSX.Element;
// }

// const LabeledRow: React.SFC<LabeledRowProps> = (props) => {
//   return (
//     <tr className={labeledRowClass}>
//       <td>{props.label}:</td>
//       <td>{props.content}</td>
//     </tr>
//   );
// };
interface SubprojectDetailsDialogBodyProps {
  projectName: string;
  subprojects: Project[];
  error: string;
}

interface SubProjectsDialogBodyState {
  subprojects: Project[] | null;
  error?: string;
}

const Headers = ['Name', 'Created', 'LastModified'];

export class SubProjectsDialogBody extends React.Component<SubprojectDetailsDialogBodyProps, SubProjectsDialogBodyState> {
  constructor(props: SubprojectDetailsDialogBodyProps) {
    super(props);
    this.state = { subprojects: props.subprojects, error: props.error };
  }

  private extractRow = (project: Project): (string | JSX.Element)[] => {

    return [
      project.Name,
      project.Created,
      project.LastModified
    ];
  };

  render(): JSX.Element {
    let content: JSX.Element;
    if (this.state.subprojects) {
      // sometimes it seems that render gets called before the constructor ???
      const rows = this.state.subprojects.map(this.extractRow);
      if (rows.length === 0) {
        content = <div className={tableEmptyClass}>No Sub-Projects are available</div>;
      } else {
        content = <SimpleTable headings={Headers} rows={rows} />;
      }
    } else if (this.state.error) {
      content = <div className={tableEmptyClass}>Error retrieving sub-projects: {this.state.error}</div>;
    } else {
      content = <div className={tableEmptyClass}>Loading sub-projects...</div>;
    }
    return <SimpleTablePage title="Sub-Projects List">{content}</SimpleTablePage>;
  }

}
