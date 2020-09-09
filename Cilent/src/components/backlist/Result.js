import React, { Component } from "react";
import { Spin } from "antd";
import { Table, Tag, Space } from "antd";

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    console.log(this.props.results, this.props.props, "RESUTS");
    const columns = [
      {
        title: "PERFORMANCE_MATRIX",
        dataIndex: "name",
        key: "name",
        //   render: text => <a>{text}</a>,
      },
      {
        title: "VALUES",
        dataIndex: "VALUES",
        key: "VALUES",
      },
    ];

    const data = [
      {
        key: "1",
        name: "Trade_start_date",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Trade_start_date"],
      },
      {
        key: "2",
        name: "Trade end date",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Trade_end_date"],
      },
      {
        key: "3",
        name: "Initial_Capital",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Initial_Capital"],
      },
      {
        key: "4",
        name: "Ending_Capital",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Ending_Capital"],
      },
      {
        key: "5",
        name: "Initial_Capital",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Initial_Capital"],
      },
      {
        key: "6",
        name: "Total_no_trades",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Total_no_trades"],
      },
      {
        key: "7",
        name: "Positive_trades",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Positive_trades"],
      },
      {
        key: "8",
        name: "Negative_trades",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Negative_trades"],
      },
      {
        key: "9",
        name: "Total_loss",
        VALUES:
          this.props.results != undefined && this.props.results["Total_loss"],
      },
      {
        key: "8",
        name: "Negative_trades",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Negative_trades"],
      },
      {
        key: "9",
        name: "Net_Profit",
        VALUES:
          this.props.results != undefined && this.props.results["Net_Profit"],
      },
      {
        key: "10",
        name: "Sharpe_ratio",
        VALUES:
          this.props.results != undefined && this.props.results["Sharpe_ratio"],
      },
      {
        key: "11",
        name: "CAGR",
        VALUES: this.props.results != undefined && this.props.results["CAGR"],
      },
      {
        key: "12",
        name: "Maximum_Drawdown",
        VALUES:
          this.props.results != undefined &&
          this.props.results["Maximum_Drawdown"],
      },
    ];

    return this.props.props == false ? (
      <Table columns={columns} dataSource={data} pagination={false} scroll={{y:500}} />
    ) : (
      <Spin tip="Loading..."></Spin>
    );
  }
}

export default Result;
