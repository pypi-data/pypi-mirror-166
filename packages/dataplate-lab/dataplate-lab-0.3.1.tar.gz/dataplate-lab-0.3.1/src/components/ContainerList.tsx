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

import { ContainersModel, ContainersUpdate } from '../models/ContainersModel';
import {Container} from '../server';
import { SimpleTable, SimpleTablePage } from './SimpleTable';
import {tableEmptyClass} from '../style/tables';

export interface ContainerListProps {
  model: ContainersModel;
}

interface ContainerListState {
  containers: Container[];
  error: string;
}

const Headers = ['Name', 'LastModified', ''];

export class ContainerList extends React.Component<ContainerListProps, ContainerListState> {
  constructor(props: ContainerListProps) {
    super(props);
    this.state = { containers: props.model.containers, error: null };

    props.model.containersChanged.connect(this.onContainersChanged, this);
  }

  private onContainersChanged(_: ContainersModel, ContainerInfo: ContainersUpdate): void {
    this.setState({ containers: ContainerInfo.containers, error: ContainerInfo.error });
  }

  componentWillUnmount(): void {
    this.props.model.containersChanged.disconnect(this.onContainersChanged, this);
  }

  private extractRow = (container: Container): (string | JSX.Element)[] => {

    return [
      container.Name,
      container.LastModified
    ];
  };

  render(): JSX.Element {
    let content: JSX.Element;
    if (this.state.containers) {
      // sometimes it seems that render gets called before the constructor ???
      const rows = this.state.containers.map(this.extractRow);
      if (rows.length === 0) {
        content = <div className={tableEmptyClass}>No Containers are available - or no proper permission</div>;
      } else {
        content = <SimpleTable headings={Headers} rows={rows} />;
      }
    } else if (this.state.error) {
      content = <div className={tableEmptyClass}>Error retrieving Containers: {this.state.error}</div>;
    } else {
      content = <div className={tableEmptyClass}>Loading Containers...</div>;
    }
    return <SimpleTablePage title="Containers List">{content}</SimpleTablePage>;
  }

}
