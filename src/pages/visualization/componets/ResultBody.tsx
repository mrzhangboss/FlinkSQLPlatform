import React, { Component } from 'react';
import { Button, Card, Table, Tag } from 'antd';
import { connect } from 'dva';
import { Dispatch } from 'redux';
import { TableDetail, VisualizationResult } from '../data';

interface ResultProp {
  loading: boolean;
  submitting: boolean;
  tables: TableDetail[];
  current?: TableDetail;
  dispatch: Dispatch<any>;
}

interface ResultState {}

@connect(
  ({
    visualization,
    loading,
  }: {
    visualization: VisualizationResult;
    loading: { effects: { [key: string]: boolean } };
  }) => ({
    tables: visualization.details,
    current: visualization.current,
    loading: loading.effects['visualization/fetchTables'],
    submitting: loading.effects['visualization/submitSelectTable'],
  }),
)
class ResultBody extends Component<ResultProp, ResultState> {
  state: ResultState = {};

  generateTableColumn = (source: TableDetail) => {
    if (source.loading) return [];
    if (!Array.isArray(source.fieldNames)) return [];
    const fields = source.fieldNames.map(fd => {
      return {
        title: fd,
        dataIndex: fd,
        key: fd,
        ellipsis: true,
        width: 200,
      };
    });
    return fields;
  };

  getListBody = (source: TableDetail) => {
    // @ts-ignore
    return (
      <Table
        rowKey={'tableName'}
        columns={this.generateTableColumn(source)}
        dataSource={source.data}
        loading={source.loading}
        scroll={{ x: 1800 }}
      />
    );
  };

  activeTable = (type: string, tableName: string) => {
    console.log(tableName);
    const { dispatch } = this.props;
    const tableNames = [type, ...tableName.split('.')];
    dispatch({
      type: 'visualization/startChangeCurrentTable',
      tableNames: tableNames,
    });
  };

  deleteTable = (tableName: string) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'visualization/deleteTable',
      tableName: tableName,
    });
  };

  generateTableTitle = (tab: TableDetail) => {
    const typ = tab.typ;
    const color = typ === 'mysql' ? 'blue' : typ === 'hive' ? 'cyan' : 'orange';
    const tagName = tab.tableName !== undefined ? tab.tableName.split('.')[0] : 'null';
    const dbName = tab.tableName !== undefined ? tab.tableName.split('.')[1] : 'null';
    const tag = <Tag color={color}>{tagName}</Tag>;
    return (
      <div>
        {tag}
        {dbName}
      </div>
    );
  };

  // @ts-ignore
  generateTableDetail = (tab: TableDetail) => {
    return (
      <Card
        hoverable
        onDoubleClick={x => this.activeTable(tab.typ, tab.tableName)}
        key={tab.tableName}
        title={this.generateTableTitle(tab)}
        style={{ marginBottom: 24, borderRadius: 10 }}
        bordered={false}
        loading={tab.loading}
        extra={
          <Button type="danger" onClick={x => this.deleteTable(tab.tableName)}>
            删除{' '}
          </Button>
        }
      >
        {this.getListBody(tab)}
      </Card>
    );
  };

  render() {
    const { loading, tables, current } = this.props;
    const displayTables = tables.filter(
      x => current === undefined || x.tableName !== current.tableName,
    );
    if (displayTables.length === 0) {
      return <></>;
    } else {
      return (
        <Card loading={loading} style={{ marginTop: 20, borderRadius: 10 }}>
          {displayTables.map(x => this.generateTableDetail(x))}
        </Card>
      );
    }
  }
}

export default ResultBody;